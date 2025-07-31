#!/usr/bin/env python3
"""
Basic functionality tests for the email automation system
"""

import sys
import os
import pytest

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.core.email_processor import parse_email
from src.core.reply_service import generate_reply
from src.core.data_logger import log_to_csv

def test_email_parsing():
    """Test that email parsing works correctly"""
    # Create a test email file
    test_email_content = """Subject: Test Email

Hi there,

This is a test email for testing purposes.

Best regards,
Test User"""
    
    test_file = "test_email.txt"
    with open(test_file, "w") as f:
        f.write(test_email_content)
    
    try:
        # Test parsing
        email_data = parse_email(test_file)
        
        # Verify structure
        assert "email_body" in email_data
        assert "subject" in email_data
        assert "Test Email" in email_data["subject"]
        assert "test email for testing purposes" in email_data["email_body"].lower()
        
    finally:
        # Cleanup
        if os.path.exists(test_file):
            os.remove(test_file)

def test_data_logging():
    """Test that data logging works correctly"""
    email_data = {
        "subject": "Test Subject",
        "email_body": "Test body",
        "category": "test",
        "intent": "test_intent",
        "entities": {"test": "value"}
    }
    reply = "Test reply"
    
    # Test logging
    log_to_csv(email_data, reply)
    
    # Verify log file exists
    log_path = "data/logs/reply_log.csv"
    assert os.path.exists(log_path)

def test_project_structure():
    """Test that the project structure is correct"""
    required_dirs = [
        "src",
        "src/core",
        "src/ui", 
        "src/models",
        "src/utils",
        "data",
        "data/emails",
        "data/logs",
        "config",
        "docs",
        "tests"
    ]
    
    for dir_path in required_dirs:
        assert os.path.exists(dir_path), f"Directory {dir_path} does not exist"
    
    required_files = [
        "src/core/email_processor.py",
        "src/core/langgraph_workflow.py", 
        "src/core/reply_service.py",
        "src/core/data_logger.py",
        "src/ui/main_interface.py",
        "src/utils/helpers.py",
        "config/app_config.yaml",
        "app.py",
        "setup.py",
        "requirements.txt"
    ]
    
    for file_path in required_files:
        assert os.path.exists(file_path), f"File {file_path} does not exist"

if __name__ == "__main__":
    pytest.main([__file__]) 