# This is where the app will be.

import streamlit as st
import pandas as pd

# Create some sample data
data = {
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [24, 27, 22],
    'City': ['New York', 'Los Angeles', 'Chicago']
}
df = pd.DataFrame(data)

# Title of the app
st.title('My First Streamlit App')

# Drop-down menu for sorting
sort_option = st.selectbox('Sort by:', options=['None', 'Name', 'Age', 'City'])

# Sort data if an option is selected
if sort_option != 'None':
    df = df.sort_values(sort_option)

# Display the data table
st.write(df)