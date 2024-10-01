import streamlit as st
import pandas as pd

# Function to process the uploaded CSV and generate the counts and sums for unique fund managers
def process_csv(file, fund_manager_col, amount_col):
    df = pd.read_csv(file)
    
    # Split the entries and remove duplicates within each row using "set"
    df['Unique fund managers'] = df[fund_manager_col].apply(
        lambda x: list(set(str(x).split(", ")))
    )
    
    # Explode the list to count each unique fund manager
    exploded_df = df.explode('Unique fund managers')
    
    # Group by fund manager and aggregate participation count and total amount raised
    fund_manager_counts = exploded_df.groupby('Unique fund managers').agg(
        Participation_count=('Unique fund managers', 'size'),
        Total_amount_raised=(amount_col, 'sum')
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
    # Read the uploaded CSV to get the column names
    df = pd.read_csv(uploaded_file)
    columns = df.columns.tolist()
    
    # Selectbox to choose the column for fund managers
    fund_manager_col = st.selectbox(
        "Select the column representing fund managers:",
        options=columns,
        index=columns.index('Fundraising investors - Fund manager') if 'Fundraising investors - Fund manager' in columns else 0
    )
    
    # Selectbox to choose the column for amount raised
    amount_col = st.selectbox(
        "Select the column representing the amount raised (converted to GBP):",
        options=columns,
        index=columns.index('Amount raised (converted to GBP)') if 'Amount raised (converted to GBP)' in columns else 0
    )
    
    # Process the file using the selected columns
    result_df = process_csv(uploaded_file, fund_manager_col, amount_col)
    
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
