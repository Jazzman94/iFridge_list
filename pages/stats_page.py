from nicegui import ui
import pandas as pd
from auth import require_auth, logout, get_current_user
from data import load_dataframe
from pages.helpers import create_menu
from config import DATA_PATH
from __version__ import version


# ============= STATISTICS PAGE =============
@ui.page('/stats')
def stats_page():
    """Statistics page"""
    global df
    
    # Check authentication
    require_auth()
    
    df = load_dataframe(DATA_PATH)
    
    def handle_logout():
        """Log out user"""
        logout()
        ui.notify('You have been logged out', type='info')
        ui.navigate.to('/login')
    
    # Header
    with ui.header().classes('items-center justify-between'):
        with ui.row().classes('items-center'):
            ui.button(icon='menu', on_click=lambda: left_drawer.toggle()).props('flat color=white')
            ui.label(f"Statistics v{version}").classes('text-h5 q-ml-md')
        
        with ui.row().classes('items-center gap-4'):
            ui.label(f'Logged in as: {get_current_user()}').classes('text-subtitle2')
            ui.button('Logout', on_click=handle_logout, icon='logout').props('outline color=white')
    
    # Left drawer menu
    with ui.left_drawer(value=False, fixed=False).classes('bg-blue-100') as left_drawer:
        create_menu(left_drawer)
    
    # Main content
    with ui.column().classes('w-full p-4'):
        ui.label('Statistics').classes('text-h4 q-mb-md')
        
        # Basic statistics
        with ui.card().classes('w-full q-mb-md'):
            ui.label('Overview').classes('text-h6')
            ui.separator()
            with ui.row().classes('q-mt-md q-gutter-md'):
                with ui.card().classes('text-center p-4'):
                    ui.label(f'{len(df)}').classes('text-h4 text-primary')
                    ui.label('Total Items').classes('text-subtitle2')
                
                if 'Category' in df.columns:
                    categories_count = df['Category'].nunique()
                    with ui.card().classes('text-center p-4'):
                        ui.label(f'{categories_count}').classes('text-h4 text-positive')
                        ui.label('Categories').classes('text-subtitle2')
        
        # Categories breakdown
        if 'Category' in df.columns and not df.empty:
            with ui.card().classes('w-full'):
                ui.label('Items by Category').classes('text-h6')
                ui.separator()
                
                category_counts = df['Category'].value_counts()
                
                with ui.column().classes('q-mt-md'):
                    for category, count in category_counts.items():
                        with ui.row().classes('items-center justify-between w-full'):
                            ui.label(f'{category}:').classes('text-subtitle1')
                            ui.label(f'{count} items').classes('text-body2 text-grey')
