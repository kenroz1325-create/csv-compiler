import streamlit as st
import pandas as pd
from io import BytesIO
import zipfile

st.title("XLSX to CSV Converter")

uploaded_files = st.file_uploader(
    "Upload one or more Excel files",
    type=["xlsx"],
    accept_multiple_files=True
)

if uploaded_files:

    zip_buffer = BytesIO()

    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:

        for uploaded_file in uploaded_files:

            try:
                excel_file = pd.ExcelFile(uploaded_file)

                st.subheader(f"📄 {uploaded_file.name}")

                # Process all sheets
                for sheet in excel_file.sheet_names:

                    df = pd.read_excel(
                        uploaded_file,
                        sheet_name=sheet
                    )

                    st.write(f"Sheet: {sheet}")
                    st.dataframe(df.head())

                    csv_data = df.to_csv(index=False)

                    original_filename = uploaded_file.name.rsplit(".", 1)[0]

                    csv_filename = f"{original_filename}_{sheet}.csv"

                    zip_file.writestr(csv_filename, csv_data)

            except Exception as e:
                st.error(f"Error processing {uploaded_file.name}: {e}")

    zip_buffer.seek(0)

    st.download_button(
        label="📥 Download All CSV Files (ZIP)",
        data=zip_buffer,
        file_name="converted_csv_files.zip",
        mime="application/zip"
    )
