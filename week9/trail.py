#!/usr/bin/env python3

import boto3,s3enforce,json
import time



def CreateTrail(trial_name, bucket_name):
    trailclient = boto3.client('cloudtrail')
    try:
        response = trailclient.create_trail(S3BucketName=bucket_name,Name=trial_name)
        return response
    except trailclient.exceptions.TrailAlreadyExistsException as error:
        response = trailclient.start_logging(Name=trial_name)
        return response
    
def StartLogging(trial_name):
    trail = boto3.client('cloudtrail')
    response = trail.start_logging(Name=trial_name)
    return response

def StopLogging(trail_name):
    trail = boto3.client('cloudtrail')
    response = trail.stop_logging(Name=trail_name)
    return response

def GetTrailStatus(trail_name):
    trail = boto3.client('cloudtrail')
    try:
        response = trail.get_trail_status(Name=trail_name)
        
        return response['IsLogging']
    except trail.exceptions.TrailNotFoundException as error:
        print("That trail name does not exist")
    except:
        print("Some other error occurred")
    
def main():
    sts_client = boto3.client("sts")
    account_id = sts_client.get_caller_identity()["Account"]
    
    bucket_name = "mesfinb-cloud-trial-wk8"
    trail_name = "mesfinb-ct-week8"
    
    policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "AWSCloudTrailAclCheck20150319",
                "Effect": "Allow",
                "Principal": {"Service": "cloudtrail.amazonaws.com"},
                "Action": "s3:GetBucketAcl",
                "Resource": f"arn:aws:s3:::{bucket_name}"
            },
            {
                "Sid": "AWSCloudTrailWrite20150319",
                "Effect": "Allow",
                "Principal": {"Service": "cloudtrail.amazonaws.com"},
                "Action": "s3:PutObject",
                "Resource": f"arn:aws:s3:::{bucket_name}/AWSLogs/{account_id}/*",
                "Condition": {"StringEquals": {"s3:x-amz-acl": "bucket-owner-full-control"}}
            }
        ]
    }

    bucket_policy_response  = s3enforce.SetBucketPolicy(bucket_name,json.dumps(policy))
    response = CreateTrail(trail_name, bucket_name)
    stop_response = StopLogging(trail_name)
    time.sleep(5)
    if GetTrailStatus(trail_name):
        print("Trail is logging as expected")
    else:
        print(f"Trail is Not logging, something is wrong")
   
  
if __name__ == "__main__":
    main()