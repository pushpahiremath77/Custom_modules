#!/usr/bin/python
from ansible.module_utils.basic import AnsibleModule

def create_mysql_user(module):
    username = module.params['username']
    password = module.params['password']
    db_name = module.params['db_name']
    root_password = module.params['root_password']

    # Log in as root to MySQL and create a user
    create_user_query = f"CREATE USER IF NOT EXISTS '{username}'@'localhost' IDENTIFIED BY '{password}';"
    create_db_query = f"CREATE DATABASE IF NOT EXISTS {db_name};"
    grant_privileges_query = f"GRANT ALL PRIVILEGES ON {db_name}.* TO '{username}'@'localhost';"
    flush_privileges_query = "FLUSH PRIVILEGES;"

    try:
        # Log in to MySQL and create user, database, and grant privileges (using TCP)
        cmd = ['mysql', '--protocol=tcp', '-u', 'root', '-p' + root_password, '-e', create_user_query]
        rc, _, stderr = module.run_command(cmd)
        if rc != 0:
            module.fail_json(msg=f"Failed to create user: {stderr}")

        cmd = ['mysql', '--protocol=tcp', '-u', 'root', '-p' + root_password, '-e', create_db_query]
        rc, _, stderr = module.run_command(cmd)
        if rc != 0:
            module.fail_json(msg=f"Failed to create database: {stderr}")

        cmd = ['mysql', '--protocol=tcp', '-u', 'root', '-p' + root_password, '-e', grant_privileges_query]
        rc, _, stderr = module.run_command(cmd)
        if rc != 0:
            module.fail_json(msg=f"Failed to grant privileges: {stderr}")

        cmd = ['mysql', '--protocol=tcp', '-u', 'root', '-p' + root_password, '-e', flush_privileges_query]
        rc, _, stderr = module.run_command(cmd)
        if rc != 0:
            module.fail_json(msg=f"Failed to flush privileges: {stderr}")

        module.exit_json(changed=True, message=f"User '{username}' created and granted privileges on '{db_name}'.")

    except Exception as e:
        module.fail_json(msg=f"An error occurred: {str(e)}")


def run_module():
    module_args = dict(
        username=dict(type='str', required=True),
        password=dict(type='str', required=True, no_log=True),
        db_name=dict(type='str', required=True),
        root_password=dict(type='str', required=True, no_log=True)
    )

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    if module.check_mode:
        module.exit_json(changed=False)

    create_mysql_user(module)

def main():
    run_module()

if __name__ == '__main__':
    main()
