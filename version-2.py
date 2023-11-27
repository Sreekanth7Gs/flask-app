import boto3
import paramiko
import os

def lambda_handler(event, context):
    ec2_instance_id = 'i-0ecbcfbdc38f5ed95'
    ec2_key_pair = 'Practice.pem'
    ec2_username = 'ec2-user'
    ec2_private_key_path = '/Downloads/Practice.pem'

    s3_bucket_name = 'lambda-sree-bucket3'

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    private_key = paramiko.RSAKey(filename=ec2_private_key_path)

    try:
        ssh_client.connect(ec2_instance_id, username=ec2_username, pkey=private_key)

        upload_files_to_s3(ssh_client, '/home/ec2-user/aws_lambda_boto3/uploads/', s3_bucket_name)

        delete_files_on_ec2(ssh_client, '/home/ec2-user/aws_lambda_boto3/uploads/')

    finally:
        ssh_client.close()

def upload_files_to_s3(ssh_client, local_path, s3_bucket_name):
    s3_client = boto3.client('s3')

    files_to_upload = [f for f in os.listdir(local_path) if os.path.isfile(os.path.join(local_path, f))]

    for file_name in files_to_upload:
        local_file_path = os.path.join(local_path, file_name)
        s3_object_key = file_name 

        s3_client.upload_file(local_file_path, s3_bucket_name, s3_object_key)

def delete_files_on_ec2(ssh_client, local_path):
    stdin, stdout, stderr = ssh_client.exec_command(f'rm -rf {local_path}*')
    print(stdout.read().decode())
    pass