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
        """Verify Lambda functions are created (main + LogRetention helper)."""
        # CDK creates a LogRetention Lambda in addition to our function
        template.resource_count_is("AWS::Lambda::Function", 2)

    def test_main_lambda_has_correct_timeout(self, template):
        """Verify main Lambda function has 300s timeout."""
        template.has_resource_properties(
            "AWS::Lambda::Function",
            {"Timeout": 300, "PackageType": "Image"},
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

    def test_lambda_function_has_iam_roles(self, template):
        """Verify IAM Roles are created (main role + LogRetention role)."""
        # CDK creates a LogRetention role in addition to our role
        template.resource_count_is("AWS::IAM::Role", 2)

    def test_lambda_function_has_execution_policy(self, template):
        """Verify Lambda has CloudWatch Logs policy attached."""
        template.resource_count_is("AWS::IAM::Policy", 1)

    def test_lambda_function_uses_docker_image(self, stack):
        """Verify the Lambda function uses a Docker image."""
        fn = stack.node.find_child("llama_lambda_server_lambda_function")
        assert isinstance(fn, aws_lambda.DockerImageFunction)

    def test_stack_has_cloudformation_output(self, template):
        """Verify the stack outputs the Lambda function URL."""
        template.has_output("UnchainedLambdaFunctionUrl", {})

    def test_default_architecture_is_arm64(self, template):
        """Verify default architecture is ARM64."""
        # Docker image Lambdas use Architectures array, not Architecture
        template.has_resource_properties(
            "AWS::Lambda::Function",
            {"Architectures": ["arm64"], "PackageType": "Image"},
        )

    def test_lambda_memory_size(self, template):
        """Verify Lambda memory is 3500 MB."""
        template.has_resource_properties(
            "AWS::Lambda::Function",
            {"MemorySize": 3500},
        )

    def test_stack_synthesizes_without_errors(self, stack):
        """Verify the stack synthesizes successfully."""
        assert stack is not None
