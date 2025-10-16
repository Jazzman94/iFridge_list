"""
UI pages module (login, main page)
"""
from nicegui import ui
import pandas as pd
from auth import require_auth, logout, get_current_user
from data import load_dataframe, save_dataframe, create_new_row, delete_rows_by_ids
from pages.helpers import create_menu
from config import COLUMNS_DEFAULTS, ROW_SELECTION, DATA_PATH
from __version__ import version

# Global DataFrame
df = load_dataframe(DATA_PATH)

# ============= MAIN PAGE =============
@ui.page('/')
def index_page():
    """Main page with data grid"""
    global df
    
    # Check authentication
    require_auth()
    
    df = load_dataframe(DATA_PATH)
    
    # ============= CALLBACK FUNCTIONS =============
    async def sync_grid_to_df():
        """Synchronize data from grid to DataFrame"""
        global df
        client_data = await grid.get_client_data()
        if client_data:
            df = pd.DataFrame(client_data)
            print(f"Synced {len(df)} rows from grid to DataFrame")
    
    async def save_df():
        """Save DataFrame to CSV"""
        await sync_grid_to_df()
        if save_dataframe(df, DATA_PATH):
            ui.notify("Fridge List saved successfully!", type='positive')
        else:
            ui.notify("Error saving data!", type='negative')
    
    async def add_row():
        """Add new empty row"""
        global df
        await sync_grid_to_df()
        new_row = create_new_row(df)
        df.loc[len(df)] = new_row
        grid.run_grid_method('applyTransaction', {'add': [new_row]})
        ui.notify("Row added", type='info')
        print(f"✓ Added row with id={new_row['id']}")
    
    async def delete_selected_rows():
        """Delete selected rows"""
        global df
        selected = await grid.get_selected_rows()
        
        if not selected:
            ui.notify("No rows selected", type='warning')
            return
        
        selected_ids = [row['id'] for row in selected if 'id' in row]
        print(f"Deleting rows with IDs: {selected_ids}")
        
        df = delete_rows_by_ids(df, selected_ids)
        grid.run_grid_method('applyTransaction', {'remove': selected})
        ui.notify(f"Deleted {len(selected)} row(s)", type='positive')
        print(f"✓ Deleted {len(selected)} rows")
    
    def handle_logout():
        """Log out user"""
        logout()
        ui.notify('You have been logged out', type='info')
        ui.navigate.to('/login')
    
    # ============= UI COMPONENTS =============
    
    # Header with menu button and logout
    with ui.header().classes('items-center justify-between'):
        with ui.row().classes('items-center'):
            ui.button(icon='menu', on_click=lambda: left_drawer.toggle()).props('flat color=white')
            ui.label(f"Fridge List v{version}").classes('text-h5 q-ml-md')
        
        with ui.row().classes('items-center gap-4'):
            ui.label(f'Logged in as: {get_current_user()}').classes('text-subtitle2')
            ui.button('Logout', on_click=handle_logout, icon='logout').props('outline color=white')
    
    # Left drawer menu
    with ui.left_drawer(value=False, fixed=False).classes('bg-blue-100') as left_drawer:
        create_menu(left_drawer)
    
    # Main content
    with ui.column().classes('w-full p-4'):
        ui.label("Your Fridge Items").classes('text-h5 q-mb-md')
        
        # Data grid
        row_data = df.to_dict('records')
        print(f"✓ Initializing grid with {len(row_data)} rows")
        
        grid = ui.aggrid({
            'columnDefs': COLUMNS_DEFAULTS,
            'rowData': row_data,
            'rowSelection': ROW_SELECTION,
            ':getRowId': '(params) => params.data.id',
            'singleClickEdit': True,
        }).classes('ag-theme-alpine').style("height: 500px; width: 100%")
        
        # Action buttons
        with ui.row().classes('q-mt-md'):
            ui.button("Add Row", on_click=add_row, icon="add")
            ui.button("Delete Selected", on_click=delete_selected_rows, icon="delete", color="red")
            ui.button("Save Changes", on_click=save_df, icon="save", color="green")