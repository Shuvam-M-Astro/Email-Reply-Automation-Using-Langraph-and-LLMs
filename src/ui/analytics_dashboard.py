import streamlit as st
import pandas as pd
from src.utils.helpers import (
    load_reply_data,
    create_category_chart,
    create_timeline_chart,
    create_intent_chart,
    get_reply_statistics,
    analyze_reply_quality,
)
import plotly.express as px
from datetime import datetime, timedelta

def show_analytics_page():
    """
    Display the analytics dashboard page
    """
    st.markdown('<h1 class="main-header">📊 Analytics Dashboard</h1>', unsafe_allow_html=True)
    
    # Load data
    df = load_reply_data()
    
    if df.empty:
        st.warning("📭 No reply data found. Generate some replies first to see analytics!")
        return
    
    # Convert timestamp to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Date range filter
    st.subheader("📅 Date Range Filter")
    col1, col2 = st.columns(2)
    
    with col1:
        start_date = st.date_input(
            "Start Date",
            value=df['timestamp'].min().date(),
            min_value=df['timestamp'].min().date(),
            max_value=df['timestamp'].max().date()
        )
    
    with col2:
        end_date = st.date_input(
            "End Date",
            value=df['timestamp'].max().date(),
            min_value=df['timestamp'].min().date(),
            max_value=df['timestamp'].max().date()
        )
    
    # Filter data by date range
    filtered_df = df[
        (df['timestamp'].dt.date >= start_date) & 
        (df['timestamp'].dt.date <= end_date)
    ]
    
    if filtered_df.empty:
        st.warning("No data found for the selected date range.")
        return
    
    # Key metrics
    st.subheader("📈 Key Metrics")
    
    stats = get_reply_statistics(filtered_df)
    quality_metrics = analyze_reply_quality(filtered_df)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Replies", stats.get('total_replies', 0))
    
    with col2:
        st.metric("Unique Categories", stats.get('unique_categories', 0))
    
    with col3:
        avg_length = stats.get('avg_reply_length', 0)
        st.metric("Avg Reply Length", f"{avg_length:.0f} chars")
    
    with col4:
        most_common = stats.get('most_common_category', 'None')
        st.metric("Most Common Category", most_common)
    
    # Charts
    st.subheader("📊 Visualizations")
    
    # Timeline chart
    timeline_fig = create_timeline_chart(filtered_df)
    if timeline_fig:
        st.plotly_chart(timeline_fig, use_container_width=True)
    
    # Category and Intent charts side by side
    col1, col2 = st.columns(2)
    
    with col1:
        category_fig = create_category_chart(filtered_df)
        if category_fig:
            st.plotly_chart(category_fig, use_container_width=True)
    
    with col2:
        intent_fig = create_intent_chart(filtered_df)
        if intent_fig:
            st.plotly_chart(intent_fig, use_container_width=True)
    
    # Reply quality analysis
    st.subheader("🔍 Reply Quality Analysis")
    
    if quality_metrics:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Short Replies (<50 chars)", quality_metrics.get('short_replies', 0))
        
        with col2:
            st.metric("Medium Replies (50-200 chars)", quality_metrics.get('medium_replies', 0))
        
        with col3:
            st.metric("Long Replies (>200 chars)", quality_metrics.get('long_replies', 0))
        
        # Reply length distribution
        reply_lengths = filtered_df['reply'].str.len()
        
        fig = px.histogram(
            x=reply_lengths,
            nbins=20,
            title="Reply Length Distribution",
            labels={'x': 'Reply Length (characters)', 'y': 'Count'}
        )
        
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Detailed data table
    st.subheader("📋 Detailed Data")
    
    # Add search and filter options
    col1, col2 = st.columns(2)
    
    with col1:
        category_filter = st.selectbox(
            "Filter by Category",
            ["All"] + list(filtered_df["category"].unique())
        )
    
    with col2:
        search_term = st.text_input("Search in subjects or replies", "")
    
    # Apply filters
    display_df = filtered_df.copy()
    
    if category_filter != "All":
        display_df = display_df[display_df["category"] == category_filter]
    
    if search_term:
        mask = (
            display_df["subject"].str.contains(search_term, case=False, na=False) |
            display_df["reply"].str.contains(search_term, case=False, na=False)
        )
        display_df = display_df[mask]
    
    # Show filtered data
    if not display_df.empty:
        # Select columns to display
        display_columns = ["timestamp", "subject", "category", "intent", "reply"]
        available_columns = [col for col in display_columns if col in display_df.columns]
        
        st.dataframe(
            display_df[available_columns].sort_values("timestamp", ascending=False),
            use_container_width=True,
            height=400
        )
        
        # Download option
        csv_data = display_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Filtered Data",
            data=csv_data,
            file_name=f"email_analytics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    else:
        st.info("No data matches the selected filters.")
    
    # Insights section
    st.subheader("💡 Insights")
    
    if not filtered_df.empty:
        # Most active day
        most_active_day = filtered_df.groupby(filtered_df['timestamp'].dt.date).size().idxmax()
        st.write(f"**Most Active Day:** {most_active_day} ({filtered_df.groupby(filtered_df['timestamp'].dt.date).size().max()} replies)")
        
        # Category insights
        category_dist = filtered_df['category'].value_counts()
        if len(category_dist) > 0:
            st.write(f"**Most Common Category:** {category_dist.index[0]} ({category_dist.iloc[0]} replies)")
        
        # Intent insights
        intent_dist = filtered_df['intent'].value_counts()
        if len(intent_dist) > 0:
            st.write(f"**Most Common Intent:** {intent_dist.index[0]} ({intent_dist.iloc[0]} replies)")
        
        # Reply length insights
        avg_len = filtered_df['reply'].str.len().mean()
        st.write(f"**Average Reply Length:** {avg_len:.0f} characters")
        
        # Recent activity
        recent_replies = filtered_df[filtered_df['timestamp'] >= datetime.now() - timedelta(days=7)]
        st.write(f"**Replies in Last 7 Days:** {len(recent_replies)}") 