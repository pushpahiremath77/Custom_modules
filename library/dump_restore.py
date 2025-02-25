#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
import subprocess

def run_command(module,command):
    rc,stdout,stderr=module.run_command(command,check_rc=True)
    return rc,stdout,stderr



def dump_database(module,user,password,database,dump_file):
    command = f"mysqldump -u {user} -p {password} {database} >{dump_file}"
    rc,stdout,stderr = run_command(module,command)
    return rc,stdout,stderr


def restore_database(module,user,password,database,dump_file):
    command = f"mysql -u {user} -p {password} {database} <{dump_file}"
    rc,stdout,stderr = run_command(module,command)
    return rc,stdout,stderr

def main():
    module = AnsibleModule(
        argument_spec=dict(
            user=dict(type='str', required=True),
            password=dict(type='str', required=True, no_log=True),
            database=dict(type='str', required=True),
            dump_file=dict(type='str', required=True),
            action=dict(type='str', choices=['dump', 'restore'], required=True)
        )
    )

    user = module.params['user']
    password = module.params['password']
    database = module.params['database']
    dump_file = module.params['dump_file']
    action = module.params['action']

    if action == 'dump':
        rc, stdout, stderr = dump_database(module, user, password, database, dump_file)
        if rc == 0:
            module.exit_json(changed=True, msg=f"Database {database} dumped to {dump_file} successfully.")
        else:
            module.fail_json(msg=f"Failed to dump database: {stderr}")

    elif action == 'restore':
        rc, stdout, stderr = restore_database(module, user, password, database, dump_file)
        if rc == 0:
            module.exit_json(changed=True, msg=f"Database {database} restored from {dump_file} successfully.")
        else:
            module.fail_json(msg=f"Failed to restore database: {stderr}")


if __name__ == '__main__':
    main()
