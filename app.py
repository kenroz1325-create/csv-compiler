import streamlit as st
import pandas as pd
from io import BytesIO
import zipfile

# Page Configuration
st.set_page_config(
    page_title="CSV Compiler",
    page_icon="📄",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
.main {
    padding-top: 1rem;
}

.title {
    text-align: center;
    color: #00BFA5;
    font-size: 3rem;
    font-weight: bold;
}

.subtitle {
    text-align: center;
    color: gray;
    margin-bottom: 30px;
}

.stDownloadButton button {
    width: 100%;
    background-color: #00BFA5;
    color: white;
    font-weight: bold;
    border-radius: 10px;
}

.stDownloadButton button:hover {
    background-color: #009688;
}

.preview-card {
    padding: 15px;
    border-radius: 10px;
    background-color: #f7f7f7;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown(
    '<div class="title">📄 CSV Compiler</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Convert Multiple Excel Files into CSV Instantly</div>',
    unsafe_allow_html=True
)

st.divider()

# Upload Section
uploaded_files = st.file_uploader(
    "📤 Upload Excel Files",
    type=["xlsx"],
    accept_multiple_files=True
)

if uploaded_files:

    st.success(f"✅ {len(uploaded_files)} file(s) uploaded successfully.")

    zip_buffer = BytesIO()

    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:

        for uploaded_file in uploaded_files:

            with st.expander(f"📁 {uploaded_file.name}", expanded=False):

                try:
                    excel_file = pd.ExcelFile(uploaded_file)

                    st.info(
                        f"Sheets Found: {len(excel_file.sheet_names)}"
                    )

                    for sheet in excel_file.sheet_names:

                        df = pd.read_excel(
                            uploaded_file,
                            sheet_name=sheet
                        )

                        st.markdown(
                            f"### 📋 Sheet: {sheet}"
                        )

                        st.dataframe(
                            df.head(),
                            use_container_width=True
                        )

                        csv_data = df.to_csv(index=False)

                        original_filename = (
                            uploaded_file.name.rsplit(".", 1)[0]
                        )

                        csv_filename = (
                            f"{original_filename}_{sheet}.csv"
                        )

                        zip_file.writestr(
                            csv_filename,
                            csv_data
                        )

                except Exception as e:
                    st.error(
                        f"Error processing {uploaded_file.name}: {e}"
                    )

    zip_buffer.seek(0)

    st.divider()

    st.download_button(
        label="📥 Download All Converted CSV Files (ZIP)",
        data=zip_buffer,
        file_name="CSV_Compiler_Output.zip",
        mime="application/zip"
    )

else:
    st.info(
        "Upload one or more Excel files to begin conversion."
    )

# Footer
st.divider()
st.caption(
    "Built with Streamlit • XLSX → CSV Compiler"
)
