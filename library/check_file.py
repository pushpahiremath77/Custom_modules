#!/usr/bin/python
from ansible.module_utils.basic import AnsibleModule
import os

def main():
    module_args = dict(
        path=dict(type='str', required=True)
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    file_path = module.params['path']
    file_exists = os.path.exists(file_path)

    result = {
        'file_exists': file_exists
    }

    module.exit_json(changed=False, **result)

if __name__ == '__main__':
    main()
