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
st.header('The latest economics working papers')

st.write(
    "The following table contains an aggregation of titles, authors, abstracts, source, dates of publication of economics working papers "
    "from 20+ different websites. Working papers, also known as pre-print papers, are articles that have not yet been vetted by the "
    "peer-review process at an academic journal.\n  "
    "See the source code and replicate the project at: https://github.com/lorae/roundup"
)

# Load data
df, source_options, current_date = load_df()
res = df
status_df = load_status()

# Calculate the number of active web scrapers
total_scrapers = status_df.shape[0]
active_scrapers = (status_df['Status'] == 'on').sum()

########## Sidebar ##########
# OPTIONS
st.sidebar.header("Options")
# Display number of active web scrapers
status_message = f"{active_scrapers} of {total_scrapers} web scrapers currently active"
st.sidebar.write(status_message)
# Web scraper status drop down
st.sidebar.header("Web Scraper Status")
with st.sidebar.expander("Show/Hide Status", expanded=False):  # This line creates a collapsible section
    # Convert DataFrame to HTML, remove index and borders
    html_status_table = status_df.to_html(index=False, border=0)
    # Display HTML table using st.markdown
    st.markdown(html_status_table, unsafe_allow_html=True)
# Configuring options
all_sources_option = "All"
source_options_with_all = [all_sources_option] + list(source_options)
# Source selection
source_selection = st.sidebar.multiselect("Select Source(s)", source_options_with_all, default=[all_sources_option])
# Recency selection
slider_selection = st.sidebar.slider("How many days of data would you like to view?",
                            min_value=1,
                            max_value=30,
                            value=7,
                            step=1)


########## Main ##########

# Get the minimum date based on the slider input
min_date = current_date - timedelta(days=(slider_selection))

# Apply user selected options
# Check if "All" is selected or individual sources are selected
if all_sources_option in source_selection:
    # If "All" is selected, use the whole DataFrame
    df_filtered = df[df['est_PubDate'] >= min_date]
else:
    # Otherwise, filter by the selected sources
    df_filtered = df[(df['est_PubDate'] >= min_date) & (df['Source'].isin(source_selection))]


# Adjust the DataFrame before converting it to HTML
df_novel = df_filtered.reset_index(drop=True)  # Reset the index and drop the old index
# Add hyperlinks to the titles
df_novel['Title'] = df_novel.apply(lambda row: f'<a href="{row["Link"]}">{row["Title"]}</a>', axis=1)
# Drop the 'Link' and 'Number' columns
df_novel = df_novel.drop(['Link', 'Number'], axis=1)

# create a custom order for sources
source_order = ['NBER', 'FED-BOARD', 'FED-BOARD-NOTES', 'FED-ATLANTA', 'FED-BOSTON', 'FED-CHICAGO', 'FED-CLEVELAND', 'FED-DALLAS', 'FED-KANSASCITY', 'FED_MINNEAPOLIS', 'FED-NEWYORK', 'FED-PHILADELPHIA', 'FED-RICHMOND', 'FED-SANFRANCISCO', 'FED-STLOUIS', 'BEA', 'BFI', 'BIS', 'BOE', 'ECB', 'IMF']
# convert 'source' column to 'Categorical' data type with custom order
df_novel['Source'] = pd.Categorical(df_novel['Source'], categories=source_order, ordered=True)
# sort the dataframe by 'source' column
df_novel = df_novel.sort_values(by='Source')
# Reset the index of df_novel after sorting, and drop the old index
#df_novel = df_novel.reset_index(drop=True)
df_novel.index = range(1, len(df_novel) + 1)

# Convert to HTML, set escape=False to prevent HTML syntax from being escaped
html = df_novel.to_html(escape=False)
# Define custom CSS style
css_style = """
<style>
    table.customTable {
        display: inline-block;
    }
    table.customTable td {
        word-wrap: break-word;
        word-break: break-all;
    }
    table.customTable td:nth-child(3) {  # Assuming 'Abstract' is the 3rd column
        font-size: 6px;  # Set to desired font size
        max-width: 500px;  # Set to desired column width
    }
</style>
"""

# Print number of data frame entries
num_entries = len(df_novel)
st.write(f"{num_entries} results")


# Apply custom CSS style
st.markdown(css_style, unsafe_allow_html=True)

# Convert DataFrame to HTML and display
st.markdown(html, unsafe_allow_html=True)

