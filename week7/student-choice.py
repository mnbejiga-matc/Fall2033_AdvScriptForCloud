#!/usr/bin/env python3

import boto3
import csv

#  Boto3 Config client function initialize
config_client = boto3.client('config')

# Thsi function will list non-compliant AWS config rules 
def rules_for_non_comliant_list():
    try:
        response = config_client.describe_compliance_by_config_rule()
        non_compliant_rules = [rule for rule in response['ComplianceByConfigRules'] if rule['ComplianceType'] != 'COMPLIANT']
        return non_compliant_rules
    except Exception as e:
        print(f"Error listing non-compliant AWS Config rules: {str(e)}")
        return []

# This function will write the audit results to a CSV file
def write_audit_results(data, filename):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['ConfigRuleName', 'ResourceType', 'ResourceId', 'ComplianceType']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for entry in data:
            writer.writerow({'ConfigRuleName': entry['ConfigRuleName'], 'ResourceType': entry['ResourceType'], 'ResourceId': entry['ResourceId'], 'ComplianceType': entry['ComplianceType']})

#this is main function
def main():
    non_compliant_rules = rules_for_non_comliant_list()
    write_audit_results(non_compliant_rules, 'export-audit.csv')
    print("Config audit result written")

# Main function called here
if __name__ == "__main__":
    main()
    
    

   
    