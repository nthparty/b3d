import boto3


class IAM:

    @staticmethod
    def delete_policy_by_arn(cl: boto3.client, arn: str):
        pass

    @staticmethod
    def detach_policy_from_role(cl: boto3.client, policy_arn: str, role_arn: str):
        pass

    @staticmethod
    def delete_role(cl: boto3.client, arn: str):
        pass

    @staticmethod
    def detach_instance_profile_from_ec2_instance(cl: boto3.client, instance_profile_arn: str, instance_arn: str):
        pass
