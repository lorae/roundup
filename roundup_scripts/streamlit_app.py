# This is where the app will be.

import streamlit as st
import pandas as pd

# Title of the app
st.title('Roundup Data Viewer')

# GitHub raw URL of the CSV file
csv_url = 'https://raw.githubusercontent.com/lorae/roundup/main/historic/papers-we-have-seen-metadata.csv'

# Read and display the CSV file
df = pd.read_csv(csv_url)

# Drop-down menu for sorting
sort_option = st.selectbox('Sort by:', options=['None'] + list(df.columns))

# Sort data if an option is selected
if sort_option != 'None':
    df = df.sort_values(sort_option)

# Display the data table
st.write(df)