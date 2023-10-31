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

    min_days_ago = 0
    max_days_ago = 30 
    
    return df, source_options, min_days_ago, max_days_ago

def check_rows(column, options):
    return res.loc[res[column].isin(options)]
    
# Title of the app
st.title('Roundup Data Viewer')
st.header('The latest economics working papers')
st.subheader('E pluribus unum.')
st.markdown(html, unsafe_allow_html=True)
html = """
<a style='background:yellow'>Displayed are the most recent working paper publications from 18 websites.</a>
"""

df, source_options, min_days_ago, max_days_ago = load_df()
res = df

name_query = st.text_input("String match for Name")

if name_query != "":
    res = res.loc[res.Name.str.contains(name_query)]
 
removal_columns = st.multiselect("Select Columns to Remove", df.columns.tolist())
for column in removal_columns:
    res = res.drop(column, axis=1)
st.write(res)


options = ["Red", "Blue", "Yellow"]
selectbox_selection = st.selectbox("Select Color", options)
st.write(f"Color selected is {selectbox_selection}")
