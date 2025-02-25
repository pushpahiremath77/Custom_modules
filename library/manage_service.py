#!/usr/bin/python
from ansible.module_utils.basic import AnsibleModule

def manage_service(module, service_name, action):

    cmd = ["systemctl", action, service_name]

    rc, stdout, stderr = module.run_command(cmd)

    if rc == 0:
        return stdout, False
    else:
        module.fail_json(msg=f"Failed to {action} service {service_name}: {stderr}")

def run_module():

    module_args = dict(
        service_name=dict(type='str', required=True),
        action=dict(type='str', choices=['start', 'stop', 'restart', 'status', 'enable', 'disable'], required=True),
    )


    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )


    service_name = module.params['service_name']
    action = module.params['action']

    if module.check_mode:
        module.exit_json(changed=False)

    output, changed = manage_service(module, service_name, action)

    if action in ['start', 'stop', 'restart', 'enable', 'disable']:
        changed = True

    module.exit_json(changed=changed, message=f"Service {service_name} {action} successfully", output=output)

def main():
    run_module()

if __name__ == '__main__':
    main()
