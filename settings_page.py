import streamlit as st
import yaml
import os
from datetime import datetime

def show_settings_page():
    """
    Display the settings configuration page
    """
    st.markdown('<h1 class="main-header">⚙️ Settings</h1>', unsafe_allow_html=True)
    
    # Configuration file path
    config_file = "config.yaml"
    
    # Load existing config or create default
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f) or {}
    else:
        config = {}
    
    st.subheader("🤖 AI Configuration")
    
    # OpenAI settings
    st.write("**OpenAI Settings**")
    openai_api_key = st.text_input(
        "OpenAI API Key",
        value=config.get('openai', {}).get('api_key', ''),
        type="password",
        help="Your OpenAI API key for generating replies"
    )
    
    model_name = st.selectbox(
        "Model",
        ["gpt-4", "gpt-3.5-turbo", "gpt-4-turbo"],
        index=["gpt-4", "gpt-3.5-turbo", "gpt-4-turbo"].index(
            config.get('openai', {}).get('model', 'gpt-4')
        ),
        help="Choose the OpenAI model to use"
    )
    
    max_tokens = st.slider(
        "Max Tokens",
        min_value=50,
        max_value=1000,
        value=config.get('openai', {}).get('max_tokens', 300),
        help="Maximum number of tokens in the generated reply"
    )
    
    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=2.0,
        value=config.get('openai', {}).get('temperature', 0.7),
        step=0.1,
        help="Controls randomness in the response (0 = deterministic, 2 = very random)"
    )
    
    st.subheader("📧 Email Processing")
    
    # Email processing settings
    auto_save_default = st.checkbox(
        "Auto-save replies by default",
        value=config.get('email', {}).get('auto_save_default', True),
        help="Automatically save generated replies to the log"
    )
    
    default_tone = st.selectbox(
        "Default Reply Tone",
        ["Professional", "Friendly", "Formal", "Casual"],
        index=["Professional", "Friendly", "Formal", "Casual"].index(
            config.get('email', {}).get('default_tone', 'Professional')
        ),
        help="Default tone for generated replies"
    )
    
    default_length = st.selectbox(
        "Default Reply Length",
        ["Concise", "Standard", "Detailed"],
        index=["Concise", "Standard", "Detailed"].index(
            config.get('email', {}).get('default_length', 'Standard')
        ),
        help="Default length preference for replies"
    )
    
    st.subheader("📊 Analytics & Logging")
    
    # Analytics settings
    enable_analytics = st.checkbox(
        "Enable Analytics",
        value=config.get('analytics', {}).get('enabled', True),
        help="Collect usage analytics and generate insights"
    )
    
    log_retention_days = st.number_input(
        "Log Retention (days)",
        min_value=1,
        max_value=365,
        value=config.get('analytics', {}).get('log_retention_days', 90),
        help="How long to keep reply logs"
    )
    
    st.subheader("🔧 Advanced Settings")
    
    # Advanced settings
    debug_mode = st.checkbox(
        "Debug Mode",
        value=config.get('advanced', {}).get('debug_mode', False),
        help="Enable debug logging and detailed error messages"
    )
    
    cache_replies = st.checkbox(
        "Cache Replies",
        value=config.get('advanced', {}).get('cache_replies', True),
        help="Cache generated replies to avoid regenerating similar responses"
    )
    
    # Save configuration
    if st.button("💾 Save Settings", type="primary", use_container_width=True):
        # Update config dictionary
        config.update({
            'openai': {
                'api_key': openai_api_key,
                'model': model_name,
                'max_tokens': max_tokens,
                'temperature': temperature
            },
            'email': {
                'auto_save_default': auto_save_default,
                'default_tone': default_tone,
                'default_length': default_length
            },
            'analytics': {
                'enabled': enable_analytics,
                'log_retention_days': log_retention_days
            },
            'advanced': {
                'debug_mode': debug_mode,
                'cache_replies': cache_replies
            },
            'last_updated': datetime.now().isoformat()
        })
        
        # Save to file
        try:
            with open(config_file, 'w') as f:
                yaml.dump(config, f, default_flow_style=False)
            st.success("✅ Settings saved successfully!")
        except Exception as e:
            st.error(f"❌ Error saving settings: {e}")
    
    # Reset to defaults
    if st.button("🔄 Reset to Defaults", use_container_width=True):
        if st.checkbox("I confirm I want to reset all settings"):
            try:
                os.remove(config_file)
                st.success("✅ Settings reset to defaults!")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error resetting settings: {e}")
    
    # Export/Import settings
    st.subheader("📤 Export/Import Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Export settings
        if st.button("📤 Export Settings"):
            try:
                yaml_content = yaml.dump(config, default_flow_style=False)
                st.download_button(
                    label="💾 Download Config",
                    data=yaml_content,
                    file_name=f"email_automation_config_{datetime.now().strftime('%Y%m%d_%H%M%S')}.yaml",
                    mime="text/yaml"
                )
            except Exception as e:
                st.error(f"❌ Error exporting settings: {e}")
    
    with col2:
        # Import settings
        uploaded_config = st.file_uploader(
            "Import Config File",
            type=["yaml", "yml"],
            help="Upload a YAML configuration file"
        )
        
        if uploaded_config is not None:
            try:
                config_content = uploaded_config.read().decode("utf-8")
                imported_config = yaml.safe_load(config_content)
                
                if st.button("📥 Import Settings"):
                    with open(config_file, 'w') as f:
                        yaml.dump(imported_config, f, default_flow_style=False)
                    st.success("✅ Settings imported successfully!")
                    st.rerun()
            except Exception as e:
                st.error(f"❌ Error importing settings: {e}")
    
    # System information
    st.subheader("ℹ️ System Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Current Configuration File:**")
        st.code(config_file)
        
        st.write("**Last Updated:**")
        last_updated = config.get('last_updated', 'Never')
        st.info(last_updated)
    
    with col2:
        st.write("**Configuration Status:**")
        if os.path.exists(config_file):
            st.success("✅ Configuration file exists")
        else:
            st.warning("⚠️ No configuration file found")
        
        st.write("**File Size:**")
        if os.path.exists(config_file):
            size = os.path.getsize(config_file)
            st.info(f"{size} bytes")
        else:
            st.info("N/A") 