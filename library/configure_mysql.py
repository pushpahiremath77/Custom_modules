#!/usr/bin/python
from ansible.module_utils.basic import AnsibleModule

def configure_mycnf(module):
    bind_address = module.params['bind_address']
    max_connections = module.params['max_connections']

    try:
        with open('/etc/mysql/my.cnf', 'a') as file:
            file.write(f"\nbind-address = {bind_address}\n")
            file.write(f"max_connections = {max_connections}\n")
        module.exit_json(changed=True, message="my.cnf configured successfully")

    except Exception as e:
        module.fail_json(msg=f"Failed to configure my.cnf: {str(e)}")

def run_module():
    module_args = dict(
        bind_address=dict(type='str', required=True),
        max_connections=dict(type='int', required=True)
    )

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    if module.check_mode:
        module.exit_json(changed=False)

    configure_mycnf(module)

def main():
    run_module()

if __name__ == '__main__':
    main()
