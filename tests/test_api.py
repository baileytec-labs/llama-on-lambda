"""Tests for llama_cpp_docker/main.py FastAPI endpoints."""

import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from fastapi import Header, HTTPException


def test_prompt_endpoint_success():
    """Test /prompt endpoint with valid input."""
    # Import after mocking
    with patch("llama_lambda.llama_cpp_docker.main.Llama") as mock_llama:
        mock_instance = MagicMock()
        mock_instance.return_value = mock_instance
        mock_instance.return_value.__call__ = MagicMock(
            return_value={"choices": [{"text": "Test response"}]}
        )
        mock_llama.return_value = mock_instance
        
        from llama_lambda.llama_cpp_docker.main import app
        client = TestClient(app)
        
        response = client.post(
            "/prompt",
            json={
                "text": "What is 2+2?",
                "tokencount": 10,
                "penalty": 1.1,
                "seedval": 42
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "returnmsg" in data
        assert data["returnmsg"] == "Test response"


def test_prompt_endpoint_missing_text():
    """Test /prompt endpoint with missing text parameter."""
    with patch("llama_lambda.llama_cpp_docker.main.Llama") as mock_llama:
        mock_instance = MagicMock()
        mock_instance.return_value = mock_instance
        mock_instance.return_value.__call__ = MagicMock(
            return_value={"choices": [{"text": "Test response"}]}
        )
        mock_llama.return_value = mock_instance
        
        from llama_lambda.llama_cpp_docker.main import app
        client = TestClient(app)
        
        response = client.post(
            "/prompt",
            json={
                "tokencount": 10,
                "penalty": 1.1,
                "seedval": 42
            }
        )
        
        # FastAPI should validate required fields
        assert response.status_code == 422


def test_prompt_endpoint_error_handling():
    """Test /prompt endpoint error handling."""
    with patch("llama_lambda.llama_cpp_docker.main.Llama") as mock_llama:
        mock_llama.side_effect = Exception("Model not found")
        
        from llama_lambda.llama_cpp_docker.main import app
        client = TestClient(app)
        
        response = client.post(
            "/prompt",
            json={
                "text": "Test query",
                "tokencount": 10
            }
        )
        
        assert response.status_code == 500
        data = response.json()
        assert "detail" in data
        assert "Internal server error" in data["detail"]
