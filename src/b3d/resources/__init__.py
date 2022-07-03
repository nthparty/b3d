import abc


class Service(abc.ABC):

    @staticmethod
    @abc.abstractmethod
    def service_type():
        pass

    class Resource(abc.ABC):

        @staticmethod
        @abc.abstractmethod
        def resource_type():
            pass

        @staticmethod
        @abc.abstractmethod
        def query(arn: str):
            """
            Determine if a resource with this ARN exists.
            """
            pass

        @staticmethod
        @abc.abstractmethod
        def destroy(arn: str, name: str, tag: str, region: str):
            """
            Destroy the resource corresponding to this ARN, if it exists.
            """
            pass
