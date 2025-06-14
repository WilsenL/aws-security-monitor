import boto3

# Membuat EC2 client untuk region Singapore
ec2 = boto3.client('ec2', region_name='us-east-1')

try:
    # Mengambil detail dari semua instans
    response = ec2.describe_instances()

    print("✅ Koneksi AWS berhasil! Berikut adalah instans EC2 Anda:")

    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            instance_type = instance['InstanceType']
            instance_state = instance['State']['Name']

            # Cari tag 'Name'
            instance_name = "Nama tidak ditemukan"
            if 'Tags' in instance:
                for tag in instance['Tags']:
                    if tag['Key'] == 'Name':
                        instance_name = tag['Value']

            print(f"  - Nama: {instance_name}, ID: {instance_id}, Tipe: {instance_type}, Status: {instance_state}")

except Exception as e:
    print(f"❌ Terjadi kesalahan: {e}")
    print("   Pastikan kredensial AWS Anda sudah diatur dengan benar sebagai environment variables.")