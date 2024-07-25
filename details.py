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
query_params = st.query_params()
name = query_params.get("name", [None])[0]

if name:
    st.title(f"Information for {name}")
    filtered_df = guest_df[guest_df['Name'].str.lower() == name.lower()]
    st.dataframe(filtered_df)

    # Calculate the attendance rate
    attendance_rate = (guest_df['Status'].isin(['Going', 'Maybe']).sum()) / len(guest_df)
    formatted_attendance_rate = f"{attendance_rate * 100:.2f}%"
    st.metric("Attendance Rate", formatted_attendance_rate)
