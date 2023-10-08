#!/usr/bin/env python3

import boto3
import ec2,sns

DRYRUN = False

sts_client = boto3.client("sts")
account_id = sts_client.get_caller_identity()["Account"]
ec2_client = boto3.client('ec2')
image = ec2.Get_Image(ec2_client)
instance = ec2.Create_EC2(image,ec2_client)
cw_client = boto3.client('cloudwatch')

topicARN = sns.CreateSNSTopic('MesfinAssignmentTopic2')
subscriptionARN = sns.SubscribeEmail(topicARN,'mnbejiga@madisoncollege.edu')

response = cw_client.put_metric_alarm(
    AlarmName='Web_Server_HIGH_CPU_Utilizatio',
    ComparisonOperator='GreaterThanOrEqualToThreshold',
    EvaluationPeriods=2,
    MetricName='CPUUtilization',
    Namespace='AWS/EC2',
    Period=300,
    Statistic='Average',
    Threshold=70.0,
    ActionsEnabled=True,
    AlarmActions=[
        f'arn:aws:swf:us-east-1:{account_id}:action/actions/AWS_EC2.InstanceId.Stop/1.0',
        f'arn:aws:sns:us-east-1:{account_id}:MesfinAssignmentTopic2'
    ],
    AlarmDescription='Alarm when server CPU is higher than 70%',
    Dimensions=[
        {
            'Name': 'InstanceId',
            'Value': instance
        },
    ]
)




    