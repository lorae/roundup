# This is where the app will be.
# Helpful tutorial: https://python-textbook.pythonhumanities.com/05_streamlit/05_01_03_displaying_data.html
# table styling: https://www.w3schools.com/html/html_table_styling.asp

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Cache our data
@st.cache()
def load_df():
    csv_url = 'https://raw.githubusercontent.com/lorae/roundup/main/historic/papers-we-have-seen-metadata.csv'
    df = pd.read_csv(csv_url, parse_dates=['est_PubDate'])
    source_options = df.Source.unique()
    
    current_date = datetime.now()
   
    return df, source_options, current_date

def check_rows(column, options):
    return res.loc[res[column].isin(options)]

st.set_page_config(page_title="Roundup Data Viewer", page_icon="📖", layout="wide")    
st.header('The latest economics working papers')
st.write("The following metadata includes titles, authors, abstracts, source, and best estimate date of publication of various working papers (also known as pre-print papers) in economics.")

df, source_options, current_date = load_df()
res = df

### Sidebar
st.sidebar.header("Options")
# Configuring options
all_sources_option = "All"
source_options_with_all = [all_sources_option] + list(source_options)
color_options = ["Red", "Orange", "Green", "Blue", "Violet", "Pink", "Yellow"]
# Color selection
color_selection = st.sidebar.selectbox("Select Color", color_options)
# Source selection
source_selection = st.sidebar.selectbox("Select Source", source_options)
st.write(f"Color selected is {color_selection}")
# Recency selection
slider_selection = st.sidebar.slider("How many days of data would you like to view?",
                            min_value=1,
                            max_value=30,
                            value=7,
                            step=1)
                            
### Main
htmltext = f"""
<a style='background:{color_selection}'>Displayed are the most recent working paper publications from 18 websites.</a>
"""
st.markdown(htmltext, unsafe_allow_html=True)



# Get the minimum date based on the slider input
min_date = current_date - timedelta(days=slider_selection)

# Apply user selected options
# Check if "All" is selected or individual sources are selected
if all_sources_option in source_selection:
    # If "All" is selected, use the whole DataFrame
    df_novel = df[df['est_PubDate'] >= min_date]
else:
    # Otherwise, filter by the selected sources
    df_novel = df[(df['est_PubDate'] >= min_date) & (df['Source'].isin(source_selection))]


# Adjust the DataFrame before converting it to HTML
df_novel = df_filtered.reset_index(drop=True)  # Reset the index and drop the old index
# Add hyperlinks to the titles
df_novel['Title'] = df_novel.apply(lambda row: f'<a href="{row["Link"]}">{row["Title"]}</a>', axis=1)
# Drop the 'Link' and 'Number' columns
df_novel = df_novel.drop(['Link', 'Number'], axis=1)

# create a custom order for sources
source_order = ['NBER', 'FED-BOARD', 'FED-BOARD-NOTES', 'FED-ATLANTA', 'FED-BOSTON', 'FED-CHICAGO', 'FED-CLEVELAND', 'FED-DALLAS', 'FED-NEWYORK', 'FED-PHILADELPHIA', 'FED-RICHMOND', 'FED-SANFRANCISCO', 'BEA', 'BFI', 'BIS', 'BOE', 'ECB', 'IMF']
# convert 'source' column to 'Categorical' data type with custom order
df_novel['Source'] = pd.Categorical(df_novel['Source'], categories=source_order, ordered=True)
# sort the dataframe by 'source' column
df_novel = df_novel.sort_values(by='Source')
# Reset the index of df_novel after sorting, and drop the old index
df_novel = df_novel.reset_index(drop=True)

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


# Apply custom CSS style
st.markdown(css_style, unsafe_allow_html=True)

# Convert DataFrame to HTML and display
st.markdown(html, unsafe_allow_html=True)




name_query = st.text_input("String match for Name")

if name_query != "":
    res = res.loc[res.Name.str.contains(name_query)]
 
removal_columns = st.multiselect("Select Columns to Remove", df.columns.tolist())
for column in removal_columns:
    res = res.drop(column, axis=1)
st.write(res)




