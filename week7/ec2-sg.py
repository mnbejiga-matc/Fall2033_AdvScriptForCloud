#!/usr/bin/env python3
import boto3
import argparse

ec2_client = boto3.client('ec2')

def list_security_groups():
    response = ec2_client.describe_security_groups()
    return response['SecurityGroups']

def find_openned_security_group(group_name):
    security_groups = list_security_groups()

    for sg in security_groups:
        if group_name and sg['GroupName'] != group_name:
            continue

        is_open_to_public = False
        allowed_ranges = []

        print(f"Securityy Group: {sg['GroupName']}")
        for rule in sg['IpPermissions']:
            for range in rule.get('IpRanges', []):
                cidr_ip = range['CidrIp', 'N/A']
                from_port = rule['FromPort']
                to_port = rule['ToPort']
                if cidr_ip == '0.0.0.0/0':
                    is_open_to_public = True
                else:
                    allowed_ranges.append(f"{from_port}-{to_port}: {cidr_ip}")
        
        if not is_open_to_public:
            if allowed_ranges:
                print("allowed Ranges:")
                for  allowed_range in allowed_ranges:
                    print(allowed_range)
            else:
                print("WARNING: Open to the public internet!")
    print()

def main():
    parser = argparse.ArgumentParser(description="Check the openness of AWS security groups")
    parser.add_argument('-s', '--security-group', help="Name of the security group to check")
    args = parser.parse_args()

    if args.security_group:
        find_openned_security_group(args.security_group)
    else:
        find_openned_security_group(None)

        
if __name__ == "__main__":
    main()
