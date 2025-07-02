import yaml
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
import json
import csv
import os

def load_config(path="config.yaml"):
    with open(path, "r") as file:
        return yaml.safe_load(file)

def load_reply_data(log_path="logs/reply_log.csv"):
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
