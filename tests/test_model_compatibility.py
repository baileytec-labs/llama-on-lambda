"""Test model compatibility documentation."""
import pytest


def test_gguf_format_documented():
    """Verify GGUF format support is documented."""
    readme_path = "README.md"
    with open(readme_path, "r") as f:
        content = f.read()
    
    assert "GGUF" in content, "README should document GGUF format requirement"
    assert "Llama 3" in content, "README should mention Llama 3 support"


def test_model_size_requirements():
    """Verify model size requirements are documented."""
    readme_path = "README.md"
    with open(readme_path, "r") as f:
        content = f.read()
    
    # Check for 6GB limit mention (Docker container limit)
    assert "6GB" in content or "10GB" in content, "README should mention size constraints"
