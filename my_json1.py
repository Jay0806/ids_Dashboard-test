import streamlit as st
import pandas as pd
import json

# Define a new function to load data from an uploaded file
def load_data_uploaded(uploaded_file):
    if uploaded_file is not None:
        # Read the content of the uploaded file
        data = json.load(uploaded_file)
        return pd.DataFrame(data)
    else:
        return None

st.title("Visualization of JSON Data")

# Create a file uploader widget to allow users to upload a JSON file
uploaded_file = st.file_uploader("Choose a JSON file", type=['json'])

if uploaded_file is not None:
    # Load the data from the uploaded file instead of a fixed path
    data = load_data_uploaded(uploaded_file)
    
    if data is not None:
        # Create a selection box for "File Name"
        selected_file_name = st.selectbox("Select File Name", options=data['FileName'].unique())
        
        # Use multiselect for selecting multiple classes
        selected_classes = st.multiselect("Select Class(es)", options=data['Class'].unique())

        # Check if any class is selected; if not, display data for all classes
        if not selected_classes:  # If no class is selected, show all data for the file name
            filtered_data = data[data['FileName'] == selected_file_name]
        else:
            # Filter the data based on the selected file name and selected classes
            filtered_data = data[(data['FileName'] == selected_file_name) & (data['Class'].isin(selected_classes))]

        # Display the filtered information
        with st.expander("Filtered Data"):
            if not filtered_data.empty:
                st.write(filtered_data[['Description', 'Reason', 'Name', 'Global ID']])
            else:
                st.write("No data available for the selected filters.")
    else:
        st.write("Please upload a file to proceed.")
else:
    st.write("Waiting for a file to be uploaded...")
