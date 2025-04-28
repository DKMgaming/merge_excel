import streamlit as st
import pandas as pd

# Hàm tự động đọc file .xls hoặc .xlsx
def read_excel_auto(file):
    if file.name.endswith('.xls'):
        return pd.read_excel(file, engine='xlrd')
    else:
        return pd.read_excel(file, engine='openpyxl')

# Giao diện Streamlit
st.title("Nối nhiều file Excel (.xls, .xlsx) thành 1 file")

uploaded_files = st.file_uploader(
    "Tải lên nhiều file Excel (.xls hoặc .xlsx)", 
    type=["xls", "xlsx"], 
    accept_multiple_files=True
)

if uploaded_files:
    all_dfs = []

    for file in uploaded_files:
        df = read_excel_auto(file)
        all_dfs.append(df)

    # Ghép tất cả các file lại
    merged_df = pd.concat(all_dfs, ignore_index=True)

    st.success(f"Đã ghép {len(uploaded_files)} file lại với nhau!")
    st.dataframe(merged_df)

    # Tải file về
    @st.cache_data
    def convert_df(df):
        return df.to_excel(index=False, engine='xlsxwriter')

    merged_file = convert_df(merged_df)

    st.download_button(
        label="📥 Tải file Excel đã ghép",
        data=merged_file,
        file_name="merged_file.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
