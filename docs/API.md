# API Documentation

## Core Modules

### Email Processor (`src/core/email_processor.py`)

The email processor handles parsing and validation of email files.

#### Functions

- `parse_email(file_path: str) -> dict`: Parses an email file and returns structured data

### Reply Service (`src/core/reply_service.py`)

The reply service orchestrates the LangGraph workflow for generating replies.

#### Functions

- `generate_reply(email_data: dict) -> tuple`: Generates a reply using the LangGraph workflow

### Data Logger (`src/core/data_logger.py`)

The data logger handles persistence of email interactions.

#### Functions

- `log_to_csv(email_data: dict, reply: str) -> None`: Logs email data and reply to CSV

### LangGraph Workflow (`src/core/langgraph_workflow.py`)

The core LangGraph workflow that processes emails through classification, entity extraction, and reply generation.

#### Functions

- `build_email_graph() -> CompiledGraph`: Builds and returns the compiled LangGraph workflow

## UI Modules

### Main Interface (`src/ui/main_interface.py`)

The main Streamlit web interface.

### Analytics Dashboard (`src/ui/analytics_dashboard.py`)

Analytics and reporting interface.

### Settings Panel (`src/ui/settings_panel.py`)

Configuration management interface.

### Help System (`src/ui/help_system.py`)

Help and documentation interface.

## Utility Modules

### Helpers (`src/utils/helpers.py`)

Common utility functions used throughout the application.

#### Functions

- `load_config() -> dict`: Loads configuration from YAML file
- `safe_api_call(func, *args, **kwargs) -> Any`: Safely calls API functions with retry logic

## Usage Examples

### Basic Email Processing

```python
from src.core.email_processor import parse_email
from src.core.reply_service import generate_reply

# Parse email
email_data = parse_email("path/to/email.txt")

# Generate reply
category, intent, entities, reply = generate_reply(email_data)

print(f"Category: {category}")
print(f"Intent: {intent}")
print(f"Entities: {entities}")
print(f"Reply: {reply}")
```

### Custom Configuration

```python
from src.utils.helpers import load_config

# Load custom configuration
config = load_config("path/to/custom_config.yaml")

# Use configuration
api_key = config["openai_api_key"]
temperature = config.get("model_temperature", 0.3)
```

### Data Logging

```python
from src.core.data_logger import log_to_csv

# Log email interaction
email_data = {
    "subject": "Test Subject",
    "email_body": "Test body",
    "category": "support",
    "intent": "help_request",
    "entities": {"user": "John"}
}
reply = "Thank you for your inquiry..."

log_to_csv(email_data, reply)
``` 