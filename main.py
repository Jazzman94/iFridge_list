import pandas as pd
from datetime import datetime
from nicegui import ui
from config import DATE_FORMAT, COLUMNS_DEFAULTS, ROW_SELECTION, DATA_PATH

df = pd.read_csv(DATA_PATH)

@ui.page('/')
def index():
    global df
    
    async def sync_grid_to_df():
        """Synchronizes data from the grid to the DataFrame"""
        global df
        client_data = await grid.get_client_data()
        if client_data:
            df = pd.DataFrame(client_data)
        
    async def save_df():
        """Saves the DataFrame to CSV"""
        await sync_grid_to_df()
        df.to_csv(DATA_PATH, index=False, date_format=DATE_FORMAT)
        ui.notify("Fridge List saved successfully!", type='positive')
    
    async def add_row():
        """Adds a new empty row to the grid"""
        global df
        await sync_grid_to_df()
        
        new_id = df["id"].max() + 1 if "id" in df.columns and not df.empty else 1
        new_row = {
            "id": new_id,
            "Item": "",
            "Category": "Fruits",
            "Price": 0.0,
            "Volume/Weight": 0.0,
            "Input date": datetime.now().strftime(DATE_FORMAT),
            "Expiry date": datetime.now().strftime(DATE_FORMAT),
        }
        
        df.loc[len(df)] = new_row
        
        grid.options['rowData'] = df.to_dict('records')
        grid.update()
        
        ui.notify("Row added", type='info')
    
    async def delete_selected_rows():
        """Deletes selected rows"""
        global df
        selected = await grid.get_selected_rows()
        
        if not selected:
            ui.notify("No rows selected", type='warning')
            return
        
        selected_ids = [row['id'] for row in selected if 'id' in row]
        
        df = df[~df['id'].isin(selected_ids)]
        df = df.reset_index(drop=True)
        
        grid.options['rowData'] = df.to_dict('records')
        grid.update()
        
        ui.notify(f"Deleted {len(selected)} row(s)", type='positive')
    
    ui.label("Fridge List").style("font-size: 24px; font-weight: bold;")
    
    grid = ui.aggrid({
        'columnDefs': COLUMNS_DEFAULTS,
        'rowData': df.to_dict('records'),
        'rowSelection': ROW_SELECTION,
    }).classes('ag-theme-alpine').style("height: 500px; width: 100%")
    
    with ui.row():
        ui.button("Add Row", on_click=add_row, icon="add")
        ui.button("Delete Selected", on_click=delete_selected_rows, icon="delete", color="red")
        ui.button("Save Changes", on_click=save_df, icon="save", color="green")

ui.run(port=8089)