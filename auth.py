"""
User authentication module
"""
import os
from dotenv import load_dotenv
from nicegui import ui, app

# Load environment variables from .env file
load_dotenv()

# ============= LOAD USERS FROM .env =============
def load_users() -> dict:
    """Load users from .env file"""
    users = {}
    for key, value in os.environ.items():
        if key.startswith('USER_'):
            username = key.replace('USER_', '')
            users[username] = value
    
    # Fallback to test account if no users found
    if not users:
        print("⚠️ No users found in .env, using test account")
        users = {'admin': 'admin123'}
    
    print(f"✓ Loaded {len(users)} users: {list(users.keys())}")
    return users

USERS = load_users()
STORAGE_SECRET = os.getenv('STORAGE_SECRET', 'default_secret_change_me_123')

# ============= HELPER FUNCTIONS =============
def is_authenticated() -> bool:
    """Check if user is logged in"""
    return app.storage.user.get('authenticated', False)

def get_current_user() -> str:
    """Get username of currently logged in user"""
    return app.storage.user.get('username', '')

def require_auth():
    """Redirect to login page if user is not authenticated"""
    if not is_authenticated():
        ui.navigate.to('/login')

def login(username: str, password: str) -> bool:
    """
    Authenticate user
    
    Returns:
        True if login successful, False otherwise
    """
    if username in USERS and USERS[username] == password:
        app.storage.user['authenticated'] = True
        app.storage.user['username'] = username
        return True
    return False

def logout():
    """Log out current user"""
    app.storage.user.clear()