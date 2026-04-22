import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Live Screener Dashboard", layout="wide")
st.title("📈 Live Options Screener Dashboard")

# Load latest screener output
data_path = "logs/screener_output.csv"

if os.path.exists(data_path):
    df = pd.read_csv(data_path)

    if df.empty:
        st.warning("⚠️ No signals generated yet.")
    else:
        st.dataframe(df.style.highlight_max(axis=0), use_container_width=True)

        st.download_button(
            label="📥 Download Screener Output",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name="screener_output.csv",
            mime="text/csv"
        )
else:
    st.error("No screener output found. Please run the signal engine.")
