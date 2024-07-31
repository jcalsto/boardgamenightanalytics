import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='Board Game Night Analytics!',
    page_icon=':game_die:',  # This is an emoji shortcode. Could be a URL too.
)

# -----------------------------------------------------------------------------
# Declare some useful functions.

@st.cache_data
def get_guest_data():
    """Grab guest list data to be used over and over again"""
    # Instead of a CSV on disk, you could read from an HTTP endpoint here too.
    DATA_FILENAME = Path(__file__).parent / 'data/Main_Guest_Table.csv'

guest_df = get_guest_data()

def clear_input():
    st.session_state.input_name = ''
    st.query_params.clear()  # Clear query parameters

# Calculate total invites and number of 'Going' statuses by Date
total_invites_by_date = guest_df.groupby('Date').size().reset_index(name='Total Invites')
going_count_by_date = guest_df[guest_df['Status'] == 'Going'].groupby('Date').size().reset_index(name='Going Count')

# Merge the dataframes for invites and going counts by Date
invites_and_goings = pd.merge(total_invites_by_date, going_count_by_date, on='Date', how='left').fillna(0)
invites_and_goings['Going/Invite Ratio'] = (invites_and_goings['Going Count'] / invites_and_goings['Total Invites']) * 100

# Calculate the breakdown of attendees
attendee_breakdown = guest_df['Status'].value_counts().reset_index(name='Count')
attendee_breakdown.columns = ['Status', 'Count']

# Calculate average response time
guest_df['ResponseTime'] = (guest_df['Date'] - guest_df['RSVP date']).dt.days
average_response_time = guest_df['ResponseTime'].mean()

# -----------------------------------------------------------------------------
# Draw the actual page
# Set the title that appears at the top of the page.
st.title('🎲 Board Game Night Analytics! 🎲')

'''
All data is exported from the guest lists from my [Partiful Invites](https://www.partiful.com/). The data in this,
just reflects up until board game night that was on July 18. This dashboard will evolve as I add more filtering and inputs.
'''

st.subheader('Fun General Event Metrics')
col1, col2, col3 = st.columns(3)

with col1:
    st.write('Top 5 Regulars (2+ events):')
    st.dataframe(top_5_names)

with col2:
    st.write('Overall Attendance Metrics')
    st.metric("Total Invites", len(guest_df))
    st.metric("Total Going", len(guest_df[guest_df['Status'] == 'Going']))
    st.metric("Attendance Rate", formatted_attendance_rate)

with col3:
    st.write('Top 5 Most Indecisive Attendees')
    st.dataframe(top_5_maybe_names)

# Tabs for visualizations
tab1, tab2, tab3 = st.tabs(["Going/Invite Ratio Over Time", "Breakdown of Attendees", "Average Response Time"])

with tab1:
    st.write("### Going/Invite Ratio Over Time")
    st.line_chart(invites_and_goings.set_index('Date')['Going/Invite Ratio'])

with tab2:
    st.write("### Breakdown of Attendees")
    fig, ax = plt.subplots()
    ax.pie(attendee_breakdown['Count'], labels=attendee_breakdown['Status'], autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    st.pyplot(fig)

with tab3:
    st.write("### Average Response Time")
    st.write(f"The average response time is {average_response_time:.2f} days.")

# Add some spacing
st.write("")
st.write("")

if 'input_name' not in st.session_state:
    st.session_state.input_name = ''

# Input box for user to filter DataFrame
input_name = st.text_input('Enter your name to check the events you went to! (check Partiful if your name does not pop up!):',
                           value=st.session_state.input_name, 
                           on_change=clear_input)

# Check if the name exists in the DataFrame
valid_name = False
if input_name:
    valid_name = not guest_df[guest_df['Name'].str.lower() == input_name.lower()].empty

# Create a placeholder for validation result
validation_result = st.empty()

col1, col2 = st.columns(2)

with col1:
    # Modify the submit button and navigation logic
    if st.button("View Details"):
        if valid_name:
            # Navigate to the detailed information page with the provided name
            st.query_params.page = "details"
            st.query_params.name = input_name
            st.rerun()  # This will rerun the script with the new query parameters
        else:
            validation_result.error("Name not found. Please check the spelling or try again.")

with col2:
    if st.button("Clear"):
        st.session_state.input_name = ''
        st.query_params.clear()  # Clear query parameters
        st.rerun()  # This will rerun the script and clear the input

# Page navigation based on query params
if st.query_params.page == "details":
    name = st.query_params.get("name", None)
    if name:
        # Make sure 'details.py' is in the same directory as this script
        exec(open("details.py").read())
