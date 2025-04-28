import streamlit as st
import pandas as pd
import os
import glob
import io

st.title("Ứng dụng nối file Excel (.xlsx, .xls)")

folder_path = st.text_input("Nhập đường dẫn tới thư mục chứa file Excel")

def merge_excels(folder_path):
    all_files = glob.glob(os.path.join(folder_path, "*.xlsx")) + glob.glob(os.path.join(folder_path, "*.xls"))
    li = []

    for filename in all_files:
        if filename.endswith('.xlsx') or filename.endswith('.xls'):
            try:
                df = pd.read_excel(filename)
                li.append(df)
            except Exception as e:
                st.error(f"Lỗi đọc file {filename}: {e}")

    if li:
        merged_df = pd.concat(li, axis=0, ignore_index=True)
        return merged_df
    else:
        return None

def convert_df_to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    processed_data = output.getvalue()
    return processed_data

if st.button("Nối file"):
    if folder_path:
        merged_df = merge_excels(folder_path)
        if merged_df is not None:
            st.success("Đã nối file thành công!")
            st.dataframe(merged_df)

            merged_file = convert_df_to_excel(merged_df)

            st.download_button(
                label="Tải file Excel đã nối",
                data=merged_file,
                file_name="merged_file.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
        else:
            st.warning("Không tìm thấy file hợp lệ trong thư mục.")
    else:
        st.warning("Vui lòng nhập đường dẫn thư mục!")
