import streamlit as st
import pandas as pd
import io

st.title('📝 Nối nhiều file Excel thành một')

uploaded_files = st.file_uploader("📂 Tải lên các file Excel (.xlsx)", type="xlsx", accept_multiple_files=True)

if uploaded_files:
    dataframes = []
    for uploaded_file in uploaded_files:
        df = pd.read_excel(uploaded_file)
        dataframes.append(df)
    
    merged_df = pd.concat(dataframes, ignore_index=True)
    
    st.success(f"✅ Đã nối {len(uploaded_files)} file Excel thành công!")

    # Hiển thị bản xem trước
    st.dataframe(merged_df)

    # Tạo file excel mới trong bộ nhớ
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        merged_df.to_excel(writer, index=False, sheet_name='MergedData')
    output.seek(0)

    # Nút tải file
    st.download_button(
        label="📥 Tải file Excel đã nối",
        data=output,
        file_name="file_merged.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
