"""
Form components for ConsciousDay Agent
Provides reusable form elements for the Streamlit interface
"""

import streamlit as st
from datetime import datetime, date
from typing import Dict, Optional

def create_morning_form() -> Optional[Dict]:
    """
    Create the main morning reflection form
    
    Returns:
        Dict: Form data if submitted, None otherwise
    """
    # Get current user ID from session state
    user_id = st.session_state.get('username')
    if not user_id:
        st.error("User not authenticated. Please log in.")
        return None
    
    st.title("🌅 ConsciousDay Agent")
    st.markdown("_\"Reflect inward. Act with clarity.\"_")
    
    # Date selection
    selected_date = st.date_input(
        "📅 Date",
        value=date.today(),
        help="Select the date for your reflection"
    )
    
    # Check if entry already exists for this date
    from database.db_operations import DatabaseManager
    db = DatabaseManager()
    date_str = selected_date.strftime("%Y-%m-%d")
    
    if db.entry_exists(user_id, date_str):
        st.warning(f"⚠️ An entry already exists for {date_str}. You can view it in the History section.")
        return None
    
    with st.container(border=True):
        with st.form("morning_reflection_form"):
            st.markdown("### 📝 Morning Journal")
            journal = st.text_area(
                "How are you feeling this morning? What's on your mind?",
                placeholder="Share your thoughts, feelings, and any insights from your morning...",
                height=120,
                help="Write freely about your current state of mind and emotions"
            )
            
            st.markdown("### 💭 Dream")
            dream = st.text_area(
                "Did you have any dreams last night?",
                placeholder="Describe your dream or write 'No dream' if you don't remember...",
                height=100,
                help="Dreams can provide insights into your subconscious mind"
            )
            
            st.markdown("### 🎯 Intention of the Day")
            intention = st.text_input(
                "What is your main intention for today?",
                placeholder="e.g., 'I will approach challenges with patience and creativity'",
                help="Set a clear intention that will guide your actions today"
            )
            
            st.markdown("### ⭐ Top 3 Priorities")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                priority1 = st.text_input("1st Priority", placeholder="Most important task")
            with col2:
                priority2 = st.text_input("2nd Priority", placeholder="Second most important")
            with col3:
                priority3 = st.text_input("3rd Priority", placeholder="Third most important")
            
            priorities = f"1. {priority1}\n2. {priority2}\n3. {priority3}"
            
            # Submit button
            submitted = st.form_submit_button(
                "🚀 Generate Insights",
                type="primary",
                use_container_width=True
            )
            
            if submitted:
                # Validation
                if not journal.strip():
                    st.error("Please fill in your morning journal entry.")
                    return None
                
                if not intention.strip():
                    st.error("Please set your intention for the day.")
                    return None
                
                if not priority1.strip() or not priority2.strip() or not priority3.strip():
                    st.error("Please fill in all three priorities.")
                    return None
                
                return {
                    'date': date_str,
                    'journal': journal.strip(),
                    'dream': dream.strip() if dream.strip() else "No dream recorded",
                    'intention': intention.strip(),
                    'priorities': priorities
                }
    
    return None

def create_date_selector() -> Optional[str]:
    """
    Create a date selector for viewing historical entries
    
    Returns:
        str: Selected date string if a date is selected, None otherwise
    """
    # Get current user ID from session state
    user_id = st.session_state.get('username')
    if not user_id:
        st.error("User not authenticated. Please log in.")
        return None
    
    st.markdown("### 📅 Select Date to View")
    
    from database.db_operations import DatabaseManager
    db = DatabaseManager()
    available_dates = db.get_available_dates(user_id)
    
    if not available_dates:
        st.info("No entries found. Create your first reflection!")
        return None
    
    # Format dates for display
    date_options = []
    for date_str in available_dates:
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            formatted_date = date_obj.strftime("%B %d, %Y")
            date_options.append((formatted_date, date_str))
        except:
            date_options.append((date_str, date_str))
    
    if date_options:
        selected_display, selected_date = st.selectbox(
            "Choose a date:",
            options=date_options,
            format_func=lambda x: x[0]
        )
        return selected_date
    
    return None

def create_quick_stats():
    """
    Display quick statistics about the user's journal entries
    """
    # Get current user ID from session state
    user_id = st.session_state.get('username')
    if not user_id:
        st.error("User not authenticated. Please log in.")
        return
    
    from database.db_operations import DatabaseManager
    db = DatabaseManager()
    stats = db.get_database_stats(user_id)
    
    with st.container(border=True):
        st.markdown("### 📊 Quick Stats")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Entries", stats['total_entries'])
        
        with col2:
            if stats['earliest_date']:
                earliest = datetime.strptime(stats['earliest_date'], "%Y-%m-%d").strftime("%b %d")
                st.metric("First Entry", earliest)
            else:
                st.metric("First Entry", "None")
        
        with col3:
            if stats['latest_date']:
                latest = datetime.strptime(stats['latest_date'], "%Y-%m-%d").strftime("%b %d")
                st.metric("Latest Entry", latest)
            else:
                st.metric("Latest Entry", "None") 