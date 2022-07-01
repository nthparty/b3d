import boto3
from rich import print
import click


def delete_resources(name, tag, region, dry_run=True):
    """
    Delete all resources with the given tag.
    """
    resources = _get_all_resources(name, tag, region)
    _delete_all_resources(resources, dry_run)
    _delete_policies(name, tag, dry_run)
    _delete_roles(name, tag, dry_run)
    _delete_s3_buckets(name, tag, dry_run)
    _delete_lamdba(name, tag, dry_run)
    _delete_volumes(name, tag, dry_run)
    _delete_ec2_instances(name, tag, dry_run)


def _get_all_resources(name, tag, region):
    """
    Get all resources with the given tag.
    """
    client = boto3.client('resourcegroupstaggingapi', region_name=region)
    response = client.get_resources(TagFilters=[{'Key': name, 'Values': [tag]}])
    results = [response['ResourceTagMappingList']]
    while response['PaginationToken']:
        response = client.get_resources(PaginationToken=response['PaginationToken'],
                                        TagFilters=[{'Key': name, 'Values': [tag]}])
        results += response['ResourceTagMappingList']
    return results


def _delete_all_resources(resources, dry_run=True):
    """
    Delete all resources in the given list.
    """
    for resource in resources:
        service = resource['ResourceARN'].split(':')[1]
        if not dry_run:
            delete[service](resource['ResourceARN'])
            print(f"Deleted {service} {resource['ResourceARN']}")
        else:
            print(f"Found {service} resource {resource['ResourceARN']} for deletion")


def _delete_volumes(name, tag, dry_run=True):
    """
    Delete all EBS volumes with the given tag.
    """
    client = boto3.client('ec2')
    response = client.describe_volumes()
    for volume in response['Volumes']:
        for t in volume['Tags']:
            if t['Key'] == name and t['Value'] == tag:
                if not dry_run:
                    client.delete_volume(VolumeId=volume['VolumeId'])
                    print(f"Deleted EBS Volume {volume['VolumeId']}")
                else:
                    print(f"Found EBS Volume {volume['VolumeId']} for deletion")


def _delete_ec2_instances(name, tag, dry_run=True):
    """
    Delete all EC2 instances with the given tag.
    """
    client = boto3.client('ec2')
    response = client.describe_instances()
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            for t in instance['Tags']:
                if t['Key'] == name and t['Value'] == tag:
                    if not dry_run:
                        client.terminate_instances(InstanceIds=[instance['InstanceId']])
                        print(f"Terminated EC2 Instance {instance['InstanceId']}")
                    else:
                        print(f"Found EC2 Instance {instance['InstanceId']} for termination")


def _delete_s3_buckets(name, tag, dry_run=True):
    """
    Delete all S3 buckets with the given tag.
    """
    client = boto3.client('s3')
    response = client.list_buckets()
    for bucket in response['Buckets']:
        for t in bucket['Tags']:
            if t['Key'] == name and t['Value'] == tag:
                if not dry_run:
                    client.delete_bucket(Bucket=bucket['Name'])
                    print(f"Deleted S3 Bucket {bucket['Name']}")
                else:
                    print(f"Found S3 Bucket {bucket['Name']} for deletion")


def _delete_policies(name, tag, dry_run=True):
    """
    Delete all IAM policies with the given tag.
    """
    client = boto3.client('iam')
    response = client.list_policies()
    for policy in response['Policies']:
        for t in policy['Tags']:
            if t['Key'] == name and t['Value'] == tag:
                if not dry_run:
                    client.delete_policy(PolicyArn=policy['Arn'])
                    print(f"Deleted IAM Policy {policy['Arn']}")
                else:
                    print(f"Found IAM Policy {policy['Arn']} for deletion")


def _delete_roles(name, tag, dry_run=True):
    """
    Delete all IAM roles with the given tag.
    """
    client = boto3.client('iam')
    response = client.list_roles()

    for role in response['Roles']:
        for t in role['Tags']:
            if t['Key'] == name and t['Value'] == tag:
                if not dry_run:
                    client.delete_role(RoleName=role['RoleName'])
                    print(f"Deleted IAM Role {role['RoleName']}")
                else:
                    print(f"Found IAM Role {role['RoleName']} for deletion")


def _delete_lamdba(name, tag, dry_run=True):
    """
    Delete all Lambda functions with the given tag.
    """
    client = boto3.client('lambda')
    response = client.list_functions()
    for function in response['Functions']:
        for t in function['Tags']:
            if t['Key'] == name and t['Value'] == tag:
                if not dry_run:
                    client.delete_function(FunctionName=function['FunctionName'])
                    print(f"Deleted Lambda Function {function['FunctionName']}")
                else:
                    print(f"Found Lambda Function {function['FunctionName']} for deletion")


def _delete_s3_by_arn(arn):
    """
    Delete S3 bucket by ARN.
    """
    client = boto3.client('s3')
    client.delete_bucket(Bucket=arn)
    print(f"Deleted S3 bucket {arn}")


def _delete_volume_by_arn(arn):
    """
    Delete EBS volume by ARN.
    """
    client = boto3.client('ec2')
    client.delete_volume(VolumeId=arn)
    print(f"Deleted EBS volume {arn}")


def _delete_ec2_resources(arn):
    """
    Delete EC2 instance by ARN.
    """
    client = boto3.client('ec2')
    client.terminate_instances(InstanceIds=[arn])
    print(f"Deleted EC2 instance {arn}")


def _delete_policy_by_arn(arn):
    """
    Delete IAM policy by ARN.
    """
    client = boto3.client('iam')
    client.delete_policy(PolicyArn=arn)
    print(f"Deleted IAM policy {arn}")


def _delete_iam_resources(arn):
    """
    Delete IAM resources by ARN.
    """
    client = boto3.client('iam')
    client.delete_role(RoleName=arn)
    print(f"Deleted IAM role {arn}")


def _delete_lambda_by_arn(arn):
    """
    Delete Lambda function by ARN.
    """
    client = boto3.client('lambda')
    client.delete_function(FunctionName=arn)
    print(f"Deleted Lambda function {arn}")


delete = {
    's3': _delete_s3_by_arn,
    'iam': _delete_policy_by_arn,
    'ec2': _delete_ec2_resources,
    'ebs': _delete_volume_by_arn,
    'lambda': _delete_lambda_by_arn
}
