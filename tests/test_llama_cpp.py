"""Test suite for llama-cpp-python package integration."""
import pytest


def test_llama_cpp_import():
    """Verify that llama-cpp-python can be imported."""
    try:
        from llama_cpp import Llama
        assert Llama is not None
    except ImportError as e:
        pytest.fail(f"llama-cpp-python package not installed: {e}")


def test_llama_version():
    """Verify llama-cpp-python version supports Llama 3 models."""
    from llama_cpp import Llama
    import pkg_resources
    
    version = pkg_resources.get_distribution("llama-cpp-python").version
    major, minor = map(int, version.split(".")[:2])
    # llama-cpp-python v0.2.0+ supports Llama 3
    assert major >= 0 and minor >= 2, f"Version {version} may not support Llama 3"
