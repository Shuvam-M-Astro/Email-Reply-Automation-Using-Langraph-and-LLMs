import re
from datetime import datetime

def parse_email(file_path):
    """
    Enhanced email parser that extracts various email headers and body
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split content into headers and body
    parts = content.split('\n\n', 1)
    headers_text = parts[0] if len(parts) > 1 else ""
    body = parts[1] if len(parts) > 1 else content
    
    # Parse headers
    headers = {}
    for line in headers_text.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            headers[key.strip().lower()] = value.strip()
    
    # Extract key information
    subject = headers.get('subject', 'Subject: Unknown')
    sender = headers.get('from', headers.get('sender', 'Unknown'))
    recipient = headers.get('to', 'Unknown')
    date = headers.get('date', 'Unknown')
    
    # Clean up subject line
    if subject.startswith('Subject:'):
        subject = subject.replace('Subject:', '').strip()
    
    # Try to parse date
    parsed_date = None
    if date != 'Unknown':
        try:
            # Try common date formats
            date_formats = [
                '%a, %d %b %Y %H:%M:%S %z',
                '%d %b %Y %H:%M:%S %z',
                '%Y-%m-%d %H:%M:%S',
                '%m/%d/%Y %H:%M:%S'
            ]
            for fmt in date_formats:
                try:
                    parsed_date = datetime.strptime(date, fmt)
                    break
                except ValueError:
                    continue
        except:
            pass
    
    return {
        "subject": subject,
        "sender": sender,
        "recipient": recipient,
        "date": date,
        "parsed_date": parsed_date,
        "email_body": body.strip(),
        "headers": headers
    }
