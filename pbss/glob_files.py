import boto3
import botocore
from glob import glob
import json
s3_config = "pbss_credentials.secret"
s3_config = json.load(open(s3_config, 'r'))
# Set up S3 client
s3 = boto3.client('s3', **s3_config)

bucket = 'xzeng'
prefix = "data/t3d_data/gen_input/zekun_render_ts_0424"

paginator = s3.get_paginator('list_objects_v2')
page_iterator = paginator.paginate(Bucket=bucket, Prefix=prefix)

all_files = []
for page in page_iterator:
    for obj in page['Contents']:
        # do something with the object
        # print(obj['Key'])
        if obj['Key'].endswith('.png') or obj['Key'].endswith('.jpg'):
            all_files.append(obj["Key"])
print(len(all_files), all_files[0])
