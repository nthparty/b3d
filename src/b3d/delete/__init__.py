import abc


class Service(abc.ABC):

    @staticmethod
    @abc.abstractmethod
    def service_type() -> str:
        """
        Return the name of this service type.
        """
        pass

    class Resource(abc.ABC):

        @staticmethod
        @abc.abstractmethod
        def extract_resource_id_from_arn(arn: str) -> str:
            pass

        @staticmethod
        @abc.abstractmethod
        def resource_type() -> str:
            """
            Return the name of this resource type.
            """
            pass

        @staticmethod
        @abc.abstractmethod
        def destroy(arn: str, region: str, dry: bool = True):
            """
            Destroy the resource corresponding to this ARN.
            """
            pass
