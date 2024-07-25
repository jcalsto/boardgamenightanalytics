import streamlit as st
import pandas as pd
import math
from pathlib import Path

<<<<<<< HEAD
# Set page config first
st.set_page_config(page_title="Board Game Night Analytics", page_icon=":game_die:")

# Function to load data
=======
# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='Board Game Night Analytics!',
    page_icon=':game_die:', # This is an emoji shortcode. Could be a URL too.
)

# -----------------------------------------------------------------------------
# Declare some useful functions.

>>>>>>> parent of 36969af (Update streamlit_app.py complete rewrite with pages instead)
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

<<<<<<< HEAD
# Navigation
page = st.sidebar.selectbox("Choose a page", ["Home", "General Metrics", "Personal Metrics"])
=======
def clear_input():
    st.session_state.input_name = ''
    st.session_state.selected_name = ''

def clear_select():
    st.session_state.input_name = ''
    st.session_state.selected_name = st.session_state.dropdown_name
>>>>>>> parent of 36969af (Update streamlit_app.py complete rewrite with pages instead)

# Calculate total invites and number of 'Going' statuses
total_invites = guest_df.groupby('Name').size().reset_index(name='Total Invites')
going_count = guest_df[guest_df['Status'] == 'Going'].groupby('Name').size().reset_index(name='Going Count')
maybe_count = guest_df[guest_df['Status'] == 'Maybe'].groupby('Name').size().reset_index(name='Maybe Count')

<<<<<<< HEAD
elif page == "General Metrics":
    st.title("General Metrics")
    
    # Your existing code for general metrics goes here
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
=======
>>>>>>> parent of 36969af (Update streamlit_app.py complete rewrite with pages instead)

# Merge the dataframes to calculate the ratio
attendance_df = pd.merge(total_invites, going_count, on='Name', how='left').fillna(0)
attendance_df = pd.merge(attendance_df, maybe_count, on='Name', how='left').fillna(0)
attendance_df['Going Ratio'] = attendance_df['Going Count'] / attendance_df['Total Invites']

attendance_df = attendance_df[attendance_df['Total Invites'] > 2]

filtered_attendance_df = attendance_df[attendance_df['Name'] != 'Jorrel Sto Tomas']
attendance_rate_percentage = ((guest_df['Status'].isin(['Going', 'Maybe']).sum()) / len(guest_df)) * 100
formatted_attendance_rate = f"{attendance_rate_percentage:.2f}%"

# Sort by the Going Ratio and select the top 5
top_5_ratio = filtered_attendance_df.sort_values(by='Going Ratio', ascending=False).head(5).reset_index()
top_5_maybe = filtered_attendance_df.sort_values(by='Maybe Count', ascending=False).head(5).reset_index()

# Select only the 'Name' column for display
top_5_names = top_5_ratio[['Name']]
top_5_maybe_names = top_5_maybe[['Name']]

# -----------------------------------------------------------------------------
# Draw the actual page

# Set the title that appears at the top of the page.
'''
# :game_die: Board Game Night Analytics!:game_die:

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

# Add some spacing
''
''

if 'input_name' not in st.session_state:
    st.session_state.input_name = ''
if 'selected_name' not in st.session_state:
    st.session_state.selected_name = ''
if 'toggle' not in st.session_state:
    st.session_state.toggle = 'You know your name'

# Toggle between input methods
toggle = st.radio('How you wanna do this?', ('You know your name', 'Look for it'), index=0 if st.session_state.toggle == 'Input' else 1)
st.session_state.toggle = toggle

# Filter the DataFrame based on the toggle
if toggle == 'You know your name':
    # Input box for user to filter DataFrame
    input_name = st.text_input('Enter your name to check the events you went to! (check Partiful if your name does not pop up!):',
                                  value=st.session_state.input_name, 
                                   on_change=clear_input)
    # Filter the Dataframe based on input
    if input_name:
        filtered_guest_df = guest_df[guest_df['Name'].str.lower() == input_name.lower()]
    else:
<<<<<<< HEAD
        st.write("Please enter a name to view personal metrics.")

# You can add more pages as needed
=======
        filtered_guest_df = guest_df
    
else:
    # Dropdown menu for user to select a name to filter the DataFrame
    name_options = [''] + guest_df['Name'].unique().tolist()
    selected_name = st.selectbox('Look for your name or some other person from the list!', 
                             options=name_options, 
                             index=name_options.index(st.session_state.selected_name) if st.session_state.selected_name in name_options else 0, 
                             on_change=clear_select, 
                             key='dropdown_name')

    if selected_name:
        filtered_guest_df = guest_df[guest_df['Name'] == selected_name]
    else:
        filtered_guest_df = guest_df

# Update session state
st.session_state.input_name = input_name if toggle == 'You know your name' else ''
st.session_state.selected_name = selected_name if toggle == 'Look for it' else ''

# Display the filtered Dataframe
guest_list = st.dataframe(filtered_guest_df.reset_index(drop=True))

# Modify the submit button and navigation logic
if st.button("View Details"):
    name_to_use = ""
    if toggle == 'You know your name':
        name_to_use = input_name
    else:
        name_to_use = selected_name
    
    if name_to_use:
        # Navigate to the detailed information page with the provided name
        st.query_params.page = "details"
        st.query_params.name = name_to_use
        st.rerun()  # This will rerun the script with the new query parameters

# Page navigation based on query params
query_params = st.query_params.to_dict()
if query_params.get("page") == "details":
    name = query_params.get("name")
    if name:
        # Make sure 'details.py' is in the same directory as this script
        exec(open("details.py").read())

>>>>>>> parent of 36969af (Update streamlit_app.py complete rewrite with pages instead)
