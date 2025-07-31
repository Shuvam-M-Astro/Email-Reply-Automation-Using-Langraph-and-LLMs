#!/usr/bin/env python3
"""
LangGraph Email Reply Automation
Main application entry point
"""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.core.email_processor import parse_email
from src.core.reply_service import generate_reply
from src.core.data_logger import log_to_csv

def handle_email(email_file):
    """
    Process an email file and generate an automated reply
    
    Args:
        email_file (str): Path to the email file to process
    """
    # Parse email into dict with 'email_body' and optionally 'subject'
    email_data = parse_email(email_file)

    # Print the input email
    print("===== Input Email =====")
    if 'subject' in email_data:
        print(f"Subject: {email_data['subject']}")
    print(f"Body:\n{email_data['email_body']}\n")

    # Generate classification, intent, entities, and reply
    category, intent, entities, reply = generate_reply(email_data)

    # Add extra info to email data for logging
    email_data.update({
        "category": category,
        "intent": intent,
        "entities": entities
    })

    # Log the interaction
    log_to_csv(email_data, reply)

    # Print to console
    print("===== Categorized Values =====")
    print(f"Category: {category}")
    print(f"Intent: {intent}")
    print(f"Entities: {entities}")
    print(f"\n===== Reply ===== \n{reply}")

def main():
    """Main entry point for the application"""
    import argparse
    
    parser = argparse.ArgumentParser(description="LangGraph Email Reply Automation")
    parser.add_argument("email_file", help="Path to the email file to process")
    parser.add_argument("--web", action="store_true", help="Launch the web interface")
    
    args = parser.parse_args()
    
    if args.web:
        # Launch Streamlit web interface
        import subprocess
        subprocess.run(["streamlit", "run", "src/ui/main_interface.py"])
    else:
        # Process single email file
        handle_email(args.email_file)

if __name__ == "__main__":
    main() 