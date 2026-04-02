"""Pytest fixtures for llama_lambda tests."""

import os
import pytest
from unittest.mock import MagicMock


@pytest.fixture
def mock_aws_context():
    """Mock AWS CDK context."""
    context = MagicMock()
    context.try_get_context = MagicMock(return_value=None)
    return context


@pytest.fixture
def mock_environment():
    """Mock environment variables."""
    env_vars = {
        "STAGE": "",
        "TITLEMESSAGE": "Test Message",
        "APIKEY": "test-key",
        "CHATFORMAT": "mistral-instruct",
        "MODELFILE": "https://example.com/model.bin",
        "ARCHITECTURE": "ARM_64",
    }
    with pytest.mock.patch.dict(os.environ, env_vars):
        yield env_vars


@pytest.fixture
def mock_llama_cpp():
    """Mock llama_cpp Llama class."""
    with pytest.mock.patch("llama_lambda.llama_cpp_docker.main.Llama") as mock_llama:
        mock_instance = MagicMock()
        mock_instance.return_value = mock_instance
        mock_instance.return_value.__call__ = MagicMock(
            return_value={"choices": [{"text": "Mock response"}]}
        )
        mock_llama.return_value = mock_instance
        yield mock_instance
