import streamlit as st
import pandas as pd

# Function to process the uploaded CSV and generate the counts of unique fund managers
def process_csv(file):
    df = pd.read_csv(file)
    # Split the entries and remove duplicates within each row using "set"
    df['Unique fund managers'] = df['Fundraising investors - Fund manager'].apply(
        lambda x: list(set(x.split(", ")))
    )
    # Explode the list to count each unique fund manager
    exploded_df = df.explode('Unique fund managers')
    # Count occurrences of each unique fund manager
    fund_manager_counts = exploded_df['Unique fund managers'].value_counts().reset_index()
    fund_manager_counts.columns = ['Fund manager', 'Participation count']
    return fund_manager_counts

# Streamlit app
st.title("Manager counter")

# File uploader
uploaded_file = st.file_uploader("Upload your CSV file", type="csv")

if uploaded_file is not None:
    # Process the file
    result_df = process_csv(uploaded_file)
    
    # Display the result
    st.write("Unique Fund Manager Participation Count")
    st.dataframe(result_df)
    
    # Provide download link
    st.download_button(
        label="Download CSV",
        data=result_df.to_csv(index=False),
        file_name='fund_mgr_participation_count.csv',
        mime='text/csv'
    )
