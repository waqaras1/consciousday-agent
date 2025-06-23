"""
ConsciousDay Agent - Main Streamlit Application
A journaling-based AI assistant for daily reflection and planning
"""

import streamlit as st
import os
from views.home import show_home_page
from views.history import show_history_page
from agent.conscious_agent import ConsciousAgent
from database.db_operations import DatabaseManager
from components.auth import AuthManager

# Page configuration
st.set_page_config(
    page_title="ConsciousDay Agent",
    page_icon="icon.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a clean, theme-aware design
st.markdown("""
<style>
    /* Card/Container Styling */
    .card {
        background-color: var(--secondary-background-color);
        border-radius: 10px;
        padding: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1.5rem;
        border: 1px solid transparent;
    }

    /* Enhanced Button Styling */
    .stButton > button {
        border-radius: 8px;
        font-weight: bold;
        border: 1px solid var(--primary-color);
        background-color: transparent;
        color: var(--primary-color);
        transition: all 0.2s ease-in-out;
    }
    .stButton > button:hover {
        background-color: var(--primary-color);
        color: white;
    }
    .stButton > button:focus {
        box-shadow: 0 0 0 2px var(--secondary-background-color), 0 0 0 4px var(--primary-color) !important;
    }
    
    /* Primary "Generate" Button */
    .stButton > button[kind="primary"] {
        background-color: var(--primary-color);
        color: white;
    }
     .stButton > button[kind="primary"]:hover {
        filter: brightness(1.2);
    }

    /* Text Input Styling */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea {
        background-color: var(--background-color);
    }
    .stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 2px var(--primary-color) !important;
    }

</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Home"
    if 'ai_response' not in st.session_state:
        st.session_state.ai_response = None
    if 'form_data' not in st.session_state:
        st.session_state.form_data = None
    if 'view_entry' not in st.session_state:
        st.session_state.view_entry = None
    if 'authentication_status' not in st.session_state:
        st.session_state.authentication_status = None
    if 'name' not in st.session_state:
        st.session_state.name = None
    if 'username' not in st.session_state:
        st.session_state.username = None

def check_api_key():
    """Check if API key is configured for local and deployed environments"""
    try:
        # Primarily check Streamlit secrets for deployed environment
        openrouter_api_key = st.secrets.get("OPENROUTER_API_KEY")
        openai_api_key = st.secrets.get("OPENAI_API_KEY")
    except (FileNotFoundError, AttributeError):
        # Fallback to environment variables for local development
        openrouter_api_key = os.getenv('OPENROUTER_API_KEY')
        openai_api_key = os.getenv('OPENAI_API_KEY')

    if not openrouter_api_key and not openai_api_key:
        st.error("""
        ⚠️ **API Key Required**
        
        Please set your API key.
        
        - **For local development:** Create a `.env` file in the project root with your `OPENROUTER_API_KEY` or `OPENAI_API_KEY`.
        
        - **For Streamlit Cloud deployment:** Add your API key to the "Secrets" in your app settings.
        """)
        return False
    return True

def show_sidebar():
    """Display the sidebar navigation"""
    with st.sidebar:
        st.markdown(
            """
            <div style="text-align: center; padding-bottom: 20px;">
                <h2>ConsciousDay</h2>
                <p style="font-size: 14px; color: #666;">"Reflect inward. Act with clarity."</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
        # Navigation
        page = st.selectbox(
            "Navigate",
            ["Home", "History"],
            index=0 if st.session_state.current_page == "Home" else 1
        )
        
        if page != st.session_state.current_page:
            st.session_state.current_page = page
            st.rerun()
        
        st.markdown("---")

        auth_manager = st.session_state.get('auth_manager')
        if auth_manager and st.session_state.get('authentication_status'):
             st.sidebar.success(f"Welcome {st.session_state.name}")
             auth_manager.logout('Logout', 'sidebar')
             
             # Admin section for authenticated users
             username = st.session_state.get('username')
             if username and auth_manager.is_admin(username):
                 st.markdown("---")
                 st.markdown("### ⚙️ Admin")
                 
                 # Show user role
                 role = auth_manager.get_user_role(username)
                 st.caption(f"Role: {role.title()}")
                 
                 # Clear all users functionality
                 if st.button("🗑️ Clear All Users", type="secondary", help="Clear all registered users except demo"):
                     if auth_manager.clear_all_users(username):
                         st.rerun()
             elif username:
                 # Show regular user info
                 role = auth_manager.get_user_role(username)
                 st.caption(f"Role: {role.title()}")

        st.markdown("---")
        
        # Quick stats in sidebar
        try:
            db = DatabaseManager()
            user_id = st.session_state.get('username')
            if user_id:
                stats = db.get_database_stats(user_id)
                
                st.markdown("### 📊 Quick Stats")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Total Entries", stats['total_entries'])
                
                with col2:
                    if stats['latest_date']:
                        from datetime import datetime
                        latest = datetime.strptime(stats['latest_date'], "%Y-%m-%d").strftime("%b %d")
                        st.metric("Last Entry", latest)
                    else:
                        st.metric("Last Entry", "None")

                with col3:
                    if stats['earliest_date']:
                        from datetime import datetime
                        earliest = datetime.strptime(stats['earliest_date'], "%Y-%m-%d").strftime("%b %d")
                        st.metric("Started", earliest)
                    else:
                        st.metric("Started", "None")

        except Exception as e:
            st.error(f"Error loading stats: {e}")
        
        st.markdown("---")
        
        # API Status
        st.markdown("### 🔧 System Status")
        agent = st.session_state.get('agent')
        if agent:
            try:
                status = agent.get_agent_status()
                if status['status'] == 'active':
                    st.success(f"✅ AI Agent: Active ({status['provider']})")
                    st.caption(f"Model: {status['model']}")
                else:
                    st.error("❌ AI Agent: Inactive")
            except Exception as e:
                st.error("❌ AI Agent: Error")
                st.caption(f"Error: {str(e)}")
        else:
            st.error("❌ AI Agent: Not initialized")
        
        # About section
        st.markdown("---")
        st.markdown("### ℹ️ About")
        st.markdown("""
        **ConsciousDay Agent** is an AI-powered journaling assistant that helps you:
        
        • Reflect on your morning thoughts
        • Interpret your dreams
        • Set daily intentions
        • Plan your priorities
        • Get personalized insights
        
        Built by Waqar Ahmed with Streamlit, LangChain, and OpenRouterAPI.
        """)

def main():
    """Main application function"""
    initialize_session_state()

    # Ensure auth_manager is initialized once and stored in session state
    if 'auth_manager' not in st.session_state:
        st.session_state.auth_manager = AuthManager()
    auth_manager = st.session_state.auth_manager

    # Initialize agent and store in session state
    if 'agent' not in st.session_state:
        try:
            st.session_state.agent = ConsciousAgent()
        except Exception as e:
            st.session_state.agent = None
            st.error(f"Failed to initialize AI Agent: {e}")

    # If user is not authenticated, show the login/register page
    if not st.session_state.get('authentication_status'):
        
        st.markdown("<h1 style='text-align: center;'>Welcome to ConsciousDay Agent </h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; margin-bottom: 2rem;'>Please log in or register to continue.</p>", unsafe_allow_html=True)

        login_tab, register_tab = st.tabs(["**Login**", "**Register**"])

        with login_tab:
            name, auth_status, username = auth_manager.login('main')
            if auth_status is False:
                st.error("Username/password is incorrect")
            elif auth_status is None:
                if 'login_form_rendered' in st.session_state:
                    st.warning("Please enter your username and password")
                st.session_state['login_form_rendered'] = True
        
        with register_tab:
            auth_manager.register_user()

        # If login is successful, update session state and rerun
        if auth_status:
            st.session_state['name'] = name
            st.session_state['authentication_status'] = auth_status
            st.session_state['username'] = username
            st.rerun()

    # If user is authenticated, show the main app
    else:
        # --- Main Application ---
        show_sidebar()

        agent = st.session_state.get('agent')

        # Check API key by checking agent status
        if not agent or agent.get_agent_status()['status'] == 'inactive':
            check_api_key() # Display detailed error
            st.stop()
        
        # Main content area
        if st.session_state.current_page == "Home":
            show_home_page()
        elif st.session_state.current_page == "History":
            show_history_page()
        else:
            st.error("Page not found!")

if __name__ == "__main__":
    main()