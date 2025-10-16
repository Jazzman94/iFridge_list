from nicegui import ui

# ============= HELPER FUNCTION FOR MENU =============
def create_menu(drawer):
    """Create navigation menu"""
    with ui.column().classes('w-full'):
        ui.label('Navigation').classes('text-h6 q-pa-md')
        ui.separator()
        
        ui.button('🏠 Fridge List', on_click=lambda: (ui.navigate.to('/'), drawer.toggle())).props('flat color=primary align=left').classes('w-full')
        ui.button('📊 Statistics', on_click=lambda: (ui.navigate.to('/stats'), drawer.toggle())).props('flat color=primary align=left').classes('w-full')
        ui.button('⚙️ Settings', on_click=lambda: (ui.navigate.to('/settings'), drawer.toggle())).props('flat color=primary align=left').classes('w-full')