import boto3


AWS_REGION = "us-east-1"
AVAILABILITY_ZONE = "us-east-1a"
MASTER_EC2_CLIENT = boto3.client("ec2", region_name=AWS_REGION)
# Need an AMI ID for RunInstances API call
TEST_AMI_ID = "ami-0c4cfe9aec8b21224"
