from nicegui import ui

from auth import is_authenticated, login

# ============= LOGIN PAGE =============
@ui.page('/login')
def login_page():
    """Login page"""
    
    def try_login():
        username = username_input.value
        password = password_input.value
        
        if login(username, password):
            ui.notify(f'Welcome, {username}!', type='positive')
            ui.navigate.to('/')
        else:
            ui.notify('Invalid username or password!', type='negative')
            password_input.value = ''
    
    # If already logged in, redirect to main page
    if is_authenticated():
        ui.navigate.to('/')
        return
    
    with ui.card().classes('absolute-center'):
        ui.label('iFridge App Login').classes('text-h4 q-mb-md')
        username_input = ui.input(
            'Username', 
            on_change=lambda: username_input.props('error=false')
        ).props('outlined').classes('w-64')
        
        password_input = ui.input(
            'Password', 
            password=True, 
            password_toggle_button=True,
            on_change=lambda: password_input.props('error=false')
        ).props('outlined').classes('w-64').on('keydown.enter', try_login)
        
        ui.button('Login', on_click=try_login, icon='login').props('color=primary')