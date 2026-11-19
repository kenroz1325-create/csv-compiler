import streamlit as st
import pandas as pd
from io import BytesIO

st.title("XLSX to CSV Converter")

uploaded_file = st.file_uploader(
    "Upload an Excel file",
    type=["xlsx"]
)

if uploaded_file:
    excel_file = pd.ExcelFile(uploaded_file)

    sheet = st.selectbox(
        "Select Sheet",
        excel_file.sheet_names
    )

    df = pd.read_excel(
        uploaded_file,
        sheet_name=sheet
    )

    st.subheader("Preview")
    st.dataframe(df.head())

    csv = df.to_csv(index=False)

original_filename = uploaded_file.name.rsplit(".", 1)[0]

st.download_button(
    label="Download CSV",
    data=csv,
    file_name=f"{original_filename}.csv",
    mime="text/csv"
)
