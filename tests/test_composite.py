"""
For each test function below, a tag pair and a list of composite resource
targets are provided. These resources are constructed by terraform before being
deleted by b3d according to their tag. The output from b3d is then checked for
correctness
"""
import pytest
import tests.utils as utils


@pytest.fixture(
    params=[
        ([
            "aws_api_gateway_rest_api.rest_api_composite",
            "aws_api_gateway_method.rest_api_composite_method_options",
            "aws_api_gateway_method_response.rest_api_composite_method_response_options",
            "aws_api_gateway_integration.rest_api_composite_integration_options",
            "aws_api_gateway_integration_response.response_200_options",
            "aws_api_gateway_deployment.rest_api_composite_deployment",
            "aws_api_gateway_usage_plan.usage_plan_composite",
            "aws_api_gateway_api_key.api_key_composite",
            "aws_api_gateway_usage_plan_key.usage_plan_key_composite"
        ], 3)
    ]
)
def targets_api_gateway_composite(request):
    """
    Return a list of API Gateway target resource(s) to be constructed & deleted by b3d
    """
    return request.param


def test_api_gateway_composite(generate_tag, targets_api_gateway_composite):
    utils.build_delete_evaluate(
        generate_tag, targets_api_gateway_composite[0], targets_api_gateway_composite[1]
    )


@pytest.fixture(
    params=[
        ([
            "aws_instance.instance_composite",
            "aws_ebs_volume.volume_composite",
            "aws_security_group.security_group_composite",
            "aws_volume_attachment.volume_composite_attach"
        ], 3)
    ]
)
def targets_ec2_composite(request):
    """
    Return a list of EC2 target resource(s) to be constructed & deleted by b3d
    """
    return request.param


def test_ec2_composite(generate_tag, targets_ec2_composite):
    utils.build_delete_evaluate(
        generate_tag, targets_ec2_composite[0], targets_ec2_composite[1]
    )


@pytest.fixture(
    params=[
        [
            "aws_iam_policy.user_composite_permissions_boundary_policy",
            "aws_iam_user.user_composite",
            "aws_iam_access_key.user_composite_access_key",
            "aws_iam_user_policy.user_composite_policy"
        ]
    ]
)
def targets_iam_composite(request):
    return request.param


def test_iam_composite(generate_tag, targets_iam_composite):
    utils.build_delete_evaluate(
        generate_tag, targets_iam_composite
    )
