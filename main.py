import streamlit as st
import pandas as pd

# Function to process the uploaded CSV and generate the counts and sums for unique fund managers
def process_csv(file):
    df = pd.read_csv(file)
    
    # Split the entries and remove duplicates within each row using "set"
    df['Unique fund managers'] = df['Fundraising investors - Fund manager'].apply(
        lambda x: list(set(x.split(", ")))
    )
    
    # Explode the list to count each unique fund manager
    exploded_df = df.explode('Unique fund managers')
    
    # Group by fund manager and aggregate participation count and total amount raised
    fund_manager_counts = exploded_df.groupby('Unique fund managers').agg(
        Participation_count=('Unique fund managers', 'size'),
        Total_amount_raised=('Amount raised (converted to GBP)', 'sum')
    ).reset_index()

    # Rename the columns for clarity
    fund_manager_counts.columns = ['Fund manager', 'Participation count', 'Total amount raised']

    return fund_manager_counts

# Streamlit app
st.title("Fund Manager Participation Counter")

st.write(
    """
    This app takes a CSV file of deals and counts the number of unique instances 
    of a fund manager involved in a deal. It also sums the total amount raised 
    (converted to GBP) for each manager.
    """
)

# File uploader
uploaded_file = st.file_uploader("Upload your CSV file", type="csv")

if uploaded_file is not None:
    # Process the file
    result_df = process_csv(uploaded_file)
    
    # Display the result
    st.write("Unique Fund Manager Participation Count and Total Amount Raised")
    st.dataframe(result_df)
    
    # Provide download link for the CSV file
    st.download_button(
        label="Download CSV",
        data=result_df.to_csv(index=False),
        file_name='fund_mgr_participation_count.csv',
        mime='text/csv'
    )
