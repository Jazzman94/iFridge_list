"""
Main application file for Fridge List
Starts NiceGUI server with authentication
"""
from nicegui import ui
from auth import STORAGE_SECRET
from pages import login_page, index_page

# Pages are automatically registered by @ui.page decorator
# login_page -> /login
# index_page -> /

if __name__ in {"__main__", "__mp_main__"}:
    ui.run(
        port=8089,
        storage_secret=STORAGE_SECRET,
        title="Fridge List App"
    )