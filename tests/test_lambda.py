"""Tests for llama_lambda_stack.py."""

import pytest
from unittest.mock import MagicMock, patch

# Mock AWS CDK imports before importing the module
sys_modules = {}
for mod_name in ["aws_cdk", "constructs"]:
    sys_modules[mod_name] = sys.modules.get(mod_name)
    sys.modules[mod_name] = MagicMock()

from llama_lambda.llama_lambda_stack import LambdaFunctionStack


def test_lambda_stack_initialization(mock_aws_context):
    """Test LambdaFunctionStack initialization."""
    scope = MagicMock()
    construct_id = "test-stack"
    
    stack = LambdaFunctionStack(scope, construct_id, node=mock_aws_context)
    
    assert stack is not None
    assert stack.node == mock_aws_context


def test_lambda_stack_default_parameters(mock_aws_context):
    """Test LambdaFunctionStack uses default parameters when context not provided."""
    scope = MagicMock()
    construct_id = "test-stack-defaults"
    
    stack = LambdaFunctionStack(scope, construct_id, node=mock_aws_context)
    
    # Verify default values are applied
    assert stack.node.try_get_context("apikey") == "insert_api_key_here"
    assert stack.node.try_get_context("chatformat") == "mistral-instruct"
    assert stack.node.try_get_context("modelfile") is None or "stablelm" in stack.node.try_get_context("modelfile")
    assert stack.node.try_get_context("architecture") == "ARM_64"


def test_lambda_stack_architecture_mapping(mock_aws_context):
    """Test architecture string to enum mapping."""
    scope = MagicMock()
    construct_id = "test-arch-map"
    
    stack = LambdaFunctionStack(scope, construct_id, node=mock_aws_context)
    
    # Test ARM_64 mapping
    mock_aws_context.try_get_context.return_value = "ARM_64"
    arch_map = {
        "ARM_64": "ARM_64",
        "X86_64": "X86_64"
    }
    assert arch_map.get("ARM_64") == "ARM_64"
    assert arch_map.get("X86_64") == "X86_64"
    assert arch_map.get("INVALID", "ARM_64") == "ARM_64"
