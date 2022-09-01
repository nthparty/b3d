"""
For each test function below, a tag pair and a list of atomic (simple) resource
targets are provided. These resources are constructed by terraform before being
deleted by b3d according to their tag. The output from b3d is then checked for
correctness
"""
import pytest
import tests.utils as utils


@pytest.fixture(
    params=[
        ["aws_api_gateway_rest_api.rest_api_simple"],
        ["aws_api_gateway_usage_plan.usage_plan_simple"],
        ["aws_api_gateway_api_key.api_key_simple"]
    ]
)
def targets_api_gateway_simple(request):
    """
    Return a list of API Gateway target resource(s) to be constructed & deleted by b3d
    """
    return request.param


def test_api_gateway_simple(generate_tag, targets_api_gateway_simple):
    utils.build_delete_evaluate(generate_tag, targets_api_gateway_simple)


@pytest.fixture(
    params=[
        ["aws_instance.instance_simple"],
        ["aws_security_group.security_group_simple"],
        ["aws_ebs_volume.volume_simple"]
    ]
)
def targets_ec2_simple(request):
    """
    Return a list of EC2 target resource(s) to be constructed & deleted by b3d
    """
    return request.param


def test_ec2_simple(generate_tag, targets_ec2_simple):
    utils.build_delete_evaluate(generate_tag, targets_ec2_simple)


@pytest.fixture(
    params=[
        ["aws_iam_user.user_simple"],
        ["aws_iam_policy.policy_simple"],
        ["aws_iam_role.role_simple"]
    ]
)
def targets_iam_simple(request):
    """
    Return a list of IAM target resource(s) to be constructed & deleted by b3d
    """
    return request.param


def test_iam_simple(generate_tag, targets_iam_simple):
    utils.build_delete_evaluate(generate_tag, targets_iam_simple)


@pytest.fixture(
    params=[
        ["aws_kms_key.kms_key_simple"]
    ]
)
def targets_kms_simple(request):
    """
    Return a list of KMS target resource(s) to be constructed & deleted by b3d
    """
    return request.param


def test_kms_simple(generate_tag, targets_kms_simple):
    utils.build_delete_evaluate(generate_tag, targets_kms_simple)


@pytest.fixture(
    params=[
        ["aws_lambda_function.lambda_function_simple"]
    ]
)
def targets_lambda_simple(request):
    """
    Return a list of Lambda target resource(s) to be constructed & deleted by b3d
    """
    return request.param


def test_lambda_simple(generate_tag, targets_lambda_simple):
    utils.build_delete_evaluate(generate_tag, targets_lambda_simple)


@pytest.fixture(
    params=[
        ["aws_s3_bucket.s3_bucket_simple"]
    ]
)
def targets_s3_simple(request):
    return request.param


def test_s3_simple(generate_tag, targets_s3_simple):
    utils.build_delete_evaluate(generate_tag, targets_s3_simple)


@pytest.fixture(
    params=[
        ["aws_ssm_parameter.ssm_parameter_simple"]
    ]
)
def targets_ssm_simple(request):
    return request.param


def test_ssm_simple(generate_tag, targets_ssm_simple):
    utils.build_delete_evaluate(generate_tag, targets_ssm_simple)


@pytest.fixture(
    params=[
        [
            "aws_api_gateway_rest_api.rest_api_simple",
            "aws_api_gateway_usage_plan.usage_plan_simple",
            "aws_api_gateway_api_key.api_key_simple",
            "aws_instance.instance_simple",
            "aws_security_group.security_group_simple",
            "aws_ebs_volume.volume_simple",
            "aws_iam_user.user_simple",
            "aws_iam_policy.policy_simple",
            "aws_iam_role.role_simple",
            "aws_kms_key.kms_key_simple",
            "aws_lambda_function.lambda_function_simple",
            "aws_s3_bucket.s3_bucket_simple",
            "aws_ssm_parameter.ssm_parameter_simple"
        ]
    ]
)
def targets_all_simple(request):
    return request.param


def test_all_simple(generate_tag, targets_all_simple):
    utils.build_delete_evaluate(generate_tag, targets_all_simple)
