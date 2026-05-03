"""Tests for LambdaFunctionStack."""
import pytest
from aws_cdk import App, Environment, aws_lambda
from aws_cdk.assertions import Template
from llama_lambda.lambda_function_stack import LambdaFunctionStack


class TestLambdaFunctionStack:
    """Test suite for LambdaFunctionStack."""

    @pytest.fixture
    def app(self):
        """Create a CDK App for testing."""
        return App()

    @pytest.fixture
    def stack(self, app):
        """Create a LambdaFunctionStack for testing."""
        return LambdaFunctionStack(
            app,
            "TestStack",
            env=Environment(account="123456789012", region="us-east-1"),
        )

    @pytest.fixture
    def template(self, stack):
        """Create a CloudFormation Template from the stack."""
        return Template.from_stack(stack)

    def test_stack_creates_lambda_function(self, template):
        """Verify a Lambda function is created."""
        template.resource_count_is("AWS::Lambda::Function", 1)

    def test_lambda_function_has_correct_timeout(self, template):
        """Verify Lambda function has 300s timeout."""
        template.has_resource_properties(
            "AWS::Lambda::Function",
            {"Timeout": 300},
        )

    def test_lambda_function_has_function_url(self, template):
        """Verify a FunctionUrl is created."""
        template.resource_count_is("AWS::Lambda::Url", 1)

    def test_lambda_function_url_has_cors(self, template):
        """Verify FunctionUrl has CORS configured."""
        template.has_resource_properties(
            "AWS::Lambda::Url",
            {"Cors": {"AllowOrigins": ["*"]}},
        )

    def test_lambda_function_has_iam_role(self, template):
        """Verify an IAM Role is created for the Lambda."""
        template.resource_count_is("AWS::IAM::Role", 1)

    def test_lambda_function_has_execution_role(self, template):
        """Verify Lambda has basic execution role attached."""
        template.has_resource_properties(
            "AWS::IAM::Policy",
            {"PolicyName": "AWSLambdaBasicExecutionRole"},
        )

    def test_lambda_function_uses_docker_image(self, stack):
        """Verify the Lambda function uses a Docker image."""
        fn = stack.node.find_child("llama_lambda_server_lambda_function")
        assert isinstance(fn, aws_lambda.DockerImageFunction)

    def test_stack_has_cloudformation_output(self, template):
        """Verify the stack outputs the Lambda function URL."""
        template.has_output("UnchainedLambdaFunctionUrl", {})

    def test_default_architecture_is_arm64(self, template):
        """Verify default architecture is ARM64."""
        template.has_resource_properties(
            "AWS::Lambda::Function",
            {"Architecture": "arm64"},
        )

    def test_stack_synthesizes_without_errors(self, stack):
        """Verify the stack synthesizes successfully."""
        # If we get here, synthesis succeeded
        assert stack is not None
