import streamlit as st
import pandas as pd
import datetime

df = pd.read_csv("data/fridge_list.csv", parse_dates=["Input date", "Expiry date"], dayfirst=True)

options = ["Dairy",
            "Vegetables",
            "Fruits",
            "Meat",
            "Fish",
            "Eggs",
            "Condiments",
            "Sauces",
            "Snacks",
            "Beverages",
            "Frozen Foods",
            "Miscellaneous",
            "Other",
            ""]

st.title("Fridge List")

if st.toggle("Enable editing"):
    config = {
        "Item": st.column_config.TextColumn("Item",default=""),
        "Category": st.column_config.SelectboxColumn("Category",options=options,default=""),
        "Input date": st.column_config.DateColumn("Input date",format="DD/MM/YYYY", default=datetime.date.today(), disabled=False, required=True),
        "Expiry date": st.column_config.DateColumn("Expiry date",format="DD/MM/YYYY", default=datetime.date.today()+datetime.timedelta(days=7), disabled=False, required=True),
    }
    edf = st.data_editor(df, column_config=config, num_rows="dynamic", use_container_width=True)

    if st.button("Save changes"):
        edf.to_csv("data/fridge_list.csv", index=False, date_format="%d/%m/%Y")
        st.success("Changes saved successfully!")

else:
    config = {
        "Item": st.column_config.TextColumn("Item",default=""),
        "Category": st.column_config.TextColumn("Category",default=""),
        "Input date": st.column_config.DateColumn("Input date",format="DD/MM/YYYY", default=datetime.date.today(), disabled=False),
        "Expiry date": st.column_config.DateColumn("Expiry date",format="DD/MM/YYYY", default=datetime.date.today(), disabled=False),
    }
    st.dataframe(df, column_config=config, use_container_width=True)




