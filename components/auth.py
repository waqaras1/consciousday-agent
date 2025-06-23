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
    
    def clear_all_users(self, username: str = None):
        """
        Clear all users and reset to default configuration (admin only)
        
        Args:
            username (str): Username of the user attempting this action
            
        Returns:
            bool: True if successful, False otherwise
        """
        # Check if user has admin privileges
        if username and not self.is_admin(username):
            st.error("❌ **Access Denied**: Only administrators can perform this action.")
            return False
        
        try:
            # Create default config (which only has the demo user)
            self.create_default_config()
            st.success('✅ All users cleared successfully!')
            st.info('System reset to default configuration with demo user only.')
            st.balloons()
            return True
        except Exception as e:
            st.error(f"Error clearing users: {e}")
            return False
    
    def upgrade_user_to_admin(self, target_username: str, admin_username: str = None) -> bool:
        """
        Upgrade a user to admin role (admin only)
        
        Args:
            target_username (str): Username to upgrade to admin
            admin_username (str): Username of the admin performing the action
            
        Returns:
            bool: True if successful, False otherwise
        """
        # Check if the performing user is admin
        if admin_username and not self.is_admin(admin_username):
            st.error("❌ **Access Denied**: Only administrators can perform this action.")
            return False
        
        return self.set_user_role(target_username, 'admin')

def show_auth_page():
    """
    Display authentication page
    
    Returns:
        bool: True if user is authenticated, False otherwise
    """
    st.markdown("## 🔐 Authentication")
    
    auth_manager = AuthManager()
    
    # Create tabs for different auth functions
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Login", "Register", "Forgot Password", "Update Details", "Clear All Users"])
    
    with tab1:
        name, authentication_status, username = auth_manager.login("Login", "Please enter your credentials")
        
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
    
    with tab5:
        st.warning("⚠️ **Danger Zone**")
        st.markdown("This will delete **ALL** registered users and reset the system to default configuration.")
        st.markdown("Only the demo user will remain.")
        
        if st.button("🗑️ Clear All Users", type="secondary"):
            if auth_manager.clear_all_users():
                st.rerun()
    
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