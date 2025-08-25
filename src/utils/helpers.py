import yaml
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
import json
import csv
import os
import time
import random
from typing import Callable, Any, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def retry_with_exponential_backoff(
    func: Callable,
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    backoff_factor: float = 2.0,
    jitter: bool = True
) -> Any:
    """
    Retry a function with exponential backoff strategy.
    
    Args:
        func: The function to retry
        max_retries: Maximum number of retry attempts
        base_delay: Initial delay between retries in seconds
        max_delay: Maximum delay between retries in seconds
        backoff_factor: Multiplier for delay after each retry
        jitter: Whether to add random jitter to delays
    
    Returns:
        The result of the function call
    
    Raises:
        Exception: The last exception encountered after all retries
    """
    last_exception = None
    
    for attempt in range(max_retries + 1):
        try:
            return func()
        except Exception as e:
            last_exception = e
            logger.warning(f"Attempt {attempt + 1} failed: {str(e)}")
            
            if attempt == max_retries:
                logger.error(f"All {max_retries + 1} attempts failed. Last error: {str(e)}")
                raise last_exception
            
            # Calculate delay with exponential backoff
            delay = min(base_delay * (backoff_factor ** attempt), max_delay)
            
            # Add jitter to prevent thundering herd
            if jitter:
                delay = delay * (0.5 + random.random() * 0.5)
            
            logger.info(f"Retrying in {delay:.2f} seconds...")
            time.sleep(delay)
    
    raise last_exception

def safe_api_call(func: Callable, *args, **kwargs) -> Any:
    """
    Safely execute an API call with retry logic and proper error handling.
    
    Args:
        func: The API function to call
        *args: Positional arguments for the function
        **kwargs: Keyword arguments for the function
    
    Returns:
        The result of the API call
    
    Raises:
        Exception: If all retry attempts fail
    """
    def api_call():
        return func(*args, **kwargs)
    
    return retry_with_exponential_backoff(api_call)

def load_config(path="config/app_config.yaml"):
    with open(path, "r") as file:
        return yaml.safe_load(file)

def load_reply_data(log_path="data/logs/reply_log.csv"):
    """
    Load and parse reply log data
    """
    if not os.path.exists(log_path):
        return pd.DataFrame()
    
    try:
        with open(log_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            rows = list(reader)
            if len(rows) <= 1:
                return pd.DataFrame()
            
            data = [json.loads(row[0]) for row in rows[1:]]
            return pd.DataFrame(data)
    except Exception as e:
        print(f"Error loading data: {e}")
        return pd.DataFrame()

def create_category_chart(df):
    """
    Create a pie chart of email categories
    """
    if df.empty:
        return None
    
    category_counts = df['category'].value_counts()
    
    fig = px.pie(
        values=category_counts.values,
        names=category_counts.index,
        title="Email Categories Distribution",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    fig.update_layout(
        height=400,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    return fig

def create_timeline_chart(df):
    """
    Create a timeline chart of replies over time
    """
    if df.empty:
        return None
    
    # Convert timestamp to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['date'] = df['timestamp'].dt.date
    
    daily_counts = df.groupby('date').size().reset_index(name='count')
    
    fig = px.line(
        daily_counts,
        x='date',
        y='count',
        title="Daily Reply Generation",
        markers=True
    )
    
    fig.update_layout(
        height=300,
        xaxis_title="Date",
        yaxis_title="Number of Replies"
    )
    
    return fig

def create_intent_chart(df):
    """
    Create a bar chart of email intents
    """
    if df.empty:
        return None
    
    intent_counts = df['intent'].value_counts()
    
    fig = px.bar(
        x=intent_counts.index,
        y=intent_counts.values,
        title="Email Intent Distribution",
        color=intent_counts.values,
        color_continuous_scale='viridis'
    )
    
    fig.update_layout(
        height=400,
        xaxis_title="Intent",
        yaxis_title="Count",
        showlegend=False
    )
    
    return fig

def get_reply_statistics(df):
    """
    Calculate various statistics about replies
    """
    if df.empty:
        return {}
    
    stats = {
        'total_replies': len(df),
        'unique_categories': df['category'].nunique(),
        'unique_intents': df['intent'].nunique(),
        'avg_reply_length': df['reply'].str.len().mean(),
        'most_common_category': df['category'].mode().iloc[0] if not df['category'].mode().empty else 'None',
        'most_common_intent': df['intent'].mode().iloc[0] if not df['intent'].mode().empty else 'None'
    }
    
    return stats

def analyze_reply_quality(df):
    """
    Basic reply quality analysis
    """
    if df.empty:
        return {}
    
    # Calculate reply length statistics
    reply_lengths = df['reply'].str.len()
    
    quality_metrics = {
        'avg_length': reply_lengths.mean(),
        'min_length': reply_lengths.min(),
        'max_length': reply_lengths.max(),
        'std_length': reply_lengths.std(),
        'short_replies': len(reply_lengths[reply_lengths < 50]),
        'medium_replies': len(reply_lengths[(reply_lengths >= 50) & (reply_lengths < 200)]),
        'long_replies': len(reply_lengths[reply_lengths >= 200])
    }
    
    return quality_metrics
