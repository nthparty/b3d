import boto3


AWS_REGION = "us-east-1"
EC2_CLIENT = boto3.client("ec2", region_name=AWS_REGION)