import streamlit as st
import pandas as pd
import math
from pathlib import Path

@st.cache_data
def get_guest_data():
    """Grab guest list data to be used over and over again
    """

    # Instead of a CSV on disk, you could read from an HTTP endpoint here too.
    DATA_FILENAME = Path(__file__).parent/'data/Main_Guest_Table.csv'
    raw_guest_df = pd.read_csv(DATA_FILENAME)

    guest_df = raw_guest_df

    return guest_df

guest_df = get_guest_data()

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
        
        if total_invites > 0:
            attendance_rate = attended_events / total_invites
            formatted_attendance_rate = f"{attendance_rate * 100:.2f}%"
        else:
            formatted_attendance_rate = "N/A"

        # Create three columns
        col1, col2, col3 = st.columns(3)

        # Column 1: Attendance metrics
        with col1:
            st.subheader("Attendance Metrics")
            st.metric("Personal Attendance Rate", formatted_attendance_rate)
            st.metric("Total Invites", total_invites)
            st.metric("Events Attended", attended_events)

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

        st.dataframe(filtered_guest_df.reset_index(drop=True))

    else:
        st.write(f"No data found for {name}")
else:
    st.write("No name provided")
