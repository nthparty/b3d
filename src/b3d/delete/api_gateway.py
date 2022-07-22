from b3d.delete import Service
from b3d import aws
from b3d.utils import log_msg
from typing import List, Dict
import boto3


class APIGateway(Service):
    """
    Container class for API Gateway resource deletion procedures
    """

    @staticmethod
    def service_type() -> str:
        return "apigateway"

    @staticmethod
    def _delete_base_path_mappings(
            cl: boto3.client, rest_api_id: str, stage_name: [str, None] = None, dry: bool = False
    ) -> List[Dict]:
        """
        Remove all base path mappings associated with either a rest api ID or both a
        rest api ID and some stage name
        """

        resps = []

        # Query all existing base path mappings and filter according to input arguments above
        for bpm in aws.api_gateway.get_base_path_mappings(cl, rest_api_id, stage_name=stage_name):
            resps.append(
                log_msg.log_msg_destroy(
                    resource_type="base-path-mapping",
                    resource_id=bpm.get("base_path"),
                    resp=aws.api_gateway.delete_base_path_mapping(
                        cl, domain_name=bpm.get("domain"), base_path=bpm.get("base_path"), dry=dry
                    )
                )
            )

        return resps

    class RestApi(Service.Resource):

        @staticmethod
        def resource_type() -> str:
            return "restapis"

        @staticmethod
        def query(cl: boto3.client, resource_arn: str) -> bool:
            return aws.api_gateway.get_rest_api(
                cl, APIGateway.RestApi.extract_resource_id_from_arn(resource_arn)
            ) is not None

        @staticmethod
        def destroy(arn: str, region: str, dry: bool = True) -> List[Dict]:

            resps = []
            cl = boto3.client("apigateway", region_name=region)
            api_id = APIGateway.RestApi.extract_resource_id_from_arn(arn)

            if not APIGateway.RestApi.query(cl, arn):
                return resps

            # Delete all base path mappings associated with this rest api
            resps.extend(APIGateway._delete_base_path_mappings(cl, api_id, dry=dry))

            # Delete this rest api
            resps.append(
                log_msg.log_msg_destroy(
                    resource_type="rest-api",
                    resource_id=api_id,
                    resp=aws.api_gateway.delete_rest_api(
                        cl, api_id, dry
                    )
                )
            )

            return resps

    class UsagePlan(Service.Resource):

        @staticmethod
        def resource_type() -> str:
            return "usageplans"

        @staticmethod
        def query(cl: boto3.client, resource_arn: str) -> bool:
            return aws.api_gateway.get_usage_plan(
                cl, APIGateway.UsagePlan.extract_resource_id_from_arn(resource_arn)
            ) is not None

        @staticmethod
        def _delete_stages(cl: boto3.client, usage_plan_id: str, dry: bool):

            resps = []

            for api_stage in aws.api_gateway.get_usage_plan(cl, usage_plan_id).get("apiStages", []):

                # Delete all base path mappings associated with this stage
                resps.extend(
                    APIGateway._delete_base_path_mappings(
                        cl, rest_api_id=api_stage.get("apiId"), stage_name=api_stage.get("stage"), dry=dry
                    )
                )

                # Delete this stage
                resps.append(
                    log_msg.log_msg_destroy(
                        resource_type="api-stage",
                        resource_id=api_stage.get("stage"),
                        resp=aws.api_gateway.delete_stage(
                            cl, api_stage.get("apiId"), api_stage.get("stage"), dry
                        )
                    )
                )

            return resps

        @staticmethod
        def destroy(arn: str, region: str, dry: bool = True) -> List[Dict]:

            resps = []
            cl = boto3.client("apigateway", region_name=region)
            usage_plan_id = APIGateway.UsagePlan.extract_resource_id_from_arn(arn)

            if not APIGateway.UsagePlan.query(cl, arn):
                return resps

            # Delete all stages associated with this usage plan
            resps.extend(APIGateway.UsagePlan._delete_stages(cl, usage_plan_id, dry))

            resps.append(
                log_msg.log_msg_destroy(
                    resource_type="usage-plan",
                    resource_id=usage_plan_id,
                    resp=aws.api_gateway.delete_usage_plan(cl, usage_plan_id, dry)
                )
            )

            return resps

    class Stage(Service.Resource):
        """
        TODO: This isn't necessary for PoC version of repository, since the UsagePlan resource
            deletes all associated stages. Will want to fill this out going forward though for
            the sake of completeness
        """

        @staticmethod
        def resource_type() -> str:
            return "stages"

        @staticmethod
        def query(cl: boto3.client, resource_arn: str) -> bool:
            return True

        @staticmethod
        def destroy(arn: str, region: str, dry: bool = True) -> List[Dict]:
            return []

    class ApiKey(Service.Resource):

        @staticmethod
        def resource_type() -> str:
            return "apikeys"

        @staticmethod
        def query(cl: boto3.client, resource_arn: str) -> bool:
            return aws.api_gateway.get_api_key(
                cl, APIGateway.ApiKey.extract_resource_id_from_arn(resource_arn)
            ) is not None

        @staticmethod
        def destroy(arn: str, region: str, dry: bool = True) -> List[Dict]:

            cl = boto3.client("apigateway", region_name=region)
            api_key_id = APIGateway.ApiKey.extract_resource_id_from_arn(arn)

            if not APIGateway.ApiKey.query(cl, arn):
                return []

            return [
                log_msg.log_msg_destroy(
                    resource_type="api-key",
                    resource_id=api_key_id,
                    resp=aws.api_gateway.delete_api_key(cl, api_key_id, dry=dry)
                )
            ]
