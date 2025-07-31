import streamlit as st
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.core.email_processor import parse_email
from src.core.reply_service import generate_reply
from src.core.data_logger import log_to_csv
from .analytics_dashboard import show_analytics_page
from .settings_panel import show_settings_page
from .help_system import show_help_page
from src.utils.helpers import load_config, safe_api_call
import os
import csv
import json
import pandas as pd
from datetime import datetime
import pyperclip
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load configuration
try:
    config = load_config()
except Exception as e:
    st.error(f"Failed to load configuration: {e}")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="AI Email Reply Automation",
    page_icon="📬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .reply-box {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #dee2e6;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #c3e6cb;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Reply tone selection
    reply_tone = st.selectbox(
        "Reply Tone",
        ["Professional", "Friendly", "Formal", "Casual"],
        help="Select the tone for generated replies"
    )
    
    # Reply length preference
    reply_length = st.selectbox(
        "Reply Length",
        ["Concise", "Standard", "Detailed"],
        help="Select the preferred length of replies"
    )
    
    # Auto-save option
    auto_save = st.checkbox("Auto-save replies", value=True)
    
    st.divider()
    
    # Statistics
    st.header("📊 Statistics")
    log_path = "logs/reply_log.csv"
    if os.path.exists(log_path):
        try:
            with open(log_path, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                rows = list(reader)
                total_replies = len(rows) - 1 if len(rows) > 1 else 0
                st.metric("Total Replies", total_replies)
                
                if total_replies > 0:
                    data = [json.loads(row[0]) for row in rows[1:]]
                    categories = [item.get("category", "Unknown") for item in data]
                    unique_categories = len(set(categories))
                    st.metric("Unique Categories", unique_categories)
        except Exception as e:
            st.error(f"Error loading statistics: {e}")

# Navigation
st.sidebar.title("📬 Navigation")
page = st.sidebar.selectbox(
    "Choose a page",
    ["🏠 Home", "📊 Analytics", "⚙️ Settings", "❓ Help"]
)

# Main content
if page == "🏠 Home":
    st.markdown('<h1 class="main-header">📬 AI Email Reply Automation</h1>', unsafe_allow_html=True)

    # File upload section
    st.header("📤 Upload Email")
uploaded_file = st.file_uploader(
    "Upload an email (.txt) file", 
    type=["txt"],
    help="Upload a text file containing the email content"
)

if uploaded_file is not None:
    try:
        # Read and parse the uploaded email
        email_content = uploaded_file.read().decode("utf-8")
        
        # Save to temporary file
        with open("temp_email.txt", "w", encoding="utf-8") as f:
            f.write(email_content)
        
        email_data = parse_email("temp_email.txt")
        
        # Display email preview in a better format
        st.subheader("📧 Email Preview")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("**Subject:**")
            st.info(email_data.get("subject", "No subject"))
            
            # Extract and display sender if available
            lines = email_content.split('\n')
            sender_line = next((line for line in lines if line.lower().startswith("from:")), None)
            if sender_line:
                st.markdown("**From:**")
                st.info(sender_line.replace("From:", "").strip())
        
        with col2:
            st.markdown("**Email Body:**")
            st.text_area(
                "Email Content",
                email_data.get("email_body", email_content),
                height=200,
                disabled=True
            )
        
        # Generate reply button
        if st.button("🚀 Generate AI Reply", type="primary", use_container_width=True):
            with st.spinner("🤖 Generating intelligent reply..."):
                try:
                    # Check if API key is configured
                    if not config.get("openai_api_key") or config["openai_api_key"] == "your-openai-api-key-here":
                        st.error("❌ OpenAI API key not configured. Please set your API key in config.yaml")
                        st.info("💡 Go to Settings page to configure your API key")
                        st.stop()
                    
                    # Generate reply with retry logic
                    category, intent, entities, reply = generate_reply(email_data)
                    email_data.update({
                        "category": category,
                        "intent": intent,
                        "entities": entities
                    })
                    
                    if auto_save:
                        try:
                            log_to_csv(email_data, reply)
                        except Exception as e:
                            logger.warning(f"Failed to save to CSV: {e}")
                            st.warning("⚠️ Reply generated but failed to save to logs")
                    
                    # Display results
                    st.subheader("🤖 AI-Generated Reply")
                    
                    # Reply display with copy functionality
                    reply_container = st.container()
                    with reply_container:
                        st.markdown('<div class="reply-box">', unsafe_allow_html=True)
                        st.text_area(
                            "Generated Reply",
                            reply,
                            height=200,
                            key="reply_text"
                        )
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        # Copy button
                        if st.button("📋 Copy to Clipboard", use_container_width=True):
                            try:
                                pyperclip.copy(reply)
                                st.success("✅ Reply copied to clipboard!")
                            except Exception as e:
                                st.error(f"Failed to copy to clipboard: {e}")
                    
                    # Analysis results
                    st.subheader("📊 Analysis Results")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                        st.metric("Category", category)
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                        st.metric("Intent", intent)
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    with col3:
                        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                        st.metric("Entities Found", len(entities) if isinstance(entities, dict) else 0)
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Detailed entities display
                    if entities and isinstance(entities, dict):
                        with st.expander("🔍 View Extracted Entities"):
                            for entity_type, entity_value in entities.items():
                                st.write(f"**{entity_type}:** {entity_value}")
                    
                    # Success message
                    if auto_save:
                        st.markdown('<div class="success-message">', unsafe_allow_html=True)
                        st.success("✅ Reply generated and automatically saved to logs!")
                        st.markdown('</div>', unsafe_allow_html=True)
                    else:
                        st.success("✅ Reply generated successfully!")
                        
                except Exception as e:
                    logger.error(f"Error generating reply: {e}")
                    st.error(f"❌ Error generating reply: {str(e)}")
                    
                    # Provide helpful error messages
                    if "rate limit" in str(e).lower():
                        st.info("💡 This error is due to API rate limiting. Please wait a moment and try again.")
                    elif "authentication" in str(e).lower():
                        st.info("💡 Please check your OpenAI API key in the Settings page.")
                    elif "quota" in str(e).lower():
                        st.info("💡 You've reached your OpenAI API quota. Please check your account.")
                    else:
                        st.info("💡 If this error persists, please check your internet connection and try again.")
    
    except Exception as e:
        st.error(f"❌ Error processing file: {str(e)}")
        st.exception(e)

# Show previous replies if log exists
if os.path.exists(log_path):
    try:
        with open(log_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            rows = list(reader)
            if len(rows) > 1:  # Skip header
                data = [json.loads(row[0]) for row in rows[1:]]
                df = pd.DataFrame(data)
                
                st.subheader("📚 Previous AI-Generated Replies")
                
                # Add filters
                col1, col2 = st.columns(2)
                with col1:
                    category_filter = st.selectbox(
                        "Filter by Category",
                        ["All"] + list(df["category"].unique())
                    )
                
                with col2:
                    search_term = st.text_input("Search in subjects", "")
                
                # Apply filters
                filtered_df = df.copy()
                if category_filter != "All":
                    filtered_df = filtered_df[filtered_df["category"] == category_filter]
                
                if search_term:
                    filtered_df = filtered_df[filtered_df["subject"].str.contains(search_term, case=False, na=False)]
                
                # Display filtered data
                if not filtered_df.empty:
                    display_df = filtered_df[["timestamp", "subject", "category", "intent"]].sort_values("timestamp", ascending=False)
                    st.dataframe(display_df, use_container_width=True)
                    
                    # Download option
                    csv_data = filtered_df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download Filtered Data",
                        data=csv_data,
                        file_name=f"email_replies_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
                else:
                    st.info("No replies match the selected filters.")
                    
    except Exception as e:
        st.error(f"Error loading previous replies: {e}")

    # Footer
    st.divider()
    st.markdown(
        """
        <div style='text-align: center; color: #666; padding: 1rem;'>
            <p>🤖 Powered by LangGraph & OpenAI | 📧 AI Email Reply Automation</p>
        </div>
        """,
        unsafe_allow_html=True
    )

elif page == "📊 Analytics":
    show_analytics_page()
elif page == "⚙️ Settings":
    show_settings_page()
elif page == "❓ Help":
    show_help_page() 