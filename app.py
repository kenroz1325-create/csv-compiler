import streamlit as st
import pandas as pd
from io import BytesIO
import zipfile

# ======================================================
# PAGE CONFIG
# ======================================================

st.set_page_config(
    page_title="CSV Compiler",
    page_icon="📄",
    layout="wide"
)

# ======================================================
# CUSTOM CSS
# ======================================================

st.markdown("""
<style>

/* App Background */
[data-testid="stAppViewContainer"]{
    background-color:#F4F5F9;
}

/* Main Container */
.main{
    padding-top:1rem;
}

/* Title */
.title{
    text-align:center;
    font-size:3rem;
    font-weight:700;
    color:#1F2A6B;
    margin-bottom:0;
}

/* Subtitle */
.subtitle{
    text-align:center;
    color:#6B7280;
    margin-bottom:20px;
}

/* Header Accent Bar */
.top-bar{
    height:8px;
    background:linear-gradient(
        90deg,
        #1F2A6B 0%,
        #1F2A6B 55%,
        #00CFE8 80%,
        #E91E63 100%
    );
    border-radius:15px;
    margin-bottom:25px;
}

/* File Uploader */
[data-testid="stFileUploader"]{
    background:white;
    padding:20px;
    border-radius:12px;
    border-left:5px solid #00CFE8;
    box-shadow:0 2px 8px rgba(0,0,0,.08);
}

/* Download Button */
.stDownloadButton button{
    width:100%;
    background:#1F2A6B;
    color:white;
    font-weight:700;
    border:none;
    border-radius:10px;
    height:55px;
}

.stDownloadButton button:hover{
    background:#2F3F99;
    color:white;
}

/* Expander */
details{
    background:white;
    border-radius:10px;
    margin-bottom:10px;
    border:1px solid #DCE1E7;
}

/* Footer */
.footer{
    text-align:center;
    color:#6B7280;
    font-size:12px;
    margin-top:15px;
}

</style>
""", unsafe_allow_html=True)

# ======================================================
# HEADER
# ======================================================

st.markdown(
    '<div class="title">📄 ELDRIAN MANYAKOL</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Bulk Convert Multiple Excel Files into CSV</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="top-bar"></div>',
    unsafe_allow_html=True
)

# ======================================================
# FILE UPLOAD
# ======================================================

uploaded_files = st.file_uploader(
    "📤 Upload Excel Files",
    type=["xlsx"],
    accept_multiple_files=True
)

# ======================================================
# PROCESS FILES
# ======================================================

if uploaded_files:

    st.success(
        f"✅ {len(uploaded_files)} file(s) uploaded successfully."
    )

    zip_buffer = BytesIO()

    with zipfile.ZipFile(
        zip_buffer,
        "w",
        zipfile.ZIP_DEFLATED
    ) as zip_file:

        for uploaded_file in uploaded_files:

            with st.expander(
                f"📁 {uploaded_file.name}",
                expanded=False
            ):

                try:

                    excel_file = pd.ExcelFile(
                        uploaded_file
                    )

                    st.info(
                        f"Sheets Found: {len(excel_file.sheet_names)}"
                    )

                    original_filename = (
                        uploaded_file.name.rsplit(".", 1)[0]
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

                        csv_data = df.to_csv(
                            index=False
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

# ======================================================
# FOOTER
# ======================================================

st.divider()

st.markdown(
    '<div class="footer">XLSX to CSV Compiler • Powered by Streamlit</div>',
    unsafe_allow_html=True
)
