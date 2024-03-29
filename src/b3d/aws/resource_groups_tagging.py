"""
ResourceGroupsTaggingApi helper functions
"""
import boto3
import b3q


def get_resources_by_tag(cl: boto3.client, tag_key: str, tag_value: str):
    """
    Retrieve the ARNs of all resources associated with some tag pair
    """

    response = b3q.get(
        cl.get_resources,
        arguments={"TagFilters": [{"Key": tag_key, "Values": [tag_value]}]},
        attribute="ResourceTagMappingList"
    )
    return [r["ResourceARN"] for r in response]
