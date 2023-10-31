# This is where the app will be.

import streamlit as st
import pandas as pd

# Title of the app
st.title('Roundup Data Viewer')

# File upload widget
uploaded_file = st.file_uploader("historic/papers-we-have-seen-metadata", type=['csv'])

# Check if a file is uploaded
if uploaded_file is not None:
    # Read and display the CSV file
    df = pd.read_csv(uploaded_file)
    
    # Drop-down menu for sorting
    sort_option = st.selectbox('Sort by:', options=['None'] + list(df.columns))
    
    # Sort data if an option is selected
    if sort_option != 'None':
        df = df.sort_values(sort_option)
    
    # Display the data table
    st.write(df)