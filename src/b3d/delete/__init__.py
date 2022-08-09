"""
Abstract class definition for AWS resource delete procedures
"""
import abc
from typing import List, Dict
import boto3


class Service(abc.ABC):
    """
    Abstract container class for AWS resource delete procedures
    """

    @staticmethod
    @abc.abstractmethod
    def service_type() -> str:
        """
        Return the name of this service type.
        """

    class Resource(abc.ABC):
        """
        Abstract class for resource delete procedure
        """

        @staticmethod
        def extract_resource_id_from_arn(arn: str) -> str:
            """
            Extract resource ID from ARN string
            """
            return arn.split("/")[-1]

        @staticmethod
        @abc.abstractmethod
        def query(cl: boto3.client, resource_arn: str) -> bool:
            """
            Determine if this resource exists.
            """

        @staticmethod
        @abc.abstractmethod
        def resource_type() -> str:
            """
            Return the name of this resource type.
            """

        @staticmethod
        @abc.abstractmethod
        def destroy(arn: str, region: str, dry: bool = True) -> List[Dict]:
            """
            Destroy the resource corresponding to this ARN.
            """
