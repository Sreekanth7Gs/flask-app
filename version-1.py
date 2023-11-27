import boto3
import os

def upload_to_s3(local_file_path, s3_bucket_name):
    try:
        s3 = boto3.client('s3')
        file_name = os.path.basename(local_file_path)
        s3.upload_file(local_file_path, s3_bucket_name, file_name)
        print(f"File {file_name} is Uploaded to s3 bucket {s3_bucket_name}")
        os.remove(local_file_path)
        print(f"File {local_file_path} is deleted..")
        
    except Exception as e:
        print(f"Error: {e} ")

def check_and_upload_files(uploads_directory, s3_bucket_name):
    for filename in os.listdir(uploads_directory):
        allowed_extensions = (".txt", ".png", ".pdf")
        if filename.endswith(allowed_extensions):  
            local_file_path = os.path.join(uploads_directory, filename)
            upload_to_s3(local_file_path, s3_bucket_name)
           
if __name__ == "__main__":
    upload_directory = 'uploads'
    s3_bucket = "lambda-sree-bucket"
    check_and_upload_files(upload_directory, s3_bucket)
