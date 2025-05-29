import csv
import os
from datetime import datetime

def log_to_csv(email_data, reply):
    log_path = "logs/reply_log.csv"
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    file_exists = os.path.isfile(log_path)

    with open(log_path, mode='a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(["Timestamp", "Subject", "Email Body", "Category", "Generated Reply"])
        writer.writerow([
            datetime.now(),
            email_data.get("subject", "Unknown"),
            email_data["email_body"],
            email_data.get("category", "Unknown"),
            reply
        ])
