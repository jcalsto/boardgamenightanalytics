import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objs as go
from plotly.subplots import make_subplots
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
    guest_df = pd.read_csv(DATA_FILENAME, parse_dates=['Date', 'RSVP date'])
    return guest_df

guest_df = get_guest_data()

def clear_input():
    st.session_state.input_name = ''
    st.query_params.clear()  # Clear query parameters

# Set the default active tab to 'Going/Invite Ratio Over Time'
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = 'Going/Invite Ratio Over Time'

# Set the tab state to View Details when 'View Details' is clicked
def set_active_tab(tab_name):
    st.session_state.active_tab = tab_name

# Calculate total invites and number of 'Going' statuses
total_invites = guest_df.groupby('Name').size().reset_index(name='Total Invites')
going_count = guest_df[guest_df['Status'] == 'Going'].groupby('Name').size().reset_index(name='Going Count')
maybe_count = guest_df[guest_df['Status'] == 'Maybe'].groupby('Name').size().reset_index(name='Maybe Count')

# Merge the dataframes to calculate the ratio
attendance_df = pd.merge(total_invites, going_count, on='Name', how='left').fillna(0)
attendance_df = pd.merge(attendance_df, maybe_count, on='Name', how='left').fillna(0)
attendance_df['Going Ratio'] = attendance_df['Going Count'] / attendance_df['Total Invites']

# Filter out attendees with fewer than 3 total invites
attendance_df = attendance_df[attendance_df['Total Invites'] > 2]

# Exclude "Jorrel Sto Tomas" for top 5 ratio calculation
filtered_attendance_df = attendance_df[attendance_df['Name'] != 'Jorrel Sto Tomas']

# Sort by the Going Ratio and select the top 5
top_5_ratio = filtered_attendance_df.sort_values(by='Going Ratio', ascending=False).head(5).reset_index(drop=True)
top_5_maybe = filtered_attendance_df.sort_values(by='Maybe Count', ascending=False).head(5).reset_index(drop=True)

# Select only the 'Name' column for display
top_5_names = top_5_ratio[['Name']]
top_5_maybe_names = top_5_maybe[['Name']]

# Calculate the combined count of 'Going' and 'Maybe' statuses
going_count_1 = guest_df[guest_df['Status'] == 'Going'].shape[0]
maybe_count_1 = guest_df[guest_df['Status'] == 'Maybe'].shape[0]

# Calculate the attendance rate including 'Going' and 'Maybe'
total_attendance = going_count_1 + maybe_count_1
attendance_rate_percentage = (total_attendance / len(guest_df)) * 100
formatted_attendance_rate = f"{attendance_rate_percentage:.2f}%"

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
    st.metric("Total Going", going_count_1)
    st.metric("Attendance Rate", formatted_attendance_rate)

with col3:
    st.write('Top 5 Most Indecisive Attendees')
    st.dataframe(top_5_maybe_names)

# Tabs for visualizations
tab1, tab2, tab3, tab4 = st.tabs(["Going/Invite Ratio Over Time", "Breakdown of Attendees", "Average Response Time", "Input Name"])

# Set the correct tab state on rerun
if st.session_state.active_tab == 'Going/Invite Ratio Over Time':
    st.select_tab(tab1)
elif st.session_state.active_tab == 'Breakdown of Attendees':
    st.select_tab(tab2)
elif st.session_state.active_tab == 'Average Response Time':
    st.select_tab(tab3)
elif st.session_state.active_tab == 'Input Name':
    st.select_tab(tab4)

with tab1:
    st.write("### Going/Invite Ratio Over Time")
    fig = go.Figure()

    # Add the data
    fig.add_trace(go.Scatter(
        x=invites_and_goings['Date'],
        y=invites_and_goings['Going/Invite Ratio'],
        mode='lines+markers',
        name='Going/Invite Ratio',
        hoverinfo='text',
        text=[f"Date: {d}<br>Ratio: {r:.2f}%" for d, r in zip(invites_and_goings['Date'], invites_and_goings['Going/Invite Ratio'])]
    ))

    # Customize the layout
    fig.update_layout(
        title="Going/Invite Ratio Over Time",
        xaxis_title="Date",
        yaxis_title="Going/Invite Ratio (%)",
        hovermode="closest"
    )

    # Show the plot
    st.plotly_chart(fig)

with tab2:
    st.write("### Breakdown of Attendees")
    fig = go.Figure(go.Bar(
        x=attendee_breakdown['Status'],
        y=attendee_breakdown['Count'],
        text=[f"Count: {count}" for count in attendee_breakdown['Count']],
        hoverinfo='text',
        marker_color='indianred'
    ))

    # Customize the layout
    fig.update_layout(
        title="Breakdown of Attendees",
        xaxis_title="Status",
        yaxis_title="Count",
        hovermode="x unified"
    )

    # Show the plot
    st.plotly_chart(fig)

with tab3:
    st.write("### Average Response Time")
    st.write(f"The average response time is {average_response_time:.2f} days.")

with tab4:
    st.write("### Input Name")
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
    query_params = st.query_params.to_dict()
    page = query_params.get("page", [None])[0]  # Default to None if "page" is not in the query params
    if page == "details":
        name = query_params.get("name", [None])[0]
        if name:
            # Make sure 'details.py' is in the same directory as this script
            exec(open("details.py").read())
    name = query_params.get("name", [None])[0]
    if name:
        # Make sure 'details.py' is in the same directory as this script
        exec(open("details.py").read())
