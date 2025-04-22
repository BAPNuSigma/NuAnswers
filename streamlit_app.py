import os
import datetime
import pandas as pd
import streamlit as st

# Function to save user data and usage time
def save_user_data(user_data, usage_time):
    # Use Render's persistent storage directory
    data_dir = "/opt/render/project/src/user_data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    # Create or load the CSV file
    csv_path = os.path.join(data_dir, "user_registrations.csv")
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
    else:
        df = pd.DataFrame(columns=[
            "timestamp", "full_name", "student_id", "email", "grade", "campus",
            "major", "course_name", "course_id", "professor", "usage_time_minutes"
        ])
    
    # Add new user data
    new_row = {
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "full_name": user_data["full_name"],
        "student_id": user_data["student_id"],
        "email": user_data["email"],
        "grade": user_data["grade"],
        "campus": user_data["campus"],
        "major": user_data["major"],
        "course_name": user_data["course_name"],
        "course_id": user_data["course_id"],
        "professor": user_data["professor"],
        "usage_time_minutes": usage_time
    }
    
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(csv_path, index=False)
    
    # Also save to a timestamped file for backup
    backup_path = os.path.join(data_dir, f"user_registrations_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
    df.to_csv(backup_path, index=False)

# Add a download button for administrators
if st.session_state.registered:
    # Add a section for administrators
    st.sidebar.title("Administrator Tools")
    
    # Get admin password from environment variable or secrets
    admin_password = os.environ.get("ADMIN_PASSWORD") or st.secrets.get("ADMIN_PASSWORD")
    
    if not admin_password:
        st.sidebar.error("Admin password not configured. Please set ADMIN_PASSWORD in environment variables or secrets.toml")
        st.stop()
    
    # Password protection for admin access
    entered_password = st.sidebar.text_input("Enter Admin Password", type="password")
    
    if entered_password == admin_password:
        st.sidebar.success("Admin access granted!")
        
        # Download button for the CSV file
        data_dir = "/opt/render/project/src/user_data"
        csv_path = os.path.join(data_dir, "user_registrations.csv")
        if os.path.exists(csv_path):
            with open(csv_path, "rb") as f:
                st.sidebar.download_button(
                    label="📥 Download User Data",
                    data=f,
                    file_name="user_registrations.csv",
                    mime="text/csv"
                )
        
        # Display the most recent entries
        st.sidebar.subheader("Recent Registrations")
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            st.sidebar.dataframe(df.tail(5))  # Show last 5 entries
    elif entered_password:  # Only show error if a password was entered
        st.sidebar.error("Incorrect password") 