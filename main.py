from graph_builder import build_email_graph
from email_parser import parse_email
from reply_generator import generate_reply
from csv_logger import log_to_csv

def handle_email(email_file):
    email_data = parse_email(email_file)
    category, reply = generate_reply(email_data)
    email_data["category"] = category
    log_to_csv(email_data, reply)
    print(f"Category: {category}\n\nReply:\n{reply}")

if __name__ == "__main__":
    handle_email("test_emails/sample1.txt")
