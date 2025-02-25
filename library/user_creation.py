#!/usr/bin/python
from ansible.module_utils.basic import AnsibleModule

def run_module(module, username, state):
    if state == "present":
        cmd = "useradd " + username
        rc, stdout, stderr = module.run_command(cmd, check_rc=False)

        if rc == 9:
            module.exit_json(changed=False, msg=f"User {username} already exists.")
        elif rc != 0:
            module.fail_json(msg=f"Failed to add user {username}: {stderr}")

        return dict(changed=True, msg=f"User {username} added successfully.")

    elif state == "absent":
        cmd = "userdel " + username
        rc, stdout, stderr = module.run_command(cmd, check_rc=False)

        if rc == 6:
            module.exit_json(changed=False, msg=f"User {username} not found.")
        elif rc != 0:
            module.fail_json(msg=f"Failed to delete user {username}: {stderr}")

        return dict(changed=True, msg=f"User {username} deleted successfully.")

    else:
        module.fail_json(msg="Invalid state. Use present or absent")


def main():
    module_args = dict(
        username=dict(type='str', required=True),
        state=dict(type='str', choices=['present', 'absent'], default='present')
    )

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    username = module.params['username']
    state = module.params['state']

    result = run_module(module, username, state)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
