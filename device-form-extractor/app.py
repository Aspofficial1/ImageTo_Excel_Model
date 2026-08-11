import os
import time
import streamlit as st
import pandas as pd

from config import UPLOADS_DIR, OUTPUT_EXCEL
from schema import COLUMNS
from ocr_engine import extract_from_image
from excel_handler import load_existing, append_row, save

st.set_page_config(page_title="Device Form Extractor", layout="wide")
st.title("📋 Mobile Device Acceptance Form Extractor")

if "df" not in st.session_state:
    st.session_state.df = load_existing()

uploaded_files = st.file_uploader(
    "Upload form images (multiple allowed — jpg, jpeg, png)",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True,
)

col1, col2 = st.columns([1, 1])

with col1:
    process_clicked = st.button("🚀 Process Images", type="primary")

with col2:
    if st.button("🗑️ Clear Table"):
        st.session_state.df = pd.DataFrame(columns=COLUMNS)
        st.rerun()

status_placeholder = st.empty()
progress_placeholder = st.empty()
table_placeholder = st.empty()

# Always show current table
table_placeholder.dataframe(st.session_state.df, width="stretch")

if process_clicked and uploaded_files:
    total = len(uploaded_files)
    progress_bar = progress_placeholder.progress(0, text="Starting...")

    for i, file in enumerate(uploaded_files):
        save_path = os.path.join(UPLOADS_DIR, file.name)
        with open(save_path, "wb") as f:
            f.write(file.getbuffer())

        status_placeholder.info(f"⏳ Processing {file.name} ({i+1}/{total})...")

        start_time = time.time()
        try:
            extracted = extract_from_image(save_path)
            elapsed = time.time() - start_time
            st.session_state.df = append_row(st.session_state.df, file.name, extracted, elapsed)
            save(st.session_state.df)  # save after EVERY image, not just at the end
            status_placeholder.success(f"✅ Done: {file.name} ({elapsed:.2f}s)")
        except Exception as e:
            elapsed = time.time() - start_time
            status_placeholder.warning(f"⚠️ Failed on {file.name} after {elapsed:.2f}s: {e}")

        # live-refresh table after each image
        table_placeholder.dataframe(st.session_state.df, width="stretch")
        progress_bar.progress((i + 1) / total, text=f"{i+1}/{total} completed")

    status_placeholder.success(f"🎉 All {total} images processed.")

st.subheader("📊 Extracted Data (editable)")

edited_df = st.data_editor(
    st.session_state.df,
    num_rows="dynamic",
    width="stretch",
    key="editor",
)
st.session_state.df = edited_df

col3, col4 = st.columns([1, 1])

with col3:
    if st.button("💾 Save Edits to Excel"):
        save(st.session_state.df)
        st.success("Saved.")

with col4:
    if not st.session_state.df.empty and os.path.exists(OUTPUT_EXCEL):
        with open(OUTPUT_EXCEL, "rb") as f:
            st.download_button(
                "⬇️ Download Excel",
                data=f.read(),
                file_name="device_forms_output.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )