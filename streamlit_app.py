import streamlit as st
from email_parser import parse_email
from reply_generator import generate_reply
from csv_logger import log_to_csv
import os
import csv
import json
import pandas as pd

st.title("📬 AI Email Reply Automation")

# Show previous replies if log exists
log_path = "logs/reply_log.csv"
if os.path.exists(log_path):
    with open(log_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)
        if len(rows) > 1:  # Skip header
            data = [json.loads(row[0]) for row in rows[1:]]
            df = pd.DataFrame(data)[["timestamp", "subject", "category", "intent", "reply"]]
            st.subheader("Previous AI-Generated Replies")
            st.dataframe(df.sort_values("timestamp", ascending=False), use_container_width=True)

uploaded_file = st.file_uploader("Upload an email (.txt) file", type=["txt"])

if uploaded_file is not None:
    # Read and parse the uploaded email
    email_content = uploaded_file.read().decode("utf-8")
    with open("temp_email.txt", "w", encoding="utf-8") as f:
        f.write(email_content)
    email_data = parse_email("temp_email.txt")

    st.subheader("Email Preview")
    st.code(email_content, language="text")

    # Generate reply
    with st.spinner("Generating reply..."):
        category, intent, entities, reply = generate_reply(email_data)
        email_data.update({
            "category": category,
            "intent": intent,
            "entities": entities
        })
        log_to_csv(email_data, reply)

    st.subheader("AI-Generated Reply")
    st.text_area("Reply", reply, height=150)

    st.markdown(f"**Category:** {category}")
    st.markdown(f"**Intent:** {intent}")
    st.markdown(f"**Entities:** {entities}")
    st.success("Reply generated and logged!") 