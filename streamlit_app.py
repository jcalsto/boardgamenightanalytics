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


# -----------------------------------------------------------------------------
# Draw the actual page

# Set the title that appears at the top of the page.
'''
# :game_die: Welcome! Check out the event analytics for Board Game Night!

All data is exported from the guest lists from my [Partiful Invites](https://www.partiful.com/). The data in this,
just reflects up until board game night that was on July 18. This dashboard will evolve as I add more filtering and inputs.
'''

# Add some spacing
''
''

guest_list = st.dataframe(guest_df)


