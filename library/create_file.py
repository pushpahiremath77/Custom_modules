#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
import os

def run_module():
    module_args = dict(
        path=dict(type='str', required=True),
        content=dict(type='str', required=False, default="Hello World")
    )

    result = dict(
        changed=False,
        message='File already exists.'
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    path = module.params['path']
    content = module.params['content']

    if module.check_mode:
        module.exit_json(**result)

    if not os.path.exists(path):
        with open(path, 'w') as f:
            f.write(content)
        result['changed'] = True
        result['message'] = f'File created at {path}'
    else:
        result['message'] = 'File already exists.'

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
