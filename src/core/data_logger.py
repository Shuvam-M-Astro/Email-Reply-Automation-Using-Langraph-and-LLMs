import csv
import json
import os
from datetime import datetime

def log_to_csv(email_data, reply):
    log_path = "data/logs/reply_log.csv"
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    file_exists = os.path.isfile(log_path)

    # Build compact JSON state
    full_state = {
        "timestamp": str(datetime.now()),
        "subject": email_data.get("subject", "Unknown"),
        "email_body": email_data["email_body"],
        "category": email_data.get("category", "Unknown"),
        "intent": email_data.get("intent", "Unknown"),
        "entities": email_data.get("entities", {}),
        "reply": reply
    }

    # Write to CSV with compact JSON (1-line per row)
    with open(log_path, mode='a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
        if not file_exists:
            writer.writerow(["FullEmailStateJSON"])
        writer.writerow([json.dumps(full_state, ensure_ascii=False)])
