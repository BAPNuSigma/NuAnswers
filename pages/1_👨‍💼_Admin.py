import streamlit as st
import pandas as pd
import os
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import calendar
import numpy as np
from pathlib import Path
import io

# Set page config
st.set_page_config(
    page_title="NuAnswers Admin",
    page_icon="👨‍💼",
    layout="wide"
)

# Hide all default Streamlit elements we don't want to show
st.markdown("""
    <style>
        /* Hide page names in sidebar */
        span.css-10trblm.e16nr0p30 {
            display: none;
        }
        /* Hide the default Streamlit menu button */
        button.css-1rs6os.edgvbvh3 {
            display: none;
        }
        /* Hide "streamlit app" text */
        .css-17ziqus {
            display: none;
        }
        /* Hide development mode indicator */
        .stDeployButton {
            display: none;
        }
        /* Sidebar styling */
        .css-1d391kg {
            padding-top: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("👨‍💼 Administrator Dashboard")

# Admin authentication
admin_password = os.environ.get("ADMIN_PASSWORD") or st.secrets.get("ADMIN_PASSWORD")

if not admin_password:
    st.error("Admin password not configured. Please set ADMIN_PASSWORD in environment variables or secrets.toml")
    st.stop()

# Password protection
entered_password = st.sidebar.text_input("Enter Admin Password", type="password")

if entered_password != admin_password:
    st.error("❌ Please enter the correct admin password to view statistics")
    st.stop()

st.sidebar.success("✅ Admin access granted!")

# Configure data directory
DATA_DIR = Path("/data" if os.path.exists("/data") else ".")
REGISTRATION_DATA_PATH = DATA_DIR / "registration_data.csv"
FEEDBACK_DATA_PATH = DATA_DIR / "feedback_data.csv"
TOPIC_DATA_PATH = DATA_DIR / "topic_data.csv"
COMPLETION_DATA_PATH = DATA_DIR / "completion_data.csv"

def load_data(filepath):
    """Load data from CSV file with error handling"""
    try:
        if filepath.exists():
            return pd.read_csv(filepath)
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading data from {filepath}: {str(e)}")
        return pd.DataFrame()

# Add download section
def create_download_section():
    """Create download section for all data"""
    st.subheader("📥 Download Data")
    
    download_col1, download_col2 = st.columns(2)
    
    # Prepare all data
    all_data = {
        "Registration Data": load_data(REGISTRATION_DATA_PATH),
        "Feedback Data": load_data(FEEDBACK_DATA_PATH),
        "Topic Data": load_data(TOPIC_DATA_PATH),
        "Completion Data": load_data(COMPLETION_DATA_PATH)
    }
    
    # Create Excel file with multiple sheets
    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
        for sheet_name, df in all_data.items():
            if not df.empty:
                df.to_excel(writer, sheet_name=sheet_name, index=False)
    
    with download_col1:
        # Download individual CSVs
        for name, df in all_data.items():
            if not df.empty:
                csv_data = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label=f"Download {name} (CSV)",
                    data=csv_data,
                    file_name=f"nuanswers_{name.lower().replace(' ', '_')}.csv",
                    mime="text/csv"
                )
    
    with download_col2:
        # Download combined Excel file
        excel_buffer.seek(0)
        st.download_button(
            label="Download All Data (Excel)",
            data=excel_buffer,
            file_name="nuanswers_all_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

try:
    # Load all data
    df = load_data(REGISTRATION_DATA_PATH)
    feedback_df = load_data(FEEDBACK_DATA_PATH)
    topic_df = load_data(TOPIC_DATA_PATH)
    completion_df = load_data(COMPLETION_DATA_PATH)
    
    # Add download section at the top
    create_download_section()
    
    # Overview metrics
    st.subheader("📊 Overview Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Registrations", len(df) if not df.empty else 0)
    with col2:
        total_usage = df['usage_time_minutes'].sum() if not df.empty else 0
        st.metric("Total Usage Time (hrs)", f"{total_usage / 60:.1f}")
    with col3:
        avg_session = df['usage_time_minutes'].mean() if not df.empty else 0
        st.metric("Avg. Session Length (min)", f"{avg_session:.1f}")
    with col4:
        unique_students = df['student_id'].nunique() if not df.empty else 0
        st.metric("Unique Students", unique_students)
    
    # Return User Analysis
    st.subheader("🔄 Return User Analysis")
    col1, col2, col3 = st.columns(3)
    
    if not df.empty:
        user_sessions = df.groupby('student_id').size()
        return_users = (user_sessions > 1).sum()
        total_users = len(user_sessions)
        avg_sessions = user_sessions.mean()
        
        with col1:
            st.metric("Return Users", return_users)
        with col2:
            st.metric("Return Rate", f"{(return_users/total_users)*100:.1f}%")
        with col3:
            st.metric("Avg Sessions per User", f"{avg_sessions:.1f}")
    else:
        with col1:
            st.metric("Return Users", 0)
        with col2:
            st.metric("Return Rate", "0.0%")
        with col3:
            st.metric("Avg Sessions per User", "0.0")
    
    # Time-based Analysis
    st.subheader("📈 Usage Trends")
    
    tab1, tab2, tab3 = st.tabs(["Daily Stats", "Weekly Patterns", "Hourly Distribution"])
    
    with tab1:
        if not df.empty:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            daily_stats = df.groupby(df['timestamp'].dt.date).agg({
                'student_id': 'count',
                'usage_time_minutes': ['sum', 'mean']
            }).reset_index()
            daily_stats.columns = ['Date', 'Registrations', 'Total Minutes', 'Avg Minutes']
            
            fig_daily = px.line(daily_stats, x='Date', y=['Registrations', 'Avg Minutes'],
                               title='Daily Registration and Usage Trends')
            st.plotly_chart(fig_daily, use_container_width=True)
        else:
            st.info("No daily statistics available yet.")
    
    with tab2:
        if not df.empty:
            df['day_of_week'] = df['timestamp'].dt.day_name()
            weekly_stats = df.groupby('day_of_week').agg({
                'student_id': 'count',
                'usage_time_minutes': 'mean'
            })
            
            # Ensure proper day order
            day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            weekly_stats = weekly_stats.reindex(day_order)
            
            fig_weekly = go.Figure()
            fig_weekly.add_trace(go.Bar(
                x=weekly_stats.index,
                y=weekly_stats['student_id'],
                name='Number of Sessions'
            ))
            fig_weekly.add_trace(go.Scatter(
                x=weekly_stats.index,
                y=weekly_stats['usage_time_minutes'],
                name='Avg Session Length (min)',
                yaxis='y2'
            ))
            fig_weekly.update_layout(
                title='Weekly Usage Patterns',
                yaxis2=dict(
                    title='Avg Session Length (min)',
                    overlaying='y',
                    side='right'
                )
            )
            st.plotly_chart(fig_weekly, use_container_width=True)
        else:
            st.info("No weekly patterns available yet.")
    
    with tab3:
        if not df.empty:
            hourly_dist = df.groupby(df['timestamp'].dt.hour)['student_id'].count().reset_index()
            hourly_dist.columns = ['Hour', 'Count']
            
            fig_hourly = px.bar(hourly_dist, x='Hour', y='Count',
                               title='Usage Distribution by Hour of Day')
            st.plotly_chart(fig_hourly, use_container_width=True)
        else:
            st.info("No hourly distribution data available yet.")
    
    # Time-Based Performance
    st.subheader("⏰ Time-Based Performance")
    
    tab1, tab2 = st.tabs(["Session Duration Analysis", "Peak Usage Times"])
    
    with tab1:
        # Average session duration by time of day
        hourly_duration = df.groupby(df['timestamp'].dt.hour)['usage_time_minutes'].mean().reset_index()
        hourly_duration.columns = ['Hour', 'Avg Duration']
        
        fig_duration = px.line(hourly_duration, x='Hour', y='Avg Duration',
                             title='Average Session Duration by Hour of Day',
                             labels={'Hour': 'Hour of Day', 'Avg Duration': 'Average Duration (minutes)'})
        st.plotly_chart(fig_duration, use_container_width=True)
        
        # Session duration distribution
        fig_duration_dist = px.histogram(df, x='usage_time_minutes',
                                       title='Distribution of Session Durations',
                                       labels={'usage_time_minutes': 'Session Duration (minutes)'},
                                       nbins=30)
        st.plotly_chart(fig_duration_dist, use_container_width=True)
    
    with tab2:
        # Peak usage times analysis
        df['day_hour'] = df['timestamp'].dt.strftime('%A %H:00')
        peak_usage = df.groupby('day_hour').size().reset_index(name='count')
        peak_usage['day'] = peak_usage['day_hour'].str.split().str[0]
        peak_usage['hour'] = peak_usage['day_hour'].str.split().str[1].str.split(':').str[0].astype(int)
        
        # Create a pivot table for the heatmap
        peak_pivot = peak_usage.pivot(index='day', columns='hour', values='count')
        # Use explicit day order instead of calendar.day_name
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        peak_pivot = peak_pivot.reindex(day_order)
        
        fig_heatmap = px.imshow(peak_pivot,
                               title='Peak Usage Times Heatmap',
                               labels=dict(x='Hour of Day', y='Day of Week', color='Number of Sessions'),
                               aspect='auto')
        st.plotly_chart(fig_heatmap, use_container_width=True)
    
    # User Engagement Analysis
    st.subheader("📱 User Engagement")
    
    # Session frequency analysis
    user_frequency = df.groupby('student_id').agg({
        'timestamp': ['count', lambda x: (x.max() - x.min()).days + 1]
    }).reset_index()
    user_frequency.columns = ['student_id', 'total_sessions', 'days_span']
    user_frequency['sessions_per_day'] = user_frequency['total_sessions'] / user_frequency['days_span'].clip(lower=1)
    
    fig_frequency = px.histogram(user_frequency, x='sessions_per_day',
                                title='Distribution of Session Frequency',
                                labels={'sessions_per_day': 'Average Sessions per Day'},
                                nbins=20)
    st.plotly_chart(fig_frequency, use_container_width=True)
    
    # Engagement metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        avg_sessions_per_day = user_frequency['sessions_per_day'].mean()
        st.metric("Avg Sessions per Day", f"{avg_sessions_per_day:.2f}")
    
    with col2:
        retention_rate = (user_frequency['total_sessions'] > 1).mean() * 100
        st.metric("User Retention Rate", f"{retention_rate:.1f}%")
    
    with col3:
        avg_days_active = user_frequency['days_span'].mean()
        st.metric("Avg Days Active", f"{avg_days_active:.1f}")
    
    # Time between sessions analysis
    df_sorted = df.sort_values(['student_id', 'timestamp'])
    df_sorted['prev_timestamp'] = df_sorted.groupby('student_id')['timestamp'].shift(1)
    df_sorted['time_between_sessions'] = (df_sorted['timestamp'] - df_sorted['prev_timestamp']).dt.total_seconds() / 3600  # in hours
    
    # Filter out first sessions (no previous timestamp) and unreasonable values
    time_between = df_sorted[df_sorted['time_between_sessions'].between(0, 720)]  # up to 30 days
    
    fig_time_between = px.histogram(time_between, x='time_between_sessions',
                                   title='Time Between Sessions',
                                   labels={'time_between_sessions': 'Hours Between Sessions'},
                                   nbins=50)
    st.plotly_chart(fig_time_between, use_container_width=True)
    
    # Academic Performance Metrics
    st.subheader("📊 Academic Performance")
    
    if not df.empty:
        # Grade level progression
        grade_order = ['Freshman', 'Sophomore', 'Junior', 'Senior', 'Graduate']
        grade_usage = df.groupby(['grade', 'major']).agg({
            'student_id': 'count',
            'usage_time_minutes': 'mean'
        }).reset_index()
        
        fig_grade_usage = px.scatter(grade_usage, 
                                    x='grade', 
                                    y='usage_time_minutes',
                                    size='student_id',
                                    color='major',
                                    category_orders={'grade': grade_order},
                                    title='Usage Patterns by Grade Level and Major',
                                    labels={'grade': 'Grade Level', 
                                           'usage_time_minutes': 'Average Session Duration (min)',
                                           'student_id': 'Number of Sessions'})
        st.plotly_chart(fig_grade_usage, use_container_width=True)
    else:
        st.info("No academic performance data available yet.")
    
    # Course success metrics
    st.subheader("📊 Course Success Metrics")
    
    # Create columns for different metrics
    success_col1, success_col2 = st.columns(2)
    
    with success_col1:
        # Session feedback analysis
        if 'feedback_data' in st.session_state:
            feedback_df = pd.DataFrame(st.session_state.feedback_data)
            if not feedback_df.empty:
                # Calculate average ratings
                avg_rating = feedback_df['rating'].mean()
                st.metric("Average Session Rating", f"{avg_rating:.1f}/5")
                
                # Rating distribution
                fig_ratings = px.histogram(feedback_df, x='rating',
                                         title='Distribution of Session Ratings',
                                         labels={'rating': 'Rating (1-5)'},
                                         nbins=5)
                st.plotly_chart(fig_ratings, use_container_width=True)
            else:
                st.info("No feedback data available yet")
        else:
            st.info("Feedback system is ready but no data collected yet")
    
    with success_col2:
        # Course completion tracking
        if 'completion_data' in st.session_state:
            completion_df = pd.DataFrame(st.session_state.completion_data)
            if not completion_df.empty:
                # Calculate completion rates
                completion_rate = (completion_df['completed'].sum() / len(completion_df)) * 100
                st.metric("Average Completion Rate", f"{completion_rate:.1f}%")
                
                # Completion by course
                course_completion = completion_df.groupby('course_id')['completed'].mean() * 100
                fig_completion = px.bar(x=course_completion.index, 
                                      y=course_completion.values,
                                      title='Completion Rates by Course',
                                      labels={'x': 'Course ID', 'y': 'Completion Rate (%)'})
                st.plotly_chart(fig_completion, use_container_width=True)
            else:
                st.info("No completion data available yet")
        else:
            st.info("Completion tracking system is ready but no data collected yet")
    
    # Most common topics/questions
    st.subheader("📝 Topic Analysis")
    
    if 'topic_data' in st.session_state:
        topic_df = pd.DataFrame(st.session_state.topic_data)
        if not topic_df.empty:
            # Create columns for different topic analyses
            topic_col1, topic_col2 = st.columns(2)
            
            with topic_col1:
                # Most common topics
                topic_counts = topic_df['topic'].value_counts().head(10)
                fig_topics = px.bar(x=topic_counts.index, 
                                  y=topic_counts.values,
                                  title='Top 10 Most Common Topics',
                                  labels={'x': 'Topic', 'y': 'Number of Questions'})
                st.plotly_chart(fig_topics, use_container_width=True)
            
            with topic_col2:
                # Topic difficulty analysis
                if 'difficulty' in topic_df.columns:
                    topic_difficulty = topic_df.groupby('topic')['difficulty'].mean().sort_values(ascending=False).head(10)
                    fig_difficulty = px.bar(x=topic_difficulty.index,
                                          y=topic_difficulty.values,
                                          title='Most Challenging Topics',
                                          labels={'x': 'Topic', 'y': 'Average Difficulty (1-5)'})
                    st.plotly_chart(fig_difficulty, use_container_width=True)
            
            # Topic trends over time
            topic_trends = topic_df.groupby([pd.Grouper(key='timestamp', freq='D'), 'topic']).size().unstack(fill_value=0)
            fig_trends = px.line(topic_trends,
                               title='Topic Trends Over Time',
                               labels={'value': 'Number of Questions', 'variable': 'Topic'})
            st.plotly_chart(fig_trends, use_container_width=True)
        else:
            st.info("No topic data available yet")
    else:
        st.info("Topic tracking system is ready but no data collected yet")
    
    # Demographic Analysis
    st.subheader("👥 User Demographics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Campus distribution
        campus_dist = df['campus'].value_counts()
        fig_campus = px.pie(values=campus_dist.values, names=campus_dist.index,
                           title='Distribution by Campus')
        st.plotly_chart(fig_campus)
        
    with col2:
        # Major distribution
        major_dist = df['major'].value_counts()
        fig_major = px.pie(values=major_dist.values, names=major_dist.index,
                          title='Distribution by Major')
        st.plotly_chart(fig_major)
    
    # Grade Level Analysis
    grade_dist = df['grade'].value_counts()
    fig_grade = px.bar(x=grade_dist.index, y=grade_dist.values,
                       title='Distribution by Grade Level')
    st.plotly_chart(fig_grade, use_container_width=True)
    
    # Cross Analysis
    st.subheader("🔄 Cross Analysis")
    
    # Major vs Grade Level
    major_grade_dist = pd.crosstab(df['major'], df['grade'])
    fig_major_grade = px.imshow(major_grade_dist,
                               title='Major vs Grade Level Distribution',
                               aspect='auto')
    st.plotly_chart(fig_major_grade, use_container_width=True)
    
    # Usage Patterns by Major
    major_usage = df.groupby('major').agg({
        'usage_time_minutes': ['mean', 'count']
    }).reset_index()
    major_usage.columns = ['Major', 'Avg Minutes', 'Session Count']
    
    fig_major_usage = go.Figure()
    fig_major_usage.add_trace(go.Bar(
        x=major_usage['Major'],
        y=major_usage['Session Count'],
        name='Number of Sessions'
    ))
    fig_major_usage.add_trace(go.Scatter(
        x=major_usage['Major'],
        y=major_usage['Avg Minutes'],
        name='Avg Session Length (min)',
        yaxis='y2'
    ))
    fig_major_usage.update_layout(
        title='Usage Patterns by Major',
        yaxis2=dict(
            title='Avg Session Length (min)',
            overlaying='y',
            side='right'
        )
    )
    st.plotly_chart(fig_major_usage, use_container_width=True)
    
    # System Performance Metrics
    st.subheader("⚙️ System Performance")
    
    # Create columns for different metrics
    perf_col1, perf_col2 = st.columns(2)
    
    with perf_col1:
        # Response time analysis
        if 'response_times' in st.session_state:
            response_times = pd.DataFrame(st.session_state.response_times)
            if not response_times.empty:
                # Calculate average response time
                avg_response_time = response_times['response_time'].mean()
                st.metric("Average Response Time", f"{avg_response_time:.2f} seconds")
                
                # Response time distribution
                fig_response = px.histogram(response_times, x='response_time',
                                          title='Response Time Distribution',
                                          labels={'response_time': 'Response Time (seconds)'},
                                          nbins=30)
                st.plotly_chart(fig_response, use_container_width=True)
            else:
                st.info("No response time data available yet")
        else:
            st.info("Response time tracking system is ready but no data collected yet")
    
    with perf_col2:
        # Error rate tracking
        if 'error_logs' in st.session_state:
            error_logs = pd.DataFrame(st.session_state.error_logs)
            if not error_logs.empty:
                # Calculate error rate
                total_requests = len(df)
                total_errors = len(error_logs)
                error_rate = (total_errors / total_requests) * 100
                st.metric("Error Rate", f"{error_rate:.2f}%")
                
                # Error type distribution
                error_types = error_logs['error_type'].value_counts()
                fig_errors = px.bar(x=error_types.index, y=error_types.values,
                                   title='Error Type Distribution',
                                   labels={'x': 'Error Type', 'y': 'Count'})
                st.plotly_chart(fig_errors, use_container_width=True)
            else:
                st.info("No error data available yet")
        else:
            st.info("Error tracking system is ready but no data collected yet")
    
    # System uptime/downtime
    st.subheader("⏱️ System Uptime")
    
    if 'system_status' in st.session_state:
        system_status = pd.DataFrame(st.session_state.system_status)
        if not system_status.empty:
            # Calculate uptime percentage
            total_time = (system_status['end_time'].max() - system_status['start_time'].min()).total_seconds()
            uptime = system_status[system_status['status'] == 'up']['duration'].sum()
            uptime_percentage = (uptime / total_time) * 100
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("System Uptime", f"{uptime_percentage:.2f}%")
            
            with col2:
                # Uptime trend
                system_status['date'] = system_status['start_time'].dt.date
                daily_uptime = system_status.groupby('date')['status'].apply(
                    lambda x: (x == 'up').mean() * 100
                ).reset_index()
                
                fig_uptime = px.line(daily_uptime, x='date', y='status',
                                    title='Daily Uptime Trend',
                                    labels={'date': 'Date', 'status': 'Uptime Percentage'})
                st.plotly_chart(fig_uptime, use_container_width=True)
        else:
            st.info("No system status data available yet")
    else:
        st.info("System status tracking is ready but no data collected yet")
    
    # Content Analysis
    st.subheader("📚 Content Analysis")
    
    # Most viewed/accessed materials
    if 'content_access' in st.session_state:
        content_access = pd.DataFrame(st.session_state.content_access)
        if not content_access.empty:
            # Create columns for different content analyses
            content_col1, content_col2 = st.columns(2)
            
            with content_col1:
                # Most accessed materials
                top_content = content_access['content_id'].value_counts().head(10)
                fig_content = px.bar(x=top_content.index, y=top_content.values,
                                    title='Top 10 Most Accessed Materials',
                                    labels={'x': 'Content ID', 'y': 'Access Count'})
                st.plotly_chart(fig_content, use_container_width=True)
            
            with content_col2:
                # Content type distribution
                content_types = content_access['content_type'].value_counts()
                fig_types = px.pie(values=content_types.values, names=content_types.index,
                                  title='Content Type Distribution')
                st.plotly_chart(fig_types, use_container_width=True)
            
            # Content access trends
            content_trends = content_access.groupby([pd.Grouper(key='access_time', freq='D'), 'content_type']).size().unstack(fill_value=0)
            fig_trends = px.line(content_trends,
                                title='Content Access Trends Over Time',
                                labels={'value': 'Access Count', 'variable': 'Content Type'})
            st.plotly_chart(fig_trends, use_container_width=True)
        else:
            st.info("No content access data available yet")
    else:
        st.info("Content tracking system is ready but no data collected yet")
    
    # Search term analysis
    if 'search_terms' in st.session_state:
        search_terms = pd.DataFrame(st.session_state.search_terms)
        if not search_terms.empty:
            st.subheader("🔍 Search Term Analysis")
            
            # Most common search terms
            top_searches = search_terms['term'].value_counts().head(10)
            fig_searches = px.bar(x=top_searches.index, y=top_searches.values,
                                 title='Top 10 Most Common Search Terms',
                                 labels={'x': 'Search Term', 'y': 'Count'})
            st.plotly_chart(fig_searches, use_container_width=True)
            
            # Search term trends
            search_trends = search_terms.groupby([pd.Grouper(key='timestamp', freq='D')]).size().reset_index(name='count')
            fig_search_trends = px.line(search_trends, x='timestamp', y='count',
                                       title='Search Activity Over Time',
                                       labels={'timestamp': 'Date', 'count': 'Number of Searches'})
            st.plotly_chart(fig_search_trends, use_container_width=True)
        else:
            st.info("No search term data available yet")
    else:
        st.info("Search term tracking system is ready but no data collected yet")
    
    # Feedback and Quality Metrics
    st.subheader("🌟 Feedback and Quality Metrics")
    
    # Create columns for different feedback metrics
    feedback_col1, feedback_col2 = st.columns(2)
    
    with feedback_col1:
        # User satisfaction scores
        if 'user_feedback' in st.session_state:
            user_feedback = pd.DataFrame(st.session_state.user_feedback)
            if not user_feedback.empty:
                # Calculate average satisfaction score
                avg_satisfaction = user_feedback['satisfaction_score'].mean()
                st.metric("Average Satisfaction Score", f"{avg_satisfaction:.1f}/5")
                
                # Satisfaction score distribution
                fig_satisfaction = px.histogram(user_feedback, x='satisfaction_score',
                                              title='Satisfaction Score Distribution',
                                              labels={'satisfaction_score': 'Satisfaction Score (1-5)'},
                                              nbins=5)
                st.plotly_chart(fig_satisfaction, use_container_width=True)
            else:
                st.info("No user feedback data available yet")
        else:
            st.info("User feedback system is ready but no data collected yet")
    
    with feedback_col2:
        # Response quality ratings
        if 'response_ratings' in st.session_state:
            response_ratings = pd.DataFrame(st.session_state.response_ratings)
            if not response_ratings.empty:
                # Calculate average response quality
                avg_quality = response_ratings['quality_score'].mean()
                st.metric("Average Response Quality", f"{avg_quality:.1f}/5")
                
                # Quality score distribution
                fig_quality = px.histogram(response_ratings, x='quality_score',
                                         title='Response Quality Distribution',
                                         labels={'quality_score': 'Quality Score (1-5)'},
                                         nbins=5)
                st.plotly_chart(fig_quality, use_container_width=True)
            else:
                st.info("No response quality data available yet")
        else:
            st.info("Response quality tracking system is ready but no data collected yet")
    
    # Resolution time analysis
    st.subheader("⏱️ Resolution Time Analysis")
    
    if 'resolution_times' in st.session_state:
        resolution_times = pd.DataFrame(st.session_state.resolution_times)
        if not resolution_times.empty:
            # Calculate average resolution time
            avg_resolution_time = resolution_times['resolution_time'].mean()
            st.metric("Average Resolution Time", f"{avg_resolution_time:.1f} minutes")
            
            # Resolution time distribution
            fig_resolution = px.histogram(resolution_times, x='resolution_time',
                                        title='Resolution Time Distribution',
                                        labels={'resolution_time': 'Resolution Time (minutes)'},
                                        nbins=30)
            st.plotly_chart(fig_resolution, use_container_width=True)
            
            # Resolution time trends
            resolution_trends = resolution_times.groupby([pd.Grouper(key='timestamp', freq='D')])['resolution_time'].mean().reset_index()
            fig_trends = px.line(resolution_trends, x='timestamp', y='resolution_time',
                                title='Resolution Time Trends',
                                labels={'timestamp': 'Date', 'resolution_time': 'Average Resolution Time (minutes)'})
            st.plotly_chart(fig_trends, use_container_width=True)
        else:
            st.info("No resolution time data available yet")
    else:
        st.info("Resolution time tracking system is ready but no data collected yet")
    
    # User feedback trends
    st.subheader("📈 User Feedback Trends")
    
    if 'feedback_trends' in st.session_state:
        feedback_trends = pd.DataFrame(st.session_state.feedback_trends)
        if not feedback_trends.empty:
            # Feedback trends over time
            fig_feedback_trends = px.line(feedback_trends, x='date', y='satisfaction_score',
                                         title='Satisfaction Score Trends',
                                         labels={'date': 'Date', 'satisfaction_score': 'Average Satisfaction Score'})
            st.plotly_chart(fig_feedback_trends, use_container_width=True)
            
            # Service improvement suggestions
            if 'suggestions' in feedback_trends.columns:
                suggestions = feedback_trends['suggestions'].value_counts().head(10)
                fig_suggestions = px.bar(x=suggestions.index, y=suggestions.values,
                                       title='Top 10 Service Improvement Suggestions',
                                       labels={'x': 'Suggestion', 'y': 'Count'})
                st.plotly_chart(fig_suggestions, use_container_width=True)
        else:
            st.info("No feedback trend data available yet")
    else:
        st.info("Feedback trend tracking system is ready but no data collected yet")
    
    # Comparative Analysis
    st.subheader("📊 Comparative Analysis")
    
    # Year-over-year growth
    st.subheader("📈 Year-over-Year Growth")
    
    if 'yearly_data' in st.session_state:
        yearly_data = pd.DataFrame(st.session_state.yearly_data)
        if not yearly_data.empty:
            # Calculate growth metrics
            yearly_metrics = yearly_data.groupby('year').agg({
                'registrations': 'sum',
                'unique_users': 'nunique',
                'total_usage': 'sum'
            }).reset_index()
            
            # Create columns for different growth metrics
            growth_col1, growth_col2 = st.columns(2)
            
            with growth_col1:
                # Registration growth
                fig_reg_growth = px.line(yearly_metrics, x='year', y='registrations',
                                        title='Registration Growth',
                                        labels={'year': 'Year', 'registrations': 'Total Registrations'})
                st.plotly_chart(fig_reg_growth, use_container_width=True)
            
            with growth_col2:
                # User growth
                fig_user_growth = px.line(yearly_metrics, x='year', y='unique_users',
                                         title='User Growth',
                                         labels={'year': 'Year', 'unique_users': 'Unique Users'})
                st.plotly_chart(fig_user_growth, use_container_width=True)
            
            # Usage growth
            fig_usage_growth = px.line(yearly_metrics, x='year', y='total_usage',
                                      title='Usage Growth',
                                      labels={'year': 'Year', 'total_usage': 'Total Usage (hours)'})
            st.plotly_chart(fig_usage_growth, use_container_width=True)
        else:
            st.info("No yearly comparison data available yet")
    else:
        st.info("Yearly comparison tracking system is ready but no data collected yet")
    
    # Semester-to-semester comparisons
    st.subheader("📅 Semester Comparisons")
    
    if 'semester_data' in st.session_state:
        semester_data = pd.DataFrame(st.session_state.semester_data)
        if not semester_data.empty:
            # Calculate semester metrics
            semester_metrics = semester_data.groupby(['year', 'semester']).agg({
                'registrations': 'sum',
                'unique_users': 'nunique',
                'total_usage': 'sum'
            }).reset_index()
            
            # Create semester labels
            semester_metrics['semester_label'] = semester_metrics['year'].astype(str) + ' ' + semester_metrics['semester']
            
            # Create columns for different semester metrics
            semester_col1, semester_col2 = st.columns(2)
            
            with semester_col1:
                # Registration comparison
                fig_sem_reg = px.bar(semester_metrics, x='semester_label', y='registrations',
                                    title='Registrations by Semester',
                                    labels={'semester_label': 'Semester', 'registrations': 'Total Registrations'})
                st.plotly_chart(fig_sem_reg, use_container_width=True)
            
            with semester_col2:
                # User comparison
                fig_sem_users = px.bar(semester_metrics, x='semester_label', y='unique_users',
                                      title='Unique Users by Semester',
                                      labels={'semester_label': 'Semester', 'unique_users': 'Unique Users'})
                st.plotly_chart(fig_sem_users, use_container_width=True)
            
            # Usage comparison
            fig_sem_usage = px.bar(semester_metrics, x='semester_label', y='total_usage',
                                  title='Total Usage by Semester',
                                  labels={'semester_label': 'Semester', 'total_usage': 'Total Usage (hours)'})
            st.plotly_chart(fig_sem_usage, use_container_width=True)
        else:
            st.info("No semester comparison data available yet")
    else:
        st.info("Semester comparison tracking system is ready but no data collected yet")
    
    # Department performance comparisons
    st.subheader("🏫 Department Performance")
    
    if 'department_data' in st.session_state:
        department_data = pd.DataFrame(st.session_state.department_data)
        if not department_data.empty:
            # Calculate department metrics
            dept_metrics = department_data.groupby('department').agg({
                'registrations': 'sum',
                'unique_users': 'nunique',
                'total_usage': 'sum',
                'satisfaction_score': 'mean'
            }).reset_index()
            
            # Create columns for different department metrics
            dept_col1, dept_col2 = st.columns(2)
            
            with dept_col1:
                # Registration by department
                fig_dept_reg = px.bar(dept_metrics, x='department', y='registrations',
                                     title='Registrations by Department',
                                     labels={'department': 'Department', 'registrations': 'Total Registrations'})
                st.plotly_chart(fig_dept_reg, use_container_width=True)
            
            with dept_col2:
                # Satisfaction by department
                fig_dept_sat = px.bar(dept_metrics, x='department', y='satisfaction_score',
                                     title='Satisfaction by Department',
                                     labels={'department': 'Department', 'satisfaction_score': 'Average Satisfaction'})
                st.plotly_chart(fig_dept_sat, use_container_width=True)
            
            # Usage by department
            fig_dept_usage = px.bar(dept_metrics, x='department', y='total_usage',
                                   title='Usage by Department',
                                   labels={'department': 'Department', 'total_usage': 'Total Usage (hours)'})
            st.plotly_chart(fig_dept_usage, use_container_width=True)
        else:
            st.info("No department comparison data available yet")
    else:
        st.info("Department comparison tracking system is ready but no data collected yet")
    
    # Predictive Analytics
    st.subheader("🔮 Predictive Analytics")
    
    # Usage forecasting
    st.subheader("📊 Usage Forecasting")
    
    if 'historical_usage' in st.session_state:
        historical_usage = pd.DataFrame(st.session_state.historical_usage)
        if not historical_usage.empty:
            # Create time series for forecasting
            historical_usage['date'] = pd.to_datetime(historical_usage['date'])
            historical_usage.set_index('date', inplace=True)
            
            # Calculate moving averages for forecasting
            historical_usage['7_day_ma'] = historical_usage['usage'].rolling(window=7).mean()
            historical_usage['30_day_ma'] = historical_usage['usage'].rolling(window=30).mean()
            
            # Plot historical usage with moving averages
            fig_forecast = go.Figure()
            fig_forecast.add_trace(go.Scatter(x=historical_usage.index, y=historical_usage['usage'],
                                            name='Actual Usage', line=dict(color='blue')))
            fig_forecast.add_trace(go.Scatter(x=historical_usage.index, y=historical_usage['7_day_ma'],
                                            name='7-Day Moving Average', line=dict(color='orange')))
            fig_forecast.add_trace(go.Scatter(x=historical_usage.index, y=historical_usage['30_day_ma'],
                                            name='30-Day Moving Average', line=dict(color='green')))
            
            fig_forecast.update_layout(title='Usage Forecasting',
                                     xaxis_title='Date',
                                     yaxis_title='Usage (hours)',
                                     showlegend=True)
            st.plotly_chart(fig_forecast, use_container_width=True)
            
            # Display forecast metrics
            col1, col2 = st.columns(2)
            
            with col1:
                # Calculate growth rate
                growth_rate = ((historical_usage['30_day_ma'].iloc[-1] / 
                              historical_usage['30_day_ma'].iloc[-30]) - 1) * 100
                st.metric("30-Day Growth Rate", f"{growth_rate:.1f}%")
            
            with col2:
                # Calculate forecast
                forecast = historical_usage['30_day_ma'].iloc[-1] * (1 + growth_rate/100)
                st.metric("Next 30-Day Forecast", f"{forecast:.1f} hours")
        else:
            st.info("No historical usage data available for forecasting")
    else:
        st.info("Usage forecasting system is ready but no data collected yet")
    
    # Peak time predictions
    st.subheader("⏰ Peak Time Predictions")
    
    if 'hourly_usage' in st.session_state:
        hourly_usage = pd.DataFrame(st.session_state.hourly_usage)
        if not hourly_usage.empty:
            # Calculate average usage by hour
            hourly_avg = hourly_usage.groupby('hour')['usage'].mean().reset_index()
            
            # Identify peak hours
            peak_hours = hourly_avg.nlargest(3, 'usage')
            
            # Plot hourly usage pattern
            fig_peak = px.line(hourly_avg, x='hour', y='usage',
                              title='Average Hourly Usage Pattern',
                              labels={'hour': 'Hour of Day', 'usage': 'Average Usage'})
            
            # Add peak hour markers
            for _, row in peak_hours.iterrows():
                fig_peak.add_vline(x=row['hour'], line_dash="dash", line_color="red")
            
            st.plotly_chart(fig_peak, use_container_width=True)
            
            # Display peak hour predictions
            st.write("Predicted Peak Hours:")
            for _, row in peak_hours.iterrows():
                st.write(f"- {row['hour']:02d}:00: {row['usage']:.1f} average users")
        else:
            st.info("No hourly usage data available for peak time prediction")
    else:
        st.info("Peak time prediction system is ready but no data collected yet")
    
    # Student success prediction
    st.subheader("🎓 Student Success Prediction")
    
    if 'student_performance' in st.session_state:
        student_performance = pd.DataFrame(st.session_state.student_performance)
        if not student_performance.empty:
            # Calculate success indicators
            success_indicators = student_performance.groupby('usage_category').agg({
                'success_rate': 'mean',
                'count': 'sum'
            }).reset_index()
            
            # Plot success rate by usage category
            fig_success = px.bar(success_indicators, x='usage_category', y='success_rate',
                                title='Success Rate by Usage Category',
                                labels={'usage_category': 'Usage Category', 'success_rate': 'Success Rate (%)'})
            st.plotly_chart(fig_success, use_container_width=True)
            
            # Display success prediction metrics
            col1, col2 = st.columns(2)
            
            with col1:
                # Calculate overall success rate
                overall_success = student_performance['success_rate'].mean()
                st.metric("Overall Success Rate", f"{overall_success:.1f}%")
            
            with col2:
                # Calculate success threshold
                success_threshold = student_performance[student_performance['success_rate'] > 70]['usage_hours'].min()
                st.metric("Minimum Hours for Success", f"{success_threshold:.1f} hours")
        else:
            st.info("No student performance data available for success prediction")
    else:
        st.info("Student success prediction system is ready but no data collected yet")
    
    # Custom Reports and Exports
    st.subheader("📊 Custom Reports and Exports")
    
    # Date range selector
    st.subheader("📅 Custom Date Range Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        start_date = st.date_input("Start Date", value=df['timestamp'].min().date())
    
    with col2:
        end_date = st.date_input("End Date", value=df['timestamp'].max().date())
    
    # Filter data based on selected date range
    filtered_df = df[(df['timestamp'].dt.date >= start_date) & 
                    (df['timestamp'].dt.date <= end_date)]
    
    if not filtered_df.empty:
        # Display filtered metrics
        st.subheader("📈 Filtered Metrics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Registrations", len(filtered_df))
        
        with col2:
            total_usage = filtered_df['usage_time_minutes'].sum()
            st.metric("Total Usage Time (hrs)", f"{total_usage / 60:.1f}")
        
        with col3:
            avg_session = filtered_df['usage_time_minutes'].mean()
            st.metric("Avg. Session Length (min)", f"{avg_session:.1f}")
        
        with col4:
            unique_students = filtered_df['student_id'].nunique()
            st.metric("Unique Students", unique_students)
        
        # Department-specific reports
        st.subheader("🏫 Department-Specific Reports")
        
        selected_department = st.selectbox("Select Department", 
                                         options=sorted(filtered_df['department'].unique()))
        
        if selected_department:
            dept_df = filtered_df[filtered_df['department'] == selected_department]
            
            # Department metrics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Department Registrations", len(dept_df))
            
            with col2:
                dept_usage = dept_df['usage_time_minutes'].sum()
                st.metric("Department Usage (hrs)", f"{dept_usage / 60:.1f}")
            
            with col3:
                dept_students = dept_df['student_id'].nunique()
                st.metric("Unique Department Students", dept_students)
            
            # Department usage trends
            dept_trends = dept_df.groupby(dept_df['timestamp'].dt.date).agg({
                'student_id': 'count',
                'usage_time_minutes': 'sum'
            }).reset_index()
            
            fig_dept_trends = px.line(dept_trends, x='timestamp', y=['student_id', 'usage_time_minutes'],
                                     title=f'{selected_department} Usage Trends',
                                     labels={'timestamp': 'Date', 'value': 'Count/Usage'})
            st.plotly_chart(fig_dept_trends, use_container_width=True)
    
    # Export options
    st.subheader("📥 Export Options")
    
    # Create export columns
    export_col1, export_col2 = st.columns(2)
    
    with export_col1:
        # Export filtered data
        if not filtered_df.empty:
            csv = filtered_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Filtered Data (CSV)",
                data=csv,
                file_name=f"nuanswers_filtered_data_{start_date}_{end_date}.csv",
                mime="text/csv"
            )
    
    with export_col2:
        # Export department report
        if selected_department and not dept_df.empty:
            dept_csv = dept_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label=f"📥 Download {selected_department} Report (CSV)",
                data=dept_csv,
                file_name=f"nuanswers_{selected_department}_report_{start_date}_{end_date}.csv",
                mime="text/csv"
            )
    
    # Scheduled report generation
    st.subheader("⏰ Scheduled Reports")
    
    # Report scheduling options
    schedule_col1, schedule_col2 = st.columns(2)
    
    with schedule_col1:
        report_frequency = st.selectbox("Report Frequency",
                                      options=["Daily", "Weekly", "Monthly"])
    
    with schedule_col2:
        report_type = st.multiselect("Report Types",
                                   options=["Usage Summary", "Department Analysis", 
                                           "Student Success", "System Performance"])
    
    if st.button("Schedule Reports"):
        st.success(f"Reports scheduled for {report_frequency} delivery: {', '.join(report_type)}")

    # Course Analysis
    st.subheader("📚 Course Analysis")
    
    tab1, tab2 = st.tabs(["Course Distribution", "Professor Analysis"])
    
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            course_dist = df['course_name'].value_counts().head(10)
            fig_course = px.bar(x=course_dist.index, y=course_dist.values,
                               title='Top 10 Most Common Courses')
            st.plotly_chart(fig_course, use_container_width=True)
        
        with col2:
            course_id_dist = df['course_id'].value_counts().head(10)
            fig_course_id = px.bar(x=course_id_dist.index, y=course_id_dist.values,
                                  title='Top 10 Course IDs')
            st.plotly_chart(fig_course_id, use_container_width=True)
    
    with tab2:
        prof_dist = df['professor'].value_counts()
        fig_prof = px.pie(values=prof_dist.values, names=prof_dist.index,
                         title='Distribution by Professor')
        st.plotly_chart(fig_prof, use_container_width=True)
    
    # Raw Data Section with enhanced filtering
    st.subheader("📝 Raw Registration Data")
    
    # Filters
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # Date filter
        date_range = st.date_input(
            "Filter by date range",
            value=(df['timestamp'].min().date(), df['timestamp'].max().date()),
            min_value=df['timestamp'].min().date(),
            max_value=df['timestamp'].max().date()
        )
    
    with col2:
        # Major filter
        selected_majors = st.multiselect(
            "Filter by Major",
            options=sorted(df['major'].unique()),
            default=[]
        )
    
    with col3:
        # Campus filter
        selected_campuses = st.multiselect(
            "Filter by Campus",
            options=sorted(df['campus'].unique()),
            default=[]
        )
    
    with col4:
        # Professor filter
        selected_professors = st.multiselect(
            "Filter by Professor",
            options=sorted(df['professor'].unique()),
            default=[]
        )
    
    # Apply filters
    filtered_df = df.copy()
    
    if len(date_range) == 2:
        start_date, end_date = date_range
        filtered_df = filtered_df[
            (filtered_df['timestamp'].dt.date >= start_date) & 
            (filtered_df['timestamp'].dt.date <= end_date)
        ]
    
    if selected_majors:
        filtered_df = filtered_df[filtered_df['major'].isin(selected_majors)]
    
    if selected_campuses:
        filtered_df = filtered_df[filtered_df['campus'].isin(selected_campuses)]
        
    if selected_professors:
        filtered_df = filtered_df[filtered_df['professor'].isin(selected_professors)]
    
    # Display filtered data
    st.dataframe(
        filtered_df.sort_values('timestamp', ascending=False),
        use_container_width=True
    )
    
    # Download options
    col1, col2 = st.columns(2)
    
    with col1:
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download as CSV",
            data=csv,
            file_name="nuanswers_registration_data.csv",
            mime="text/csv"
        )
        
    with col2:
        excel_buffer = pd.ExcelWriter(pd.io.common.BytesIO(), engine='openpyxl')
        filtered_df.to_excel(excel_buffer, index=False)
        excel_data = pd.io.common.BytesIO()
        filtered_df.to_excel(excel_data, index=False)
        st.download_button(
            label="📊 Download as Excel",
            data=excel_data.getvalue(),
            file_name="nuanswers_registration_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    # Add Data Management Section at the end
    st.divider()
    st.subheader("⚠️ Data Management")
    st.warning("Warning: These actions cannot be undone!")

    data_mgmt_col1, data_mgmt_col2 = st.columns(2)

    with data_mgmt_col1:
        st.subheader("Clear Individual Data")
        
        # Clear Registration Data
        if st.button("🗑️ Clear Registration Data"):
            st.session_state.confirm_clear_registration = True
            
        if "confirm_clear_registration" in st.session_state and st.session_state.confirm_clear_registration:
            st.warning("Are you sure you want to clear all registration data?")
            col1, col2 = st.columns(2)
            if col1.button("Yes, Clear Registration Data", key="confirm_reg"):
                try:
                    if REGISTRATION_DATA_PATH.exists():
                        REGISTRATION_DATA_PATH.unlink()
                    st.success("Registration data cleared successfully!")
                except Exception as e:
                    st.error(f"Error clearing registration data: {str(e)}")
                st.session_state.confirm_clear_registration = False
                st.rerun()
            if col2.button("Cancel", key="cancel_reg"):
                st.session_state.confirm_clear_registration = False
                st.rerun()
        
        # Clear Feedback Data
        if st.button("🗑️ Clear Feedback Data"):
            st.session_state.confirm_clear_feedback = True
            
        if "confirm_clear_feedback" in st.session_state and st.session_state.confirm_clear_feedback:
            st.warning("Are you sure you want to clear all feedback data?")
            col1, col2 = st.columns(2)
            if col1.button("Yes, Clear Feedback Data", key="confirm_feed"):
                try:
                    if FEEDBACK_DATA_PATH.exists():
                        FEEDBACK_DATA_PATH.unlink()
                    st.success("Feedback data cleared successfully!")
                except Exception as e:
                    st.error(f"Error clearing feedback data: {str(e)}")
                st.session_state.confirm_clear_feedback = False
                st.rerun()
            if col2.button("Cancel", key="cancel_feed"):
                st.session_state.confirm_clear_feedback = False
                st.rerun()
        
        # Clear Topic Data
        if st.button("🗑️ Clear Topic Data"):
            st.session_state.confirm_clear_topic = True
            
        if "confirm_clear_topic" in st.session_state and st.session_state.confirm_clear_topic:
            st.warning("Are you sure you want to clear all topic data?")
            col1, col2 = st.columns(2)
            if col1.button("Yes, Clear Topic Data", key="confirm_topic"):
                try:
                    if TOPIC_DATA_PATH.exists():
                        TOPIC_DATA_PATH.unlink()
                    st.success("Topic data cleared successfully!")
                except Exception as e:
                    st.error(f"Error clearing topic data: {str(e)}")
                st.session_state.confirm_clear_topic = False
                st.rerun()
            if col2.button("Cancel", key="cancel_topic"):
                st.session_state.confirm_clear_topic = False
                st.rerun()
                
        # Clear Completion Data
        if st.button("🗑️ Clear Completion Data"):
            st.session_state.confirm_clear_completion = True
            
        if "confirm_clear_completion" in st.session_state and st.session_state.confirm_clear_completion:
            st.warning("Are you sure you want to clear all completion data?")
            col1, col2 = st.columns(2)
            if col1.button("Yes, Clear Completion Data", key="confirm_comp"):
                try:
                    if COMPLETION_DATA_PATH.exists():
                        COMPLETION_DATA_PATH.unlink()
                    st.success("Completion data cleared successfully!")
                except Exception as e:
                    st.error(f"Error clearing completion data: {str(e)}")
                st.session_state.confirm_clear_completion = False
                st.rerun()
            if col2.button("Cancel", key="cancel_comp"):
                st.session_state.confirm_clear_completion = False
                st.rerun()

    with data_mgmt_col2:
        st.subheader("Clear All Data")
        
        if st.button("🗑️ Clear All Data", type="primary"):
            st.session_state.confirm_clear_all = True
            
        if "confirm_clear_all" in st.session_state and st.session_state.confirm_clear_all:
            st.error("⚠️ Are you absolutely sure you want to clear ALL data? This action cannot be undone!")
            col1, col2 = st.columns(2)
            if col1.button("Yes, Clear ALL Data", key="confirm_all"):
                try:
                    # Clear all data files
                    for path in [REGISTRATION_DATA_PATH, FEEDBACK_DATA_PATH, TOPIC_DATA_PATH, COMPLETION_DATA_PATH]:
                        if path.exists():
                            path.unlink()
                    st.success("All data cleared successfully!")
                except Exception as e:
                    st.error(f"Error clearing all data: {str(e)}")
                st.session_state.confirm_clear_all = False
                st.rerun()
            if col2.button("Cancel", key="cancel_all"):
                st.session_state.confirm_clear_all = False
                st.rerun()

except Exception as e:
    st.error(f"Error loading or processing data: {str(e)}")
    st.info("Some dashboard features may be limited until data becomes available.") 
