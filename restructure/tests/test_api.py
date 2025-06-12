"""
Tests for llmgenie FastAPI application
"""

import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.llmgenie.api.main import app

client = TestClient(app)

def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert data["version"] == "0.1.0"

def test_workflow_modes():
    """Test workflow modes endpoint"""
    response = client.get("/workflow/modes")
    assert response.status_code == 200
    data = response.json()
    assert "modes" in data
    assert "discuss" in data["modes"]
    assert "meta" in data["modes"]
    assert "code" in data["modes"]

def test_agent_execute():
    """Test agent execution endpoint"""
    request_data = {
        "agent_type": "test_agent",
        "task": "test_task",
        "context": {"test": "data"}
    }
    response = client.post("/agents/execute", json=request_data)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "completed"
    assert "agent_id" in data
    assert data["result"]["message"].startswith("Task 'test_task' executed")

def test_mcp_tools_placeholder():
    """Test MCP tools placeholder endpoint"""
    response = client.post("/mcp/tools/execute?tool_name=test_tool", json={"param": "value"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "not_implemented"
    assert "MCP integration coming" in data["message"] 