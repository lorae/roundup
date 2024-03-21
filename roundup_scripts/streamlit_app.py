# This is where the app will be.
# Helpful tutorial: https://python-textbook.pythonhumanities.com/05_streamlit/05_01_03_displaying_data.html
# table styling: https://www.w3schools.com/html/html_table_styling.asp

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Cache our data
def load_df():
    csv_url = 'https://raw.githubusercontent.com/lorae/roundup/main/historic/papers-we-have-seen-metadata.csv'
    df = pd.read_csv(csv_url, parse_dates=['est_PubDate'])
    source_options = df.Source.unique()
    
    current_date = datetime.now()
   
    return df, source_options, current_date

def load_status():
    txt_url = 'https://raw.githubusercontent.com/lorae/roundup/main/scraper_status.txt'
    status_df = pd.read_csv(txt_url, names=["Source", "Status"])
    
    return status_df
    
    
def check_rows(column, options):
    return res.loc[res[column].isin(options)]

st.set_page_config(page_title="Roundup Data Viewer", page_icon="📖", layout="wide")    
st.title('Roundup: The Latest Economics Research')

st.write(
    "What are economists researching? We aggregate recent economics working papers from "
    "21 sources, with results updated daily at 7:00 a.m. EST. "
    "Working papers, also known as pre-print papers, are recently written research "
    "articles that have not yet been vetted by the peer review process at an academic "
    "journal."
)
st.write("")
st.write(
    "See the source code and replicate the project at: "
    "https://github.com/lorae/roundup"
)
st.divider()

# Load data
df, source_options, current_date = load_df()
res = df
status_df = load_status()

# Calculate the number of active web scrapers
total_scrapers = status_df.shape[0]
active_scrapers = (status_df['Status'] == 'on').sum()

########## Sidebar ##########
st.sidebar.header("Options")
# Configure options
all_sources_option = "All"
source_options_with_all = [all_sources_option] + list(source_options)
# Source selection
source_selection = st.sidebar.multiselect("Select source(s)", source_options_with_all, default=[all_sources_option])
# Recency selection
slider_selection = st.sidebar.slider("How many days of data would you like to view?",
                            min_value=1,
                            max_value=30,
                            value=7,
                            step=1)
# Display web scraper status
st.sidebar.header("Web Scraper Status")
# Display number of active web scrapers
st.sidebar.write(f"{active_scrapers} of {total_scrapers} web scrapers currently active")
# Web scraper status drop down
with st.sidebar.expander("Show/Hide Status", expanded=False):
    for _, row in status_df.iterrows():
        # Specify the column widths where the first column is 3 times wider than the second
        col1, col2 = st.columns([3, 1])
        # Write the values to the columns
        col1.write(row[0])
        col2.write(row[1])


########## Main ##########

## Get the minimum date based on the slider input
min_date = current_date - timedelta(days=(slider_selection))

## Apply user selected options from sidebar menu
if all_sources_option in source_selection: # If "All" is selected, filter above min_date
    df_filtered = df[df['est_PubDate'] >= min_date]
else: # Otherwise, filter by the selected sources, and filter above min_date
    df_filtered = df[(df['est_PubDate'] >= min_date) & (df['Source'].isin(source_selection))]


## Sort results before displaying df_filtered
source_order = ['NBER', 'FED-BOARD', 'FED-BOARD-NOTES', 'FED-ATLANTA', 'FED-BOSTON', 'FED-CHICAGO', 'FED-CLEVELAND', 'FED-DALLAS', 'FED-KANSASCITY', 'FED_MINNEAPOLIS', 'FED-NEWYORK', 'FED-PHILADELPHIA', 'FED-RICHMOND', 'FED-SANFRANCISCO', 'FED-STLOUIS', 'BEA', 'BFI', 'BIS', 'BOE', 'ECB', 'IMF']
# Map each source to its corresponding index in 'source_order' to use as a sort key
sort_key = df_filtered['Source'].map(lambda x: source_order.index(x))
# Sort df_novel by this sort key
df_filtered = df_filtered.iloc[sort_key.argsort()]

st.write("")
st.write("")
st.header("Results")
st.write(f"{num_results} entries found")

## Display contents of df_filtered using for loop, Streamlit columns
# Initialize a counter before the loop
entry_number = 1

# Displaying each entry vertically
for _, row in df_filtered.iterrows():
    col1, col2 = st.columns([1, 15])

    with index_col: # Column containing the index number of the paper
        # Format number as heading to ensure consistent alignment with the title
        st.markdown(f"### {entry_number}")
    
    with text_col: # Column containing title, author, source, date, etc
        st.markdown(f"###  `{row['Source']}` [{row['Title']}]({row['Link']})")
        st.markdown(f"**Authors:** {row['Author']}")
        colA, colB = st.columns([1,1])
        with colA:
            st.markdown(f"**Est Pub Date:** {row['est_PubDate'].strftime('%Y-%m-%d')}")
        with colB:
            st.markdown(f"**Posted Pub Date:** {row['Date']}")
        st.markdown(f"**Abstract:** {row['Abstract']}")
    
    entry_number += 1


