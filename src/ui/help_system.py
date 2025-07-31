import streamlit as st

def show_help_page():
    """
    Display the help and documentation page
    """
    st.markdown('<h1 class="main-header">❓ Help & Documentation</h1>', unsafe_allow_html=True)
    
    # Quick start guide
    st.subheader("🚀 Quick Start Guide")
    
    with st.expander("📋 Getting Started", expanded=True):
        st.markdown("""
        ### Step 1: Upload an Email
        1. Go to the **Home** page
        2. Click "Browse files" to upload a `.txt` email file
        3. The email will be automatically parsed and displayed
        
        ### Step 2: Generate a Reply
        1. Review the parsed email content
        2. Configure reply settings in the sidebar (optional)
        3. Click "🚀 Generate AI Reply" button
        4. Wait for the AI to analyze and generate a response
        
        ### Step 3: Review and Use
        1. Review the generated reply
        2. Copy it to clipboard if needed
        3. The reply is automatically saved to logs
        """)
    
    # Email format guide
    st.subheader("📧 Email Format Guide")
    
    with st.expander("📄 Supported Email Formats"):
        st.markdown("""
        ### Text File Format
        Your email should be saved as a `.txt` file with the following structure:
        
        ```
        Subject: Your email subject here
        From: sender@example.com
        To: recipient@example.com
        Date: 2024-01-15 10:30:00
        
        Email body content goes here.
        This can be multiple lines of text.
        ```
        
        ### Required Fields
        - **Subject**: Email subject line
        - **Body**: Main email content (required)
        
        ### Optional Fields
        - **From**: Sender email address
        - **To**: Recipient email address
        - **Date**: Email timestamp
        """)
        
        # Example email
        st.code("""
Subject: Meeting Request for Project Discussion
From: john.doe@company.com
To: jane.smith@company.com
Date: 2024-01-15 14:30:00

Hi Jane,

I hope this email finds you well. I would like to schedule a meeting to discuss the upcoming project timeline and deliverables.

Could you please let me know your availability for this week or next week? I'm flexible with the time and can accommodate your schedule.

Looking forward to hearing from you.

Best regards,
John
        """, language="text")
    
    # Features guide
    st.subheader("✨ Features Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🏠 Home Page
        - **Email Upload**: Upload and parse email files
        - **AI Reply Generation**: Generate intelligent responses
        - **Reply Customization**: Adjust tone and length
        - **Copy to Clipboard**: Easy reply copying
        - **Auto-save**: Automatic logging of replies
        
        ### 📊 Analytics Page
        - **Usage Statistics**: View reply metrics
        - **Category Analysis**: Email type distribution
        - **Timeline Charts**: Reply activity over time
        - **Quality Metrics**: Reply length and quality analysis
        - **Data Export**: Download filtered data
        """)
    
    with col2:
        st.markdown("""
        ### ⚙️ Settings Page
        - **AI Configuration**: Model and parameter settings
        - **Email Preferences**: Default tone and length
        - **Analytics Settings**: Data collection options
        - **Advanced Options**: Debug mode and caching
        - **Import/Export**: Configuration management
        
        ### 🔧 Advanced Features
        - **Entity Extraction**: Identify key information
        - **Intent Classification**: Understand email purpose
        - **Category Detection**: Automatically categorize emails
        - **Reply Quality**: Analyze response effectiveness
        """)
    
    # Troubleshooting
    st.subheader("🔧 Troubleshooting")
    
    with st.expander("❌ Common Issues"):
        st.markdown("""
        ### File Upload Issues
        **Problem**: File won't upload
        - **Solution**: Ensure file is `.txt` format and under 10MB
        - **Solution**: Check file encoding (UTF-8 recommended)
        
        ### AI Generation Issues
        **Problem**: Reply generation fails
        - **Solution**: Check OpenAI API key in Settings
        - **Solution**: Verify internet connection
        - **Solution**: Try reducing max tokens in Settings
        
        ### Display Issues
        **Problem**: Email not parsing correctly
        - **Solution**: Check email format (see Email Format Guide)
        - **Solution**: Ensure proper header separation with double newlines
        
        ### Performance Issues
        **Problem**: Slow response times
        - **Solution**: Use smaller model in Settings
        - **Solution**: Reduce max tokens
        - **Solution**: Check your internet connection
        """)
    
    # Best practices
    st.subheader("💡 Best Practices")
    
    with st.expander("🎯 Tips for Better Results"):
        st.markdown("""
        ### Email Preparation
        - **Clear Subject Lines**: Use descriptive subjects
        - **Complete Context**: Include all relevant information
        - **Proper Formatting**: Use standard email format
        
        ### Reply Generation
        - **Choose Appropriate Tone**: Match the original email's tone
        - **Review Before Sending**: Always review AI-generated replies
        - **Customize When Needed**: Adjust settings for specific needs
        
        ### Data Management
        - **Regular Backups**: Export your reply logs periodically
        - **Clean Old Data**: Use log retention settings
        - **Monitor Analytics**: Check usage patterns regularly
        """)
    
    # API and technical info
    st.subheader("🔌 Technical Information")
    
    with st.expander("⚙️ Technical Details"):
        st.markdown("""
        ### Supported Models
        - **GPT-4**: Best quality, slower response
        - **GPT-3.5-turbo**: Good balance of speed and quality
        - **GPT-4-turbo**: Latest model with improved performance
        
        ### Configuration Files
        - **config.yaml**: Main configuration file
        - **logs/reply_log.csv**: Reply history and analytics data
        
        ### Dependencies
        - **Streamlit**: Web interface framework
        - **OpenAI**: AI model API
        - **LangGraph**: Workflow orchestration
        - **Plotly**: Data visualization
        """)
    
    # Contact and support
    st.subheader("📞 Support")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🐛 Report Issues
        If you encounter problems:
        1. Check the troubleshooting section above
        2. Review the error messages carefully
        3. Note the steps that led to the issue
        4. Contact support with detailed information
        
        ### 💬 Get Help
        - **Documentation**: This help page
        - **Settings**: Check configuration options
        - **Analytics**: Review usage patterns
        """)
    
    with col2:
        st.markdown("""
        ### 📚 Additional Resources
        - **OpenAI Documentation**: API reference and guides
        - **Streamlit Documentation**: Interface customization
        - **LangGraph Documentation**: Workflow development
        
        ### 🔄 Updates
        - Check for updates regularly
        - Review changelog for new features
        - Backup data before major updates
        """)
    
    # Footer with version info
    st.divider()
    st.markdown(
        """
        <div style='text-align: center; color: #666; padding: 1rem;'>
            <p>📧 AI Email Reply Automation v1.0 | 🤖 Powered by LangGraph & OpenAI</p>
        </div>
        """,
        unsafe_allow_html=True
    ) 