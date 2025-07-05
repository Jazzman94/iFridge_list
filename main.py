import pandas as pd
from datetime import datetime
from nicegui import ui

from config import DATE_FORMAT, COLUMNS_DEFAULTS, ROW_SELECTION

# Load the CSV file with date parsing parse_dates=["Input date", "Expiry date"]
df = pd.read_csv("data/fridge_list.csv")

def save_df():
    df.to_csv("data/fridge_list.csv", index=False, date_format=DATE_FORMAT)
    ui.notify("Fridge List saved successfully!")

def add_row():
    new_row = {
        "Item": "",
        "Category": "",
        "Input date": datetime.now().strftime(DATE_FORMAT),
        "Expiry date": ""
    }
    df.loc[len(df)] = new_row
    grid.options["rowData"] = df.to_dict('records')
    grid.run_grid_method('applyTransaction', {'add': [new_row]})

ui.label("Fridge List").style("font-size: 24px; font-weight: bold;")
grid = ui.aggrid.from_pandas(df).props("virtual-scroll").style("height: 500px; width: 100%")

grid.options['columnDefs'] = COLUMNS_DEFAULTS
grid.options['rowSelection'] = ROW_SELECTION

ui.button("Add Row", on_click=add_row)
ui.button("Save Changes", on_click=save_df)

ui.run(port = 8089)