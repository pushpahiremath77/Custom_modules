import boto3

def fetch_instance_ips():
    ec2_client = boto3.client('ec2')
    response = ec2_client.describe_instances()
    instance_ips = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            public_ip = instance.get('PublicIpAddress', 'No Public IP')
            private_ip = instance.get('PrivateIpAddress', 'No Private IP')
            instance_ips.append({
                'InstanceId': instance_id,
                'Public IP': public_ip,
                'Private IP': private_ip
            })
    return instance_ips

if __name__ == "__main__":
    ips = fetch_instance_ips()

    if ips:
        print(f"{'Instance ID':<20} {'Public IP':<20} {'Private IP':<20}")
        print('-' * 60)
        for ip_info in ips:
            print(f"{ip_info['InstanceId']:<20} {ip_info['Public IP']:<20} {ip_info['Private IP']:<20}")
    else:
        print("No instances found.")
