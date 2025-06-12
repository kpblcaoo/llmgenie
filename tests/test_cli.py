"""
Tests for llmgenie CLI module
"""

import pytest
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_cli_import():
    """Test that CLI module can be imported"""
    try:
        from core.llmgenie import cli
        assert True
    except ImportError:
        pytest.fail("CLI module cannot be imported")

def test_llm_client_import():
    """Test that LLM client can be imported"""
    try:
        from core.llmgenie import llm_client
        assert True
    except ImportError:
        pytest.fail("LLM client module cannot be imported") 