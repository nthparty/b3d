import boto3
import b3q


def get_resources_by_tag(cl: boto3.client, name: str, tag: str):

    response = b3q.get(
        cl.get_resources,
        arguments={"TagFilters": [{"Key": name, "Values": [tag]}]},
        attribute="ResourceTagMappingList"
    )
    return [r["ResourceARN"] for r in response]
