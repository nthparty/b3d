from b3d.delete import Service
from b3d import aws
from b3d.utils import log_msg
from typing import List, Dict
import boto3


class KMS(Service):
    """
    Container class for KMS resource deletion procedures
    """

    @staticmethod
    def service_type() -> str:
        return "kms"

    class Key(Service.Resource):

        @staticmethod
        def resource_type() -> str:
            return "key"

        @staticmethod
        def query(cl: boto3.client, resource_arn: str) -> bool:

            key_data = aws.kms.get_key(
                cl, KMS.Key.extract_resource_id_from_arn(resource_arn)
            )

            if key_data is None:
                return False

            return key_data["KeyMetadata"].get("KeyState") != "PendingDeletion"

        @staticmethod
        def destroy(arn: str, region: str, dry: bool = True) -> List[Dict]:

            resps = []
            cl = boto3.client("kms", region_name=region)
            key_id = KMS.Key.extract_resource_id_from_arn(arn)

            if not KMS.Key.query(cl, arn):
                return resps

            # Disable this key
            resps.append(
                log_msg.log_msg_disable(
                    resource_type="key",
                    resource_id=key_id,
                    resp=aws.kms.disable_key(cl, key_id, dry)
                )
            )

            # Schedule key for deletion
            resps.append(
                log_msg.log_msg_destroy(
                    resource_type="key",
                    resource_id=key_id,
                    resp=aws.kms.schedule_key_deletion(cl, key_id, dry)
                )
            )

            return resps
