from b3d.delete import Service
from b3d import aws
from b3d.utils import log_msg
from typing import List, Dict
import boto3


class S3(Service):
    """
    Container class for S3 resource deletion procedures
    """

    @staticmethod
    def service_type() -> str:
        return "s3"

    class Bucket(Service.Resource):

        @staticmethod
        def extract_resource_id_from_arn(arn: str) -> str:
            return arn.split(":")[-1]

        @staticmethod
        def resource_type() -> str:
            return "bucket"

        @staticmethod
        def query(cl: boto3.client, resource_arn: str) -> bool:
            return aws.s3.get_bucket(
                cl, S3.Bucket.extract_resource_id_from_arn(resource_arn)
            ) is not None

        @staticmethod
        def _delete_objects(cl: boto3.client, bucket_name: str, dry: bool) -> dict:

            objects = aws.s3.get_objects_in_bucket(cl, bucket_name)
            return log_msg.log_msg_destroy(
                resource_type="objects",
                resource_id=" | ".join(objects),
                resp=aws.s3.delete_objects(cl, bucket_name, objects, dry)
            )

        @staticmethod
        def destroy(arn: str, region: str, dry: bool = True) -> List[Dict]:

            resps = []
            cl = boto3.client("s3", region_name=region)
            bucket_name = S3.Bucket.extract_resource_id_from_arn(arn)

            if not S3.Bucket.query(cl, arn):
                return resps

            # Remove all objects stored in this bucket
            resps.append(S3.Bucket._delete_objects(cl, bucket_name, dry))

            # Delete this bucket
            resps.append(
                log_msg.log_msg_destroy(
                    resource_type="bucket",
                    resource_id=bucket_name,
                    resp=aws.s3.delete_bucket(cl, bucket_name, dry)
                )
            )

            return resps
