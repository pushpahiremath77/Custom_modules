#!usr/bin/python
from ansible.module_utils.basic import AnsibleModule
import csv

def main():

    module_args = dict(
        device_facts = dict(type='dict',required=True),
        dest_csv_path = dict(type='dict',required=True,default='home/ubuntu/Custom_modules/library/new_generated_file.csv'),
        dest_csv_file = dict(type='str',required=False,default='facts_file.csv')
    )

    module = AnsibleModule(
        argument_spec = module_args,
        supports_check_mode = True
    )

    device_facts = module.params['device_facts']
    csv_fiename = f"{module.params['dest_csv_path']}/{module.params['device_facts']}"

    csv_fiename = 'home/ubuntu/Custom_modules/library/new_generated_file.csv'
    csv_header = ['Inventory_name','host_name','model']

    with open(csv_fiename,'w') as csvfile:
        writer = csv.DictWriter(csvfile,fieldnames=csv_header)
        writer.writeheader()
        for device, details in sorted_device_items():
            writer.writerow({
                "Inventory_name":device,
                "host_name":details['net_hostname'],
                "model":details['net_model']
            })

    module.exit_json(changed=True,output="Saved content to csv file")

    if __name__ == "__main__":
        main()
