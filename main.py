from graph_builder import build_email_graph
from email_parser import parse_email
from reply_generator import generate_reply
from csv_logger import log_to_csv
import os

def handle_email(email_file):
    email_data = parse_email(email_file)
    reply = generate_reply(email_data)
    log_to_csv(email_data, reply)
    print(f"Reply:\n{reply}")

if __name__ == "__main__":
    graph = build_email_graph()
    email_file = "test_emails/sample1.txt"
    handle_email(email_file)
