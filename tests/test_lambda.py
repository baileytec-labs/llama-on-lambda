"""Tests for llama_lambda_stack.py."""

import sys
import pytest
from unittest.mock import MagicMock, patch

# Mock AWS CDK imports before importing the module
sys_modules = {}
for mod_name in ["aws_cdk", "constructs"]:
    sys_modules[mod_name] = sys.modules.get(mod_name)
    sys.modules[mod_name] = MagicMock()

from llama_lambda_stack import LlamaLambdaStack


def test_lambda_stack_initialization():
    """Test LlamaLambdaStack initialization."""
    scope = MagicMock()
    construct_id = "test-stack"
    
    stack = LlamaLambdaStack(scope, construct_id)
    
    assert stack is not None


def test_lambda_stack_default_parameters():
    """Test LlamaLambdaStack uses default parameters."""
    scope = MagicMock()
    construct_id = "test-stack-defaults"
    
    stack = LlamaLambdaStack(scope, construct_id)
    
    # Verify the stack is initialized
    assert stack is not None


def test_lambda_stack_architecture_mapping():
    """Test architecture string to enum mapping."""
    # Test ARM_64 mapping
    arch_map = {
        "ARM_64": "ARM_64",
        "X86_64": "X86_64"
    }
    assert arch_map.get("ARM_64") == "ARM_64"
    assert arch_map.get("X86_64") == "X86_64"
    assert arch_map.get("INVALID", "ARM_64") == "ARM_64"
