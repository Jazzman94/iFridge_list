import streamlit as st
import pandas as pd

df = pd.read_csv("data/fridge_list.csv")

st.title("Fridge List")

config = {
    "Item": st.column_config.TextColumn(),
    "Category": st.column_config.TextColumn(),
    "Input date":st.column_config.DatetimeColumn(),
    "Expiry date": st.column_config.DateColumn(disabled=False)
}

if st.toggle("Enable editing"):
    edited_df = st.data_editor(df, column_config=config, num_rows="dynamic", use_container_width=True)
else:
    st.dataframe(df, column_config=config, use_container_width=True)

