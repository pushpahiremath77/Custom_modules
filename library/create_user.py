from ansible.module_utils.basic import AnsibleModule
import subprocess

def run_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr

def main():
    module_args = {
        "action" : {"type" : "str", "required" : True},
        "user" : {"type" : "str", "required" : False},
        "password" : {"type" : "str", "required" : False},
    }

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    action = module.params['action']
    try:
        if action == "install":
            rc, out, err = run_command("apt update && apt install -y mysql-server")
            module.exit_json(changed=True, msg=" MySQL installed successfully.")
        elif action == "start":
            rc, out, err = run_command("systemctl start mysql")
            module.exit_json(changed=True, msg=" MySQL started successfully.")
        elif action == "stop":
            rc, out, err = run_command("systemctl stop mysql")
        elif action == "create_user":
            user = module.params['user']
            password = module.params['password']

            check_user_cmd = f"mysql -e \"SELECT EXISTS(SELECT 1 FROM mysql.user WHERE user = '{user}');\""
            rc, out, err = run_command(check_user_cmd)

            if "1" in out:
                module.exit_json(changed=False, msg=f"The user with name '{user}' exists!")
            else:
                rc, out, err = run_command(f'mysql -e "CREATE USER \'{user}\'@\'%\' IDENTIFIED BY \'{password}\';"')
                if rc == 0:
                    module.exit_json(changed=True, msg=f"User '{user}' created successfully.")
                else:
                    module.fail_json(msg=f"Failed to create user '{user}'", stdout=out, stderr=err)

        else:
            module.fail_json(msg="Invalid action provided")
    except Exception as e:
        module.fail_json(msg=f"Exception occurred: {str(e)}")

if __name__ == '__main__':
    main()
