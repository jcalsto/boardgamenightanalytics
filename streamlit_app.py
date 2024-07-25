import streamlit as st
import pandas as pd
from pathlib import Path

# Function to load data
@st.cache_data
def get_guest_data():
    DATA_FILENAME = Path(__file__).parent/'data/Main_Guest_Table.csv'
    return pd.read_csv(DATA_FILENAME)

# Load the data
guest_df = get_guest_data()

# Set page config
st.set_page_config(page_title="Board Game Night Analytics", page_icon=":game_die:")

# Navigation
page = st.sidebar.selectbox("Choose a page", ["Home", "General Metrics", "Personal Metrics"])

if page == "Home":
    st.title("Board Game Night Analytics")
    st.write("Welcome to the Board Game Night Analytics dashboard. Use the sidebar to navigate between pages.")

elif page == "General Metrics":
    st.title("General Metrics")
    
    # Your existing code for general metrics goes here
    # For example:
    attendance_rate_percentage = ((guest_df['Status'].isin(['Going', 'Maybe']).sum()) / len(guest_df)) * 100
    formatted_attendance_rate = f"{attendance_rate_percentage:.2f}%"
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Invites", len(guest_df))
    with col2:
        st.metric("Total Going", len(guest_df[guest_df['Status'] == 'Going']))
    with col3:
        st.metric("Overall Attendance Rate", formatted_attendance_rate)
    
    # Add more general metrics as needed

elif page == "Personal Metrics":
    st.title("Personal Metrics")
    
    # Input for user name
    name = st.text_input("Enter your name:")
    
    if name:
        # Filter data for the specific user
        user_data = guest_df[guest_df['Name'].str.lower() == name.lower()]
        
        if not user_data.empty:
            # Calculate personal metrics
            total_invites = len(user_data)
            attended_events = user_data['Status'].isin(['Going', 'Maybe']).sum()
            personal_attendance_rate = (attended_events / total_invites) * 100 if total_invites > 0 else 0
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Personal Invites", total_invites)
            with col2:
                st.metric("Events Attended", attended_events)
            with col3:
                st.metric("Personal Attendance Rate", f"{personal_attendance_rate:.2f}%")
            
            # Display recent activity
            st.subheader("Recent Activity")
            st.dataframe(user_data.sort_values('Date', ascending=False).head())
        else:
            st.write("No data found for this name.")
    else:
        st.write("Please enter a name to view personal metrics.")
