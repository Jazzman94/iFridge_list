"""
UI pages module (login, main page)
"""
from nicegui import ui
from auth import require_auth, logout, get_current_user
from pages.helpers import create_menu
from config import DATA_PATH
from __version__ import version


# ============= SETTINGS PAGE =============
@ui.page('/settings')
def settings_page():
    """Settings page"""
    
    # Check authentication
    require_auth()
    
    def handle_logout():
        """Log out user"""
        logout()
        ui.notify('You have been logged out', type='info')
        ui.navigate.to('/login')
    
    # Header
    with ui.header().classes('items-center justify-between'):
        with ui.row().classes('items-center'):
            ui.button(icon='menu', on_click=lambda: left_drawer.toggle()).props('flat color=white')
            ui.label(f"Settings v{version}").classes('text-h5 q-ml-md')
        
        with ui.row().classes('items-center gap-4'):
            ui.label(f'Logged in as: {get_current_user()}').classes('text-subtitle2')
            ui.button('Logout', on_click=handle_logout, icon='logout').props('outline color=white')
    
    # Left drawer menu
    with ui.left_drawer(value=False, fixed=False).classes('bg-blue-100') as left_drawer:
        create_menu(left_drawer)
    
    # Main content
    with ui.column().classes('w-full p-4'):
        ui.label('Settings').classes('text-h4 q-mb-md')
        
        with ui.card().classes('w-full'):
            ui.label('Application Settings').classes('text-h6')
            ui.separator()
            
            with ui.column().classes('q-mt-md q-gutter-md'):
                ui.label('Version:').classes('text-subtitle2')
                ui.label(f'iFridge v{version}').classes('text-body2 q-ml-md')
                
                ui.separator()
                
                ui.label('Data Location:').classes('text-subtitle2')
                ui.label(DATA_PATH).classes('text-body2 q-ml-md')
                
                ui.separator()
                
                ui.label('Coming soon:').classes('text-subtitle2')
                with ui.column().classes('q-ml-md'):
                    ui.label('• Theme customization').classes('text-body2')
                    ui.label('• Export options').classes('text-body2')
                    ui.label('• Notification settings').classes('text-body2')