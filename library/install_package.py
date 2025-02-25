#!usr/bin/python
from ansible.utils_module.basic import AnsibleModule
import subprocess

def install_package(package_name):
    try:
        subprocess.run(['apt-get','update'])
        subprocess.run(['apt-get','install','-y',package_name])
        return True, f"Package '{package_name}' installed successfully"
    except subprocess.CalledProcessError as e:
        return False, f"Failed to install package '{package_name}': {e}"
    

def remove_package(package_name):
    try:
        subprocess.run(['apt-get','remove','-y',package_name])
        return True, f"Package {package_name} removed successfully"
    except subprocess.CalledProcessError as e:
        return False, f"Failed to delete package '{package_name}': {e}"

def run_module():
    module_args = dict(
        name=dict(type='str', required=True),
        state=dict(type='str', choices=['present', 'absent'], default='present')
    )

    module = AnsibleModule(argument_spec=module_args)

    name = module.params['name']
    state = module.params['state']

    if state=='present':
        changed,msg=install_package(name)
    else:
        changed,msg=remove_package(name)

    if changed:
        module.exit_json(changed=True,msg=msg)
    else:
        module.fail_json(msg=msg)

if __name__ == '__main__':
    run_module()