# This is where the app will be.

import streamlit as st
import pandas as pd

# Title of the app
st.title('Roundup Data Viewer')

# GitHub raw URL of the CSV file
csv_url = 'https://raw.githubusercontent.com/lorae/roundup/main/historic/papers-we-have-seen-metadata.csv'

# Read and display the CSV file
df = pd.read_csv(csv_url)

# Remove the 'Number' column
df = df.drop(columns=['Number'])

# Create hyperlinks for the 'Title' column using the 'Link' column
df['Title'] = df.apply(lambda row: f"[{row['Title']}]({row['Link']})", axis=1)

# Remove the 'Link' column
df = df.drop(columns=['Link'])

# Split the layout into 2 columns
col1, col2 = st.beta_columns((3,1))

# Display the data table in the left column (col1)
col1.write(df, use_container_width=True)

# Drop-down menu for sorting in the right column (col2)
sort_option = col2.selectbox('Sort by:', options=['None'] + list(df.columns))

# Sort data if an option is selected
if sort_option != 'None':
    df = df.sort_values(sort_option)
    col1.write(df, use_container_width=True)  # Re-display the sorted data table