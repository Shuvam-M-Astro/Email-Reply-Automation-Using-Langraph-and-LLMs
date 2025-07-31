

# 📬 LangGraph Email Reply Automation

A professional, production-ready LangGraph-powered agentic AI system that generates automatic replies to emails using fine-tuned large language models. This modular and extendable project provides intelligent email classification, intent extraction, and automated response generation.

![Demo](assets/Demo.png)

## 🏗️ Project Structure

```
langgraph-email-reply-automation/
├── src/                          # Source code
│   ├── core/                     # Core functionality
│   │   ├── email_processor.py    # Email parsing and processing
│   │   ├── langgraph_workflow.py # LangGraph workflow definition
│   │   ├── reply_service.py      # Reply generation service
│   │   └── data_logger.py        # Data logging and analytics
│   ├── ui/                       # User interface components
│   │   ├── main_interface.py     # Streamlit main interface
│   │   ├── analytics_dashboard.py # Analytics and reporting
│   │   ├── settings_panel.py     # Configuration management
│   │   └── help_system.py        # Help and documentation
│   ├── models/                   # Machine learning models
│   │   ├── gpt2_trainer.py       # GPT-2 fine-tuning
│   │   └── roberta_trainer.py    # RoBERTa fine-tuning
│   └── utils/                    # Utility functions
│       └── helpers.py            # Common utilities
├── data/                         # Data storage
│   ├── emails/                   # Test email files
│   └── logs/                     # Application logs
├── config/                       # Configuration files
│   └── app_config.yaml          # Main configuration
├── docs/                         # Documentation
├── tests/                        # Test files
├── assets/                       # Static assets
├── app.py                        # Main application entry point
├── setup.py                      # Package setup
└── requirements.txt              # Dependencies
```

## 🚀 Features

- **Intelligent Email Classification**: Automatically categorizes emails into support, schedule, billing, feedback, or other
- **Entity Extraction**: Extracts key information like names, dates, times, and intent
- **Contextual Reply Generation**: Generates professional, context-aware responses
- **Web Interface**: Modern Streamlit-based UI with analytics dashboard
- **Comprehensive Logging**: Tracks all interactions for audit and improvement
- **Modular Architecture**: Easy to extend and customize
- **Production Ready**: Professional structure with proper error handling

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- OpenAI API key

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/langgraph-email-reply-automation.git
   cd langgraph-email-reply-automation
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure your API key**
   ```bash
   # Edit config/app_config.yaml
   openai_api_key: "your-openai-api-key-here"
   ```

4. **Run the application**
   ```bash
   # Command line interface
   python app.py data/emails/sample1.txt
   
   # Web interface
   python app.py --web
   ```

## 📖 Usage

### Command Line Interface

Process a single email file:
```bash
python app.py path/to/email.txt
```

### Web Interface

Launch the Streamlit web interface:
```bash
python app.py --web
```

Or directly:
```bash
streamlit run src/ui/main_interface.py
```

### Programmatic Usage

```python
from src.core.email_processor import parse_email
from src.core.reply_service import generate_reply

# Parse email
email_data = parse_email("path/to/email.txt")

# Generate reply
category, intent, entities, reply = generate_reply(email_data)

print(f"Category: {category}")
print(f"Intent: {intent}")
print(f"Reply: {reply}")
```

## ⚙️ Configuration

Edit `config/app_config.yaml` to customize:

```yaml
# OpenAI Configuration
openai_api_key: "your-openai-api-key-here"
model_temperature: 0.3
model_name: "gpt-3.5-turbo"

# Application Settings
max_retries: 3
base_delay: 1.0
max_delay: 60.0
backoff_factor: 2.0

# Logging Configuration
log_level: "INFO"
log_file: "data/logs/app.log"

# UI Settings
default_reply_tone: "Professional"
default_reply_length: "Standard"
auto_save_enabled: true
```

## 🧪 Example

**Input Email:**
```
Subject: Meeting Reschedule

Hi team,

Can we move our meeting from 3pm to 4:30pm tomorrow?

Thanks,
Alex
```

**Generated Response:**
```
Hi Alex,

Sure, we can reschedule the meeting to 4:30pm tomorrow. I've updated the calendar invite accordingly.

Best regards,  
Support Team
```

## 📊 Analytics

The system provides comprehensive analytics including:
- Email classification statistics
- Response generation metrics
- User interaction patterns
- Performance monitoring

Access analytics through the web interface or check `data/logs/reply_log.csv`.

## 🔧 Development

### Project Structure

- **Core Module**: Contains the main business logic for email processing and reply generation
- **UI Module**: Streamlit-based user interface components
- **Models Module**: Machine learning model training and fine-tuning
- **Utils Module**: Shared utility functions and helpers

### Adding New Features

1. **New Email Classifier**: Add to `src/core/langgraph_workflow.py`
2. **New UI Page**: Create in `src/ui/` and import in `main_interface.py`
3. **New Model**: Add to `src/models/` with proper training scripts
4. **New Utility**: Add to `src/utils/helpers.py`

### Testing

```bash
# Run tests
python -m pytest tests/

# Run with coverage
python -m pytest tests/ --cov=src
```

## 📈 Roadmap

- [ ] Gmail API integration
- [ ] Multilingual support
- [ ] Advanced entity recognition
- [ ] Custom model fine-tuning UI
- [ ] Real-time collaboration features
- [ ] Enterprise deployment options

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- 📧 Email: support@email-automation.com
- 📖 Documentation: [docs/](docs/)
- 🐛 Issues: [GitHub Issues](https://github.com/your-username/langgraph-email-reply-automation/issues)

---

**Built with ❤️ using LangGraph, LangChain, and Streamlit**
