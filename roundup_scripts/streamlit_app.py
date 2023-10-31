# This is where the app will be.
# Helpful tutorial: https://python-textbook.pythonhumanities.com/05_streamlit/05_01_03_displaying_data.html

import streamlit as st
import pandas as pd



# Cache our data
@st.cache()
def load_df():
    csv_url = 'https://raw.githubusercontent.com/lorae/roundup/main/historic/papers-we-have-seen-metadata.csv'
    df = pd.read_csv(csv_url)
    source_options = df.Source.unique()
   
    return df, source_options

def check_rows(column, options):
    return res.loc[res[column].isin(options)]

st.set_page_config(page_title="KRoundup Data Viewer", page_icon="📖", layout="wide")    
st.header('The latest economics working papers')
st.write("The following metadata includes titles, authors, abstracts, source, and best estimate date of publication of various working papers (also known as pre-print papers) in economics.")

options = ["Red", "Blue", "Yellow"]
st.sidebar.header("Sidebar Header")
selectbox_selection = st.sidebar.selectbox("Select Color", options)
st.write(f"Color selected is {selectbox_selection}")
htmltext = f"""
<a style='background:{selectbox_selection}'>Displayed are the most recent working paper publications from 18 websites.</a>
"""
st.markdown(htmltext, unsafe_allow_html=True)




slider_number = st.slider("Select your Number",
                            min_value=1,
                            max_value=30,
                            value=7,
                            step=1)
st.write(slider_number)



df, source_options = load_df()
res = df

# Adjust the DataFrame before converting it to HTML
df_novel = df.reset_index(drop=True)  # Reset the index and drop the old index
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
# Wrap the HTML in a <div> element with a custom style to control the width
html_with_style = f"""
<div style="width:100%; overflow-x: auto; border-collapse: collapse;">
    {html}
</div>
"""

# Use st.markdown to display the HTML
st.markdown(html_with_style, unsafe_allow_html=True)




name_query = st.text_input("String match for Name")

if name_query != "":
    res = res.loc[res.Name.str.contains(name_query)]
 
removal_columns = st.multiselect("Select Columns to Remove", df.columns.tolist())
for column in removal_columns:
    res = res.drop(column, axis=1)
st.write(res)




