#!/usr/bin/env python3

import boto3
import datetime
import pytz
import botocore

iam_client = boto3.client('iam')


def list_roles_created():
    roles = iam_client.list_roles()
    filtered_roles = []

    for role in roles['Roles']:
        somedate = role['CreateDate']
        if somedate > (pytz.utc.localize(datetime.datetime.utcnow())-datetime.timedelta(days=90)): 
            filtered_roles.append(role)

    return filtered_roles

def list_Role_policies(role_name):
    try:
        attached_policies = iam_client.list_attached_role_policies(RoleName=role_name)['AttachedPolicies']
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'AccessDenied':
            attached_policies = []
        else:
            raise
    
    return attached_policies
     
   
if __name__ == "__main__":

    roles = list_roles_created()
    
    for role in roles:
        role_name = role['RoleName']
        somedate = role['CreateDate']

        print(f"Role {role_name} -- Created: {somedate}")

        attached_policies = list_Role_policies(role_name)
        
        for policy in attached_policies:
            print(f"... has managed policy name: {policy['PolicyName']}")
        
        print()
    




