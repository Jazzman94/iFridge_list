"""
Main application file for Fridge List
Starts NiceGUI server with authentication
"""
from nicegui import ui
from auth import STORAGE_SECRET
from pages.login_page import login_page
from pages.main_page import index_page
from pages.settings_page import settings_page
from pages.stats_page import stats_page
from pages.freezer_page import index_page as freezer_page
from pages.cabinet_page import index_page as cabinet_page

# Pages are automatically registered by @ui.page decorator
# login_page -> /login
# index_page -> /
# settings_page -> /settings
# stats_page -> /stats


if __name__ in {"__main__", "__mp_main__"}:
    ui.run(
        port=8089,
        storage_secret=STORAGE_SECRET,
        title="Fridge List App"
    )