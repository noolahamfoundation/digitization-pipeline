"""
Author: Parathan Thiyagalingam
Date: 2024-06-07
Description: A python script to upload files to the S3 bucket recursively.
Prerequisite:
1. Python 3
2. Pip
3. AWS Cli should be insalled
"""

import os
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from datetime import datetime, time

def upload_to_glacier_deep_archive(local_directory, bucket_name, s3_base_path='', log_file='upload_log.txt'):
    """
    Uploads files from a local directory to an S3 bucket with Glacier Deep Archive storage class,
    maintaining the folder structure. Resumes from the last uploaded file in case of interruption.
    Stops uploading if the current time is past 6:30 AM.
    :param local_directory: Path to the local directory
    :param bucket_name: Name of the S3 bucket
    :param s3_base_path: Base path in the S3 bucket where files should be uploaded
    :param log_file: Path to the log file that stores uploaded file paths
    """
    # Initialize S3 client
    s3 = boto3.client('s3')

    # Load the set of already uploaded files from the log file
    uploaded_files = set()
    if os.path.exists(log_file):
        with open(log_file, 'r') as f:
            uploaded_files = set(line.strip() for line in f)

    # Time to stop the script (6:30 AM)
    stop_time = time(6, 30)

    # Loop through all the files and directories in the local directory
    with open(log_file, 'a') as log:
        for root, dirs, files in os.walk(local_directory):
            for filename in files:
                # Check the current time
                current_time = datetime.now().time()
                if current_time > stop_time:
                    print(f'Current time {current_time} has passed the stop time of {stop_time}. Stopping.')
                    return

                # Construct the full local path
                local_path = os.path.join(root, filename)

                # Construct the relative path to maintain folder structure
                relative_path = os.path.relpath(local_path, local_directory)
                s3_path = os.path.join(s3_base_path, relative_path).replace("\\", "/")  # Use '/' for S3 paths

                # Check if the file is already uploaded
                if relative_path in uploaded_files:
                    print(f'Skipping already uploaded file: {local_path}')
                    continue

                print(f'Uploading {local_path} to s3://{bucket_name}/{s3_path} with DEEP_ARCHIVE storage class')

                try:
                    # Upload the file to S3 with Glacier Deep Archive storage class
                    s3.upload_file(local_path, bucket_name, s3_path, ExtraArgs={'StorageClass': 'DEEP_ARCHIVE'})
                    print(f'Successfully uploaded {local_path} to {s3_path} with DEEP_ARCHIVE storage class')

                    # Log the uploaded file
                    log.write(relative_path + '\n')
                    log.flush()  # Ensure the log is written to the file
                except FileNotFoundError:
                    print(f'The file was not found: {local_path}')
                except NoCredentialsError:
                    print('Credentials not available.')
                except PartialCredentialsError:
                    print('Incomplete credentials provided.')

# Usage
local_directory = '/path/to/local/directory'  # Change this to your local directory path
bucket_name = 'your-s3-bucket-name'           # Change this to your S3 bucket name
s3_base_path = '/'                            # Optional: Change this to your S3 base path if needed
log_file = 'upload_log.txt'                   # Optional: Change this to your log file path if needed

upload_to_glacier_deep_archive(local_directory, bucket_name, s3_base_path, log_file)