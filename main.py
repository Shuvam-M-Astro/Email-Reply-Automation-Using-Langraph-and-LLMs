from email_parser import parse_email
from reply_generator import generate_reply
from csv_logger import log_to_csv

def handle_email(email_file):
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

    log_to_csv(email_data, reply)


    # Print to console
    print("===== Categorized Values =====")
    print(f"Category: {category}")
    print(f"Intent: {intent}")
    print(f"Entities: {entities}")
    print(f"\n===== Reply ===== \n{reply}")

if __name__ == "__main__":
    handle_email("test_emails/sample1.txt")
