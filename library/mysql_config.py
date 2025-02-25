#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
import os
import re

def update_config(config_path, param, value):
    try:
        with open(config_path, 'r') as f:
            config_content = f.readlines()
    except IOError as e:
        return {"failed": True, "msg": f"Unable to read {config_path}: {str(e)}"}

    param_found = False
    new_content = []
    for line in config_content:
        if re.match(rf'^\s*{param}\s*=.*$', line):
            new_content.append(f"{param} = {value}\n")
            param_found = True
        else:
            new_content.append(line)

    
    if not param_found:
        new_content.append(f"{param} = {value}\n")

   
    try:
        with open(config_path, 'w') as f:
            f.writelines(new_content)
    except IOError as e:
        return {"failed": True, "msg": f"Unable to write to {config_path}: {str(e)}"}

    return {"changed": True, "msg": f"{param} updated to {value}"}

def main():
    
    module_args = dict(
        config_path=dict(type='str', required=True, default="/etc/mysql/my.cnf"),
        bind_address=dict(type='str', required=False, default=None),
        max_connections=dict(type='int', required=False, default=None),
    )

    
    module = AnsibleModule(argument_spec=module_args)

    config_path = module.params['config_path']
    bind_address = module.params['bind_address']
    max_connections = module.params['max_connections']

    
    if not os.path.exists(config_path):
        module.fail_json(msg=f"Config file {config_path} does not exist.")

    results = []

    
    if bind_address:
        result = update_config(config_path, 'bind-address', bind_address)
        if "failed" in result:
            module.fail_json(msg=result["msg"])
        results.append(result)

    
    if max_connections:
        result = update_config(config_path, 'max_connections', max_connections)
        if "failed" in result:
            module.fail_json(msg=result["msg"])
        results.append(result)

    if results:
        module.exit_json(changed=True, msg="MySQL configuration updated", details=results)
    else:
        module.exit_json(changed=False, msg="No changes made to MySQL configuration")

if __name__ == '__main__':
    main()
