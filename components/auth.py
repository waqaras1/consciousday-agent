"""
Authentication component for ConsciousDay Agent
Optional authentication using Streamlit Authenticator
"""

import streamlit as st
import streamlit_authenticator as stauth
from streamlit_authenticator.utilities.hasher import Hasher
import yaml
from yaml.loader import SafeLoader
import os

class AuthManager:
    """
    Manages user authentication for the ConsciousDay Agent
    """
    
    def __init__(self, config_path: str = "config.yaml"):
        """
        Initialize authentication manager
        
        Args:
            config_path (str): Path to configuration file
        """
        self.config_path = config_path
        self.config = None
        self.authenticator = None
        self.init_authentication()
    
    def init_authentication(self):
        """Initialize authentication system"""
        # Create default config if it doesn't exist
        if not os.path.exists(self.config_path):
            self.create_default_config()
        
        # Load configuration
        with open(self.config_path) as file:
            self.config = yaml.load(file, Loader=SafeLoader)

        # If config is empty (e.g., corrupted), recreate and reload
        if self.config is None:
            self.create_default_config()
            with open(self.config_path) as file:
                self.config = yaml.load(file, Loader=SafeLoader)
        
        # Create authenticator
        self.authenticator = stauth.Authenticate(
            self.config['credentials'],
            self.config['cookie']['name'],
            self.config['cookie']['key'],
            self.config['cookie']['expiry_days'],
            self.config['preauthorized']
        )
    
    def create_default_config(self):
        """Create default configuration file"""
        # Generate hashed password using the correct API
        hashed_password = Hasher(['demo123']).generate()
        
        config = {
            'credentials': {
                'usernames': {
                    'demo': {
                        'email': 'demo@example.com',
                        'name': 'Demo User',
                        'password': hashed_password[0]
                    }
                }
            },
            'cookie': {
                'expiry_days': 30,
                'key': 'consciousday_key',
                'name': 'consciousday_cookie'
            },
            'preauthorized': {
                'emails': ['demo@example.com']
            }
        }
        
        with open(self.config_path, 'w') as file:
            yaml.dump(config, file, default_flow_style=False)
        self.config = config # Also update the in-memory config
    
    def login(self, location: str = 'main', fields: dict = None):
        """
        Display login form
        
        Args:
            location (str): Location where to display the form ('main' or 'sidebar')
            fields (dict): Rendered names of the fields/buttons
            
        Returns:
            tuple: (name, authentication_status, username)
        """
        if self.authenticator:
            name, authentication_status, username = self.authenticator.login(location, fields=fields)
            return name, authentication_status, username
        return None, False, None
    
    def logout(self, button_name: str = 'Logout', location: str = 'main', key: str = None):
        """Display logout button"""
        if self.authenticator:
            self.authenticator.logout(button_name, location, key)
    
    def register_user(self):
        """Display user registration form"""
        if self.authenticator:
            try:
                result = self.authenticator.register_user('main', pre_authorization=False)
                if result and result[1]: # Check if a username was returned
                    email, username, name = result
                    st.success(f'✅ User **{username}** registered successfully!')
                    st.info(f'You can now login with username: **{username}**')
                    # The library has updated the credentials in self.config in-place.
                    # We just need to save the updated config object.
                    with open(self.config_path, 'w') as file:
                        yaml.dump(self.config, file, default_flow_style=False)
                    st.balloons()
            except Exception as e:
                st.error(f"Registration error: {e}")
    
    def reset_password(self):
        """Display password reset form"""
        if self.authenticator:
            try:
                username_forgot_pw, email_forgot_password, random_password = self.authenticator.forgot_password('Forgot password')
                if username_forgot_pw:
                    st.success('New password sent securely')
                    # Random password to be transferred to user securely
                    st.info(f'New password: {random_password}')
            except Exception as e:
                st.error(e)
    
    def update_user_details(self):
        """Display user details update form"""
        if self.authenticator:
            try:
                if self.authenticator.update_user_details('Update user details', 'main'):
                    st.success('Entries updated successfully')
            except Exception as e:
                st.error(e)

def show_auth_page():
    """
    Display authentication page
    
    Returns:
        bool: True if user is authenticated, False otherwise
    """
    st.markdown("## 🔐 Authentication")
    
    auth_manager = AuthManager()
    
    # Create tabs for different auth functions
    tab1, tab2, tab3, tab4 = st.tabs(["Login", "Register", "Forgot Password", "Update Details"])
    
    with tab1:
        name, authentication_status, username = auth_manager.login()
        
        if authentication_status == False:
            st.error('Username/password is incorrect')
        elif authentication_status == None:
            st.warning('Please enter your username and password')
        elif authentication_status:
            st.success(f'Welcome {name}')
            return True
    
    with tab2:
        auth_manager.register_user()
    
    with tab3:
        auth_manager.reset_password()
    
    with tab4:
        auth_manager.update_user_details()
    
    return False

def require_auth():
    """
    Decorator to require authentication for pages
    
    Usage:
        @require_auth
        def protected_page():
            # Your page content here
            pass
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Check if user is authenticated
            if 'authenticated' not in st.session_state:
                st.session_state.authenticated = False
            
            if not st.session_state.authenticated:
                st.session_state.authenticated = show_auth_page()
                if not st.session_state.authenticated:
                    return
            
            # User is authenticated, show the page
            return func(*args, **kwargs)
        return wrapper
    return decorator 