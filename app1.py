import streamlit as st
import pandas as pd

# Title of the app
st.title("Percentage Difference Between Two DataFrames")

st.header("Upload Your DataFrames")
file1 = st.file_uploader("Upload first CSV file", type=["csv"])
file2 = st.file_uploader("Upload second CSV file", type=["csv"])

if file1 and file2:
    df1 = pd.read_csv(file1)
    st.subheader("First DataFrame")
    st.dataframe(df1)
    df2 = pd.read_csv(file2)
    st.subheader("Second DataFrame")
    st.dataframe(df2)

    if df1.shape == df2.shape:
        try:
            # Clean column names
            df1.columns = df1.columns.str.strip().str.lower()
            df2.columns = df2.columns.str.strip().str.lower()

            # Clean numeric data
            def clean_currency(df):
                numeric_columns = df.select_dtypes(include=['object', 'float']).columns
                for col in numeric_columns:
                    df[col] = pd.to_numeric(df[col].replace(r'[\$,]', '', regex=True), errors='coerce')
                return df

            df1_cleaned = clean_currency(df1.copy())
            df2_cleaned = clean_currency(df2.copy())

            # Align columns
            common_columns = df1_cleaned.columns.intersection(df2_cleaned.columns)
            if common_columns.empty:
                st.error("No common columns found between the DataFrames!")
                st.stop()

            df1_cleaned = df1_cleaned[common_columns]
            df2_cleaned = df2_cleaned[common_columns]

            # Handle division by zero and calculate percentage difference
            percentage_diff = ((df2_cleaned - df1_cleaned) / df1_cleaned.replace(0, pd.NA)) * 100
            percentage_diff["weight break"]=df1["weight break"]
            # Display results
            st.subheader("Percentage Difference")
            st.dataframe(percentage_diff)
            st.write("Statistics")
            st.write(percentage_diff.describe())

        except Exception as e:
            st.error(f"An error occurred during calculation: {e}")
    else:
        st.error("DataFrames must have the same shape!")
else:
    st.info("Please upload two CSV files to proceed.")
