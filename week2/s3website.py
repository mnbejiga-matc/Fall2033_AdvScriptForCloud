#!/usr/bin/env python3

import boto3.json


s3_client = boto3.client('s3')

bucket_name = "cmalin1-script2-week2-f23"

bucket_response = s3_client.create_bucket(Bucket=bucket_name)

bucket_policy = {
    'Version': '2012-10-17',
    'Statement': [{
        'Sid': 'AddPerm',
        'Effect': 'Allow',
        'Principal': '*',
        'Action': ['s3:GetObject'],
        'Resource': "arn:aws:s3:::%s/*" % bucket_name
    }]
}
bucket_policy_string = json.dumps(bucket_policy)

bucket_policy_response = s3_client.put_bucket_policy (
    Bucket=bucket_name,
    Policy=bucket_policy_string
)

put_bucket_response = client.put_bucket_website(
    Bucket=bucket_name,
    WebsiteConfiguration={
    'ErrorDocument': {'Key': 'error.html'},
    'IndexDocument': {'Suffix': 'index.html'},
    }
)

