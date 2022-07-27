import boto3
from b3d import aws, utils
from typing import Iterator


DELETE_PROTOCOL_OBJECT_MAP = utils.build_resource_map("b3d.delete")


def _get_all_resources_with_tag(tag_key: str, tag_value: str, region: str):

    ret = []

    resource_groups_tagging_client = boto3.client("resourcegroupstaggingapi", region_name=region)
    # Retrieve ARNs of all objects with the supplied name/tag pair using the ResourceGroupsTaggingApi.
    # Note that this API does not support *all* AWS resource types, so some manual ARN querying is
    # performed below.
    ret.extend(
        aws.resource_groups_tagging.get_resources_by_tag(
            resource_groups_tagging_client, tag_key, tag_value
        )
    )

    iam_client = boto3.client("iam", region_name=region)
    # Retrieve ARNs of all IAM Users with supplied key/value tag pair
    ret.extend(
        aws.iam.get_all_user_arns_with_tags(iam_client, [(tag_key, tag_value)])
    )
    # Retrieve ARNs of all IAM Roles with supplied key/value tag pair
    ret.extend(
        aws.iam.get_all_role_arns_with_tags(iam_client, [(tag_key, tag_value)])
    )
    # Retrieve ARNs of all IAM Policies with supplied key/value tag pair
    ret.extend(
        aws.iam.get_all_policy_arns_with_tags(iam_client, [(tag_key, tag_value)])
    )

    return ret


def _parse_api_gateway_arn(arn: str):
    """
    Custom parsing rules for API Gateway ARNs
    """

    splt = arn.split(":")
    resource_path = splt[-1].split("/")

    if len(resource_path) > 3 and resource_path[3] == "stages":
        # Form /restapis/<api_id>/stages/<stage_name>
        return "apigateway", "stages"
    else:
        # Form /<resource-type>/<resource_id>
        return "apigateway", resource_path[1]


def _parse_arn(arn: str):
    """
    Parse an ARN with the following form:
    'arn:aws:<SERVICE>:<REGION>:<ACCT_ID>:<RESOURCE_TYPE>/<RESOURCE_ID>'
    and return (<SERVICE>, <RESOURCE_TYPE>) tuples for each ARN.
    """

    splt = arn.split(":")

    # API Gateway ARNs have at least one corner case
    if splt[2] == "apigateway":
        return _parse_api_gateway_arn(arn)

    if splt[2] == "s3":
        # The ResourceGroupsTaggingApi only supports S3 buckets and we
        # don't support a manual search-object-with-tag process for other
        # S3 objects at this time
        return "s3", "bucket"

    if splt[2] == "lambda":
        return "lambda", splt[-2]

    return splt[2], splt[-1].split("/")[0]


def _map_arn(arn: str):
    """
    Map an ARN to its corresponding entry in DELETE_PROTOCOL_OBJECT_MAP. If it has no
    corresponding entry (i.e. - this library doesn't currently support that resource
    type), then the UnsupportedResource delete object is returned.
    """

    parsed_arn = _parse_arn(arn)
    try:
        return DELETE_PROTOCOL_OBJECT_MAP[parsed_arn[0]][parsed_arn[1]]
    except KeyError:
        return DELETE_PROTOCOL_OBJECT_MAP["unsupported-service"]["unsupported-resource"]


def _map_arns(arns: list) -> zip:
    """
    Map each ARN to its corresponding delete protocol object.
    """

    mapped_arns = [_map_arn(arn) for arn in arns]
    return zip(arns, mapped_arns)


def delete_resources(tag_key: str, tag_value: str, region: str = "us-east-1", dry=True) -> Iterator[list]:

    # Retrieve ARNs of all objects with the supplied name/tag pair
    resource_arns = _get_all_resources_with_tag(tag_key, tag_value, region)

    # Map each ARN to it's corresponding delete object
    mapped_arns = _map_arns(resource_arns)

    # For each resource, detach it from all dependent objects, delete it, and produce a report
    # of all performed actions, whether they were successful, and error messages for any actions
    # that were unsuccessful.
    for arn, obj in mapped_arns:
        yield obj.destroy(arn, region, dry)
