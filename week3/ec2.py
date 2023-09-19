#!/usr/bin/env python3
import boto3
import json

client = boto3.client('ec2')

def Get_Image(ec2client):
    image_response = client.describe_images(
        Filters=[
            {
                'Name': 'description',
                'Values': ['Amazon Linux 2 AMI*']
            },
            {
                'Name': 'architecture',
                'Values': ['x86_64']
            },
            {

                'Name': 'owner-alias',
                'Values': ['amazon']
            }
        ]
    )
    return image_response['Images'][0]['ImageId']
def Create_EC2(AMI, ec2client):

    DRYRUN = False

    response = client.run_instances(
        ImageId=AMI,
        InstanceType='t2.micro',
        MaxCount=1,
        MinCount=1,
        DryRun=DRYRUN
    )
    return response['Instances'][0]['InstanceId']

def main():
    client = boto3.client('ec2')
    AmI = Get_Image(client)

    instance_id = Create_EC2(AMI, client)

    
    ec2 = boto3.resource('ec2')
    instance = ec2.Instance(instance_id)

    print(f"Before Waiting: Instance is {instance.state['Name']}")
    instance.wait_until_running()
    instance = ec2.Instance.load()
    print(f"After Waiting: Instance is {instance.state['Name']}")
    instance.terminate()
    print(f"Before Terminated: Instance is {instance.state['Name']}")
    instance.wait_until_terminated()
    instance = ec2.Instance.load()
    print(f"After Terminated: Instance is {instance.state['Name']}")

    #print(instance.instance_id)

    if __name__ == '__main__':
        main()
