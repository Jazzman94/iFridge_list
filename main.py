import pandas as pd
from datetime import datetime
from nicegui import ui
from config import DATE_FORMAT, COLUMNS_DEFAULTS, ROW_SELECTION, DATA_PATH
import os

def load_dataframe():
    """Loads the DataFrame from CSV or creates an empty one if the file doesn't exist"""
    if os.path.exists(DATA_PATH):
        df = pd.read_csv(DATA_PATH)
        print(f"✓ Loaded {len(df)} rows from {DATA_PATH}")
        print(f"✓ Columns: {df.columns.tolist()}")
        if not df.empty:
            print(f"✓ First row: {df.iloc[0].to_dict()}")
        return df
    else:
        print(f"✗ File {DATA_PATH} not found, creating empty DataFrame")
        return pd.DataFrame(columns=['id', 'Item', 'Category', 'Price', 'Volume/Weight', 'Input date', 'Expiry date'])

df = load_dataframe()

@ui.page('/')
def index():
    global df
    
    df = load_dataframe()
    
    async def sync_grid_to_df():
        """Synchronizes data from the grid to the DataFrame"""
        global df
        client_data = await grid.get_client_data()
        if client_data:
            df = pd.DataFrame(client_data)
            print(f"Synced {len(df)} rows from grid to DataFrame")
    
    async def save_df():
        """Saves the DataFrame to CSV"""
        await sync_grid_to_df()
        df.to_csv(DATA_PATH, index=False, date_format=DATE_FORMAT)
        ui.notify("Fridge List saved successfully!", type='positive')
        print(f"✓ Saved {len(df)} rows to {DATA_PATH}")
    
    async def add_row():
        """Adds a new empty row to the grid using transaction"""
        global df
        await sync_grid_to_df()
        
        new_id = df["id"].max() + 1 if "id" in df.columns and not df.empty else 1
        new_row = {
            "id": int(new_id),
            "Item": "",
            "Category": "Fruits",
            "Price": 0.0,
            "Volume/Weight": 0.0,
            "Input date": datetime.now().strftime(DATE_FORMAT),
            "Expiry date": datetime.now().strftime(DATE_FORMAT),
        }
        
        df.loc[len(df)] = new_row
        grid.run_grid_method('applyTransaction', {'add': [new_row]})
        
        ui.notify("Row added", type='info')
        print(f"✓ Added row with id={new_id}")
    
    async def delete_selected_rows():
        """Deletes selected rows using transaction"""
        global df
        
        selected = await grid.get_selected_rows()
        if not selected:
            ui.notify("No rows selected", type='warning')
            return
        
        selected_ids = [row['id'] for row in selected if 'id' in row]
        print(f"Deleting rows with IDs: {selected_ids}")
        
        df = df[~df['id'].isin(selected_ids)]
        df = df.reset_index(drop=True)
        
        grid.run_grid_method('applyTransaction', {'remove': selected})
        
        ui.notify(f"Deleted {len(selected)} row(s)", type='positive')
        print(f"✓ Deleted {len(selected)} rows")
    
    ui.label("Fridge List").style("font-size: 24px; font-weight: bold;")
    
    row_data = df.to_dict('records')
    print(f"✓ Initializing grid with {len(row_data)} rows")
    
    grid = ui.aggrid({
        'columnDefs': COLUMNS_DEFAULTS,
        'rowData': row_data,
        'rowSelection': ROW_SELECTION,
        ':getRowId': '(params) => params.data.id',
    }).classes('ag-theme-alpine').style("height: 500px; width: 100%")
    
    with ui.row():  
        ui.button("Add Row", on_click=add_row, icon="add")
        ui.button("Delete Selected", on_click=delete_selected_rows, icon="delete", color="red")
        ui.button("Save Changes", on_click=save_df, icon="save", color="green")

ui.run(port=8089)