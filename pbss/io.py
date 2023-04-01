import sys
from tqdm import tqdm
import io
from PIL import Image
import json
import boto3
import os
import boto3

"""
{
"aws_access_key_id": "${pbss_name}",
"aws_secret_access_key": "${key}",
"endpoint_url": "https://pbss.s8k.io"
}
"""
aws_credentials_file_ckpt="pbss_credentials.secret"
s3_bucket="xzeng"

with open(aws_credentials_file_ckpt) as file:
    s3_config = json.load(file)
s3_client = boto3.client("s3", **s3_config)

def parallel_upload(upload_file_list):
    # upload files to s3
    pool = multiprocessing.Pool(10)
    pool.map(upload_file, upload_file_list)
    pool.close()
    pool.join()

def upload_file(args):
    filename, target_file_name = args
    print('upload %s to s3://%s/%s'%(filename, s3_bucket, target_file_name))
    s3_client.upload_file(filename, s3_bucket, target_file_name)

def write_to_s3(save_pairs):
    save_dict, save_path = save_pairs
    with io.BytesIO() as buffer:
        torch.save(save_dict, buffer)
        buffer.seek(0)
        # s3_client = boto3.client("s3", **s3_config)
        s3_resource = boto3.resource("s3", **s3_config)
        bucket = s3_resource.Bucket(s3_bucket)
        if not bucket.creation_date:
            print('bucket not found!')
            raise ValueError
        s3_client.upload_fileobj(Bucket=s3_bucket, Key=save_path, Fileobj=buffer)
        print(f'Finish saving {save_path}')

def list_objects(s3_client, s3_bucket, prefix):
    # source: https://stackoverflow.com/a/59816089
    paginator = s3_client.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=s3_bucket, Prefix=prefix)
    keys = []
    for page in pages:
        for obj in page['Contents']:
            keys.append(obj['Key'])
    return keys
  
def _load_from_s3(s3_bucket, file_path, s3_client):
    for attempt in range(100):
        try:
            with io.BytesIO() as buffer:
                s3_client.download_fileobj(Bucket=s3_bucket, Key=file_path, Fileobj=buffer)
                # Read state dict from BytesIO buffer.
                buffer.seek(0)
                img = Image.open(buffer)
                img.load()
                img = img.convert("RGB") 
            return img.resize((512,512))
        except Exception:
            print(f'Loading checkpoint, attempt: {attempt}')
    raise ConnectionError(f'Unable to read checkpoints after {attempt}')
