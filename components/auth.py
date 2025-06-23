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
        
        # Update existing configs to include roles if missing
        self.update_existing_users_with_roles()
        
        # Create authenticator
        self.authenticator = stauth.Authenticate(
            self.config['credentials'],
            self.config['cookie']['name'],
            self.config['cookie']['key'],
            self.config['cookie']['expiry_days'],
            self.config['preauthorized']
        )
    
    def update_existing_users_with_roles(self):
        """Update existing users to include roles if missing"""
        if not self.config or 'credentials' not in self.config:
            return
        
        usernames = self.config.get('credentials', {}).get('usernames', {})
        updated = False
        
        for username, user_data in usernames.items():
            if 'role' not in user_data:
                # Set demo user as admin, others as regular users
                if username == 'demo':
                    user_data['role'] = 'admin'
                else:
                    user_data['role'] = 'user'
                updated = True
        
        # Save updated config if changes were made
        if updated:
            try:
                with open(self.config_path, 'w') as file:
                    yaml.dump(self.config, file, default_flow_style=False)
            except Exception as e:
                st.error(f"Error updating user roles: {e}")
    
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
                        'password': hashed_password[0],
                        'role': 'admin'  # Demo user is admin by default
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
    
    def is_admin(self, username: str) -> bool:
        """
        Check if a user has admin privileges
        
        Args:
            username (str): Username to check
            
        Returns:
            bool: True if user is admin, False otherwise
        """
        if not self.config or 'credentials' not in self.config:
            return False
        
        usernames = self.config.get('credentials', {}).get('usernames', {})
        user_data = usernames.get(username, {})
        
        # Check if user has admin role
        return user_data.get('role') == 'admin'
    
    def get_user_role(self, username: str) -> str:
        """
        Get the role of a user
        
        Args:
            username (str): Username to get role for
            
        Returns:
            str: User role ('admin' or 'user'), defaults to 'user'
        """
        if not self.config or 'credentials' not in self.config:
            return 'user'
        
        usernames = self.config.get('credentials', {}).get('usernames', {})
        user_data = usernames.get(username, {})
        
        return user_data.get('role', 'user')
    
    def set_user_role(self, username: str, role: str) -> bool:
        """
        Set the role of a user (admin only)
        
        Args:
            username (str): Username to set role for
            role (str): Role to set ('admin' or 'user')
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.config or 'credentials' not in self.config:
            return False
        
        usernames = self.config.get('credentials', {}).get('usernames', {})
        if username not in usernames:
            return False
        
        # Update user role
        usernames[username]['role'] = role
        
        # Save updated config
        try:
            with open(self.config_path, 'w') as file:
                yaml.dump(self.config, file, default_flow_style=False)
            return True
        except Exception as e:
            st.error(f"Error updating user role: {e}")
            return False
    
    def login(self, title: str, subheader: str):
        """
        Display login form using st.tabs.
        
        Args:
            title (str): The title for the login page.
            subheader (str): The subheader for the login page.
            
        Returns:
            tuple: (name, authentication_status, username)
        """
        if self.authenticator:
            st.markdown(f"<h1 style='text-align: center;'>{title}</h1>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align: center; margin-bottom: 2rem;'>{subheader}</p>", unsafe_allow_html=True)

            login_tab, register_tab = st.tabs(["**Login**", "**Register**"])

            with login_tab:
                # The modern way to call the login method
                name, authentication_status, username = self.authenticator.login()

            with register_tab:
                try:
                    if self.authenticator.register_user(pre_authorization=False):
                        st.success('User registered successfully')
                        # Save updated config
                        with open(self.config_path, 'w') as file:
                            yaml.dump(self.config, file, default_flow_style=False)
                except Exception as e:
                    st.error(e)
            
            return name, authentication_status, username
            
        return None, False, None
    
    def logout(self, button_name: str = 'Logout', location: str = 'main'):
        """Display logout button"""
        if self.authenticator:
            self.authenticator.logout(button_name, location=location)
    
    def register_user(self):
        """Handles user registration logic"""
        try:
            if self.authenticator.register_user(pre_authorization=False):
                st.success("User registered successfully")
                # Save updated config to file
                with open(self.config_path, 'w') as file:
                    yaml.dump(self.config, file, default_flow_style=False)
        except Exception as e:
            st.error(e)

    def reset_password(self):
        """Handles reset password logic"""
        if self.authenticator.reset_password(st.session_state["username"]):
            st.success("Password modified successfully")
            # Save updated config to file
            with open(self.config_path, 'w') as file:
                yaml.dump(self.config, file, default_flow_style=False)

    def update_user_details(self):
        """Handles update user details logic"""
        if self.authenticator.update_user_details(st.session_state["username"]):
            st.success("Entries updated successfully")
            # Save updated config to file
            with open(self.config_path, 'w') as file:
                yaml.dump(self.config, file, default_flow_style=False)
                
    def clear_all_users(self, username: str = None):
        """
        Clear all users from the config file, except for the demo user
        
        Args:
            username (str): The username of the user trying to clear users
        """
        if username and self.is_admin(username):
            if self.config and 'credentials' in self.config:
                usernames = self.config['credentials'].get('usernames', {})
                # Filter to keep only the 'demo' user
                demo_user = {k: v for k, v in usernames.items() if k == 'demo'}
                
                self.config['credentials']['usernames'] = demo_user
                
                # Save updated config
                try:
                    with open(self.config_path, 'w') as file:
                        yaml.dump(self.config, file, default_flow_style=False)
                    st.success("All non-admin users cleared.")
                    return True
                except Exception as e:
                    st.error(f"Error clearing users: {e}")
                    return False
        else:
            st.error("You are not authorized to perform this action.")
            return False

    def upgrade_user_to_admin(self, target_username: str, admin_username: str = None) -> bool:
        """
        Upgrade a user to admin
        
        Args:
            target_username (str): The user to be upgraded
            admin_username (str): The user performing the action
            
        Returns:
            bool: True if successful, False otherwise
        """
        if admin_username and self.is_admin(admin_username):
            if self.set_user_role(target_username, 'admin'):
                st.success(f"User '{target_username}' has been upgraded to admin.")
                return True
            else:
                st.error(f"Failed to upgrade user '{target_username}'.")
                return False
        else:
            st.error("You are not authorized to perform this action.")
            return False

def show_auth_page():
    """
    Shows a standalone authentication page with tabs for login, register, etc.
    This function can be called from anywhere in the app to show the auth UI.
    """
    st.markdown("<h1 style='text-align: center;'>Welcome to ConsciousDay Agent</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; margin-bottom: 2rem;'>Please log in or register to continue.</p>", unsafe_allow_html=True)

    auth_manager = AuthManager()

    # Create tabs for authentication actions
    tab1, tab2, tab3, tab4 = st.tabs(["Login", "Register", "Update Details", "Reset Password"])

    with tab1:
        name, authentication_status, username = auth_manager.login("Login", "Please enter your credentials")
        
        if authentication_status == False:
            st.error("Username/password is incorrect")
        elif authentication_status == None:
            st.warning("Please enter your username and password")
        
        if authentication_status:
            st.session_state['name'] = name
            st.session_state['authentication_status'] = authentication_status
            st.session_state['username'] = username
            st.rerun()

    with tab2:
        auth_manager.register_user()

    with tab3:
        if st.session_state["authentication_status"]:
            auth_manager.update_user_details()
        else:
            st.warning("Please login to update your details")

    with tab4:
        if st.session_state["authentication_status"]:
            auth_manager.reset_password()
        else:
            st.warning("Please login to reset your password")

# --- Decorator for authentication ---
def require_auth():
    """
    A decorator that checks for authentication before running a page.
    If the user is not authenticated, it shows the login page.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Check if user is authenticated
            if not st.session_state.get("authentication_status"):
                show_auth_page()
            else:
                return func(*args, **kwargs)
        return wrapper
    return decorator 