import streamlit as st
import pandas as pd
import json

st.title("Visualization of JSON Data")

# Create a file uploader widget to allow users to upload a JSON file
uploaded_file = st.file_uploader("Choose a JSON file", type=['json'])

if uploaded_file is not None:
    # Define a function to load data from the uploaded file
    def load_data_uploaded(uploaded_file):
        # Read the content of the uploaded file
        data = json.load(uploaded_file)
        return pd.DataFrame(data)

    # Load the data from the uploaded file
    data = load_data_uploaded(uploaded_file)
    
    if data is not None:
        # Create a selection box for "File Name"
        selected_file_name = st.selectbox("Select File Name", options=data['FileName'].unique())
        
        # Assuming your data includes an "Author" field, create a multiselect for "Author"
        if 'Author' in data.columns:  # Check if the 'Author' column exists
            selected_authors = st.multiselect("Select Author(s)", options=data['Author'].unique())
        else:
            st.write("No 'Author' field in the uploaded data.")
            selected_authors = []

        # Use multiselect for selecting multiple classes
        selected_classes = st.multiselect("Select Class(es)", options=data['Class'].unique())

        # Apply filters based on selections
        if not selected_classes and not selected_authors:  # If no class and no author is selected, show all data for the file name
            filtered_data = data[data['FileName'] == selected_file_name]
        else:
            # Filter the data based on the selected file name, classes, and authors
            filtered_data = data[(data['FileName'] == selected_file_name) & 
                                 (data['Class'].isin(selected_classes) if selected_classes else True) & 
                                 (data['Author'].isin(selected_authors) if selected_authors else True)]

        # Display the filtered information
        with st.expander("Filtered Data"):
            if not filtered_data.empty:
                st.write(filtered_data[['FileName', 'Class', 'Name', 'Global ID', 'Author', 'Software', 'Description', 'Reason']])
            else:
                st.write("No data available for the selected filters.")
else:
    st.write("Waiting for a file to be uploaded...")
