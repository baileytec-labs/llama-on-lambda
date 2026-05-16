"""Tests for LlamaLambdaStack (legacy stack)."""
import pytest
from aws_cdk import App, Environment, aws_lambda
from aws_cdk.assertions import Template
from llama_lambda.llama_lambda_stack import LlamaLambdaStack


class TestLlamaLambdaStack:
    """Test suite for LlamaLambdaStack."""

    @pytest.fixture
    def app(self):
        """Create a CDK App for testing."""
        return App()

    @pytest.fixture
    def stack(self, app):
        """Create a LlamaLambdaStack for testing."""
        return LlamaLambdaStack(
            app,
            "TestLegacyStack",
            env=Environment(account="123456789012", region="us-east-1"),
        )

    @pytest.fixture
    def template(self, stack):
        """Create a CloudFormation Template from the stack."""
        return Template.from_stack(stack)

    def test_stack_creates_lambda_function(self, template):
        """Verify Lambda functions are created (main + LogRetention helper)."""
        template.resource_count_is("AWS::Lambda::Function", 2)

    def test_main_lambda_has_correct_timeout(self, template):
        """Verify main Lambda function has 900s timeout."""
        template.has_resource_properties(
            "AWS::Lambda::Function",
            {"Timeout": 900, "PackageType": "Image"},
        )

    def test_lambda_function_has_function_url(self, template):
        """Verify a FunctionUrl is created."""
        template.resource_count_is("AWS::Lambda::Url", 1)

    def test_lambda_function_has_iam_roles(self, template):
        """Verify IAM Roles are created (main role + LogRetention role)."""
        template.resource_count_is("AWS::IAM::Role", 2)

    def test_lambda_function_has_execution_policy(self, template):
        """Verify Lambda has CloudWatch Logs policy attached."""
        template.resource_count_is("AWS::IAM::Policy", 1)

    def test_lambda_function_uses_docker_image(self, stack):
        """Verify the Lambda function uses a Docker image."""
        fn = stack.node.find_child("open_llama_lambda_function")
        assert isinstance(fn, aws_lambda.DockerImageFunction)

    def test_lambda_memory_size(self, template):
        """Verify Lambda memory is 10240 MB."""
        template.has_resource_properties(
            "AWS::Lambda::Function",
            {"MemorySize": 10240},
        )

    def test_stack_has_cloudformation_output(self, template):
        """Verify the stack outputs the Lambda function URL."""
        template.has_output("OpenLlamaUrl", {})

    def test_stack_synthesizes_without_errors(self, stack):
        """Verify the stack synthesizes successfully."""
        assert stack is not None
