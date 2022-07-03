import boto3
import b3q


class ResourceGroupsTaggingApi:

    @staticmethod
    def get_resources_by_tag(name: str, tag: str, region: str):

        client = boto3.client("resourcegroupstaggingapi", region_name=region)
        response = b3q.get(
            client.get_resources,
            arguments={"TagFilters": [{"Key": name, "Values": [tag]}]},
            attribute="ResourceTagMappingList"
        )
        return list(response)
