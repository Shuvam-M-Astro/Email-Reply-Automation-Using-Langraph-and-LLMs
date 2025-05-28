def parse_email(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    subject = next((line for line in lines if line.lower().startswith("subject:")), "Subject: Unknown")
    body = ''.join(lines[lines.index('\n')+1:]).strip()
    return {"subject": subject, "email_body": body}
