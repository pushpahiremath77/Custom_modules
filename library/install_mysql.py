#!/usr/bin/python
from ansible.module_utils.basic import AnsibleModule
import subprocess

def is_mysql_installed(module):
    """Check if MySQL is already installed and return the version if installed"""
    try:
        result = subprocess.run(['mysql', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            version = result.stdout.decode('utf-8').strip()
            return True, version
        else:
            return False, None
    except FileNotFoundError:
        return False, None
    except Exception as e:
        module.fail_json(msg=f'Failed to check MySQL installation: {str(e)}')

def install_mysql(module):
    """Install MySQL using apt package manager"""
    try:
        subprocess.run(["apt-get", "update"], check=True)
        subprocess.run(["apt-get", "-y", "install", "mysql-server"], check=True)
        return True
    except subprocess.CalledProcessError as e:
        module.fail_json(msg=f"Failed to install MySQL: {str(e)}")

def run_module():
    result = dict(
        changed=False,
        message=''
    )

    module = AnsibleModule(
        argument_spec={},
        supports_check_mode=True
    )

    # Check mode, don't perform any changes
    if module.check_mode:
        module.exit_json(**result)

    # Check if MySQL is already installed
    installed, version = is_mysql_installed(module)
    if installed:
        result['message'] = f"MySQL is already installed: {version}"
        module.exit_json(**result)

    # Install MySQL
    if install_mysql(module):
        result['changed'] = True
        result['message'] = "MySQL successfully installed."

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
