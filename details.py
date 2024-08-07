import streamlit as st
import pandas as pd
import math
from pathlib import Path

@st.cache_data
def get_guest_data():
    """Grab guest list data to be used over and over again"""
    DATA_FILENAME = Path(__file__).parent / 'data/Main_Guest_Table.csv'
    raw_guest_df = pd.read_csv(DATA_FILENAME, parse_dates=['Date', 'RSVP date'])
    guest_df = raw_guest_df
    return guest_df

guest_df = get_guest_data()

# Define the weights for each RSVP status
weights = {
    'Going': 0.9,
    'Maybe': 0.5,
    'Can\'t Go': 0.1}

# Function to calculate attendance likelihood
def calculate_attendance_likelihood(status):
    return weights.get(status, 0)  # Default to 0 if the status is not recognized

# Apply the function to the Main Guest Table dataframe to calculate attendance likelihood for each guest
guest_df['Attendance Likelihood'] = guest_df['Status'].apply(calculate_attendance_likelihood)

# Get the name from query params
query_params = st.query_params.to_dict()
name = query_params.get("name", [None])

if name:
    st.title(f"Information for {name}")
    
    # Filter the dataframe for the specific guest
    filtered_df = guest_df[guest_df['Name'].str.lower() == name.lower()]
    
    if not filtered_df.empty:
        # Calculate metrics
        total_invites = len(filtered_df)
        attended_events = filtered_df['Status'].isin(['Going', 'Maybe']).sum()
        going_events = filtered_df['Status'].eq('Going').sum()
        maybe_events = filtered_df['Status'].eq('Maybe').sum()
        attend_chance = filtered_df['Attendance Likelihood'].mean()
        formatted_attend_chance = f"{attend_chance * 100:.2f}%"
        
        if total_invites > 0:
            attendance_rate = attended_events / total_invites
            formatted_attendance_rate = f"{attendance_rate * 100:.2f}%"
        else:
            formatted_attendance_rate = "N/A"
        
        # Calculate average response time
        filtered_df['ResponseTime'] = (filtered_df['Date'] - filtered_df['RSVP date'].dt.normalize()).dt.days
        average_response_time = filtered_df['ResponseTime'].mean()
        
        # Create three columns
        col1, col2, col3 = st.columns(3)

        # Column 1: Attendance metrics
        with col1:
            st.subheader("Attendance Metrics")
            st.metric("Personal Attendance Rate", formatted_attendance_rate)
            st.metric("Total Invites", total_invites)
            st.metric("Events Attended", attended_events)
            st.metric("Chance of Attending Next Event", formatted_attend_chance)

        # Column 2: Event breakdown
        with col2:
            st.subheader("Event Breakdown")
            st.metric("'Going' Events", going_events)
            st.metric("'Maybe' Events", maybe_events)
            st.metric("Missed Events", total_invites - attended_events)

        # Column 3: Recent activity
        with col3:
            st.subheader("Recent Activity")
            recent_events = filtered_df.sort_values('Date', ascending=False).head(5)
            for _, event in recent_events.iterrows():
                st.write(f"{event['Date']}: {event['Status']}")
            st.write(f"Average Response Time: {average_response_time:.2f} days")

        st.dataframe(filtered_df.reset_index(drop=True))

    else:
        st.write(f"No data found for {name}")
else:
    st.write("No name provided")
