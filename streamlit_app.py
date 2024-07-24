import streamlit as st
import pandas as pd
import math
from pathlib import Path

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='Board Game Night Analytics!',
    page_icon=':game_die:', # This is an emoji shortcode. Could be a URL too.
)

# -----------------------------------------------------------------------------
# Declare some useful functions.

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

def clear_input():
    st.session_state.input_name = ''
    st.session_state.selected_name = ''

def clear_select():
    st.session_state.input_name = ''
    st.session_state.selected_name = st.session_state.dropdown_name


# -----------------------------------------------------------------------------
# Draw the actual page

# Set the title that appears at the top of the page.
'''
# :game_die: Board Game Night Analytics!:game_die:

All data is exported from the guest lists from my [Partiful Invites](https://www.partiful.com/). The data in this,
just reflects up until board game night that was on July 18. This dashboard will evolve as I add more filtering and inputs.
'''

# Add some spacing
''
''

if 'input_name' not in st.session_state:
    st.session_state.input_name = ''
if 'selected_name' not in st.session_state:
    st.session_state.selected_name = ''

input_name = st.text_input('Enter your name to check the events you went to! (check Partiful if your name does not pop up!):',
                                  value=st.session_state.input_name, 
                                   on_change=clear_input)

name_options = [''] + guest_df['Name'].unique().tolist()
selected_name = st.selectbox('Select a name to filter the DataFrame:', 
                             options=name_options, 
                             index=name_options.index(st.session_state.selected_name) if st.session_state.selected_name in name_options else 0, 
                             on_change=clear_select, 
                             key='dropdown_name')

# Filter the DataFrame based on user input
if input_name:
    filtered_guest_df = guest_df[guest_df['Name'].str.lower() == input_name.lower()]
elif selected_name:
    filtered_guest_df = guest_df[guest_df['Name'] == selected_name]
else:
    filtered_guest_df = guest_df

guest_list = st.dataframe(filtered_guest_df.reset_index(drop=True))




