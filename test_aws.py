import boto3

ec2 = boto3.client('ec2', region_name='us-east-1')

try:
    # Test AWS Connection
    response = ec2.describe_instances()

    print("✅ AWS Connectiong Succeed! EC2 Instance Info:")

    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            instance_type = instance['InstanceType']
            instance_state = instance['State']['Name']
            # Get instance name from tags
            instance_name = "Name not found"
            if 'Tags' in instance:
                for tag in instance['Tags']:
                    if tag['Key'] == 'Name':
                        instance_name = tag['Value']

            print(
                f"  - Name: {instance_name}, ID: {instance_id}, Type: {instance_type}, State: {instance_state}")

except Exception as e:
    print(f"❌ Error: {e}")
