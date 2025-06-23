"""
History page for ConsciousDay Agent
Page for viewing historical journal entries
"""

import streamlit as st
from components.forms import create_date_selector, create_quick_stats
from components.display import display_entry, display_entry_summary, display_empty_state
from database.db_operations import DatabaseManager

def show_history_page():
    """
    Display the history page with previous entries.
    This function has two main states:
    1. Displaying the list of all entries.
    2. Displaying a single, full entry view.
    """
    
    # Get current user ID from session state
    user_id = st.session_state.get('username')
    if not user_id:
        st.error("User not authenticated. Please log in.")
        return
    
    # State 2: Display a single, full entry view if one is selected.
    if 'view_entry' in st.session_state and st.session_state.view_entry is not None:
        st.markdown("## 📖 Full Entry View")
        display_entry(st.session_state.view_entry)
        
        if st.button("← Back to History List"):
            del st.session_state.view_entry
            st.rerun()
        return  # Stop execution to only show the single entry

    # State 1: Display the main history page with lists and tabs.
    st.markdown("## 📚 Journal History")
    st.markdown("Review your past reflections and insights.")
    
    create_quick_stats()
    st.markdown("---")
    
    db = DatabaseManager()
    all_entries = db.get_all_entries(user_id)
    
    if not all_entries:
        display_empty_state()
        return
    
    # Create tabs for different views
    tab1, tab2 = st.tabs(["📅 Date Selector", "📋 All Entries"])
    
    with tab1:
        st.markdown("### View Specific Entry")
        selected_date = create_date_selector()
        
        if selected_date:
            entry = db.get_entry_by_date(user_id, selected_date)
            if entry:
                display_entry(entry)
            else:
                st.error("Entry not found for selected date.")
    
    with tab2:
        st.markdown("### All Your Reflections")
        
        # Add search/filter options
        col1, col2 = st.columns(2)
        
        with col1:
            search_term = st.text_input("🔍 Search entries", placeholder="Search in journal or intention...")
        
        with col2:
            sort_by = st.selectbox("📊 Sort by", ["Date (Newest)", "Date (Oldest)"])
        
        # Filter and sort entries
        filtered_entries = all_entries
        
        if search_term:
            filtered_entries = [
                entry for entry in all_entries
                if search_term.lower() in entry['journal'].lower() or 
                   search_term.lower() in entry['intention'].lower()
            ]
        
        # Sort entries
        if sort_by == "Date (Oldest)":
            filtered_entries.sort(key=lambda x: x['date'])
        else:  # Date (Newest) - default
            filtered_entries.sort(key=lambda x: x['date'], reverse=True)
        
        # Display entries
        if filtered_entries:
            st.markdown(f"**Found {len(filtered_entries)} entries**")
            
            for entry in filtered_entries:
                display_entry_summary(entry)
                
                # Add delete button for each entry
                col1, col2, col3 = st.columns([3, 1, 1])
                with col2:
                    if st.button(f"🗑️ Delete", key=f"delete_{entry['id']}"):
                        if db.delete_entry(user_id, entry['id']):
                            st.success("Entry deleted successfully!")
                            st.rerun()
                        else:
                            st.error("Failed to delete entry.")
                
                with col3:
                    if st.button(f"👁️ View Full", key=f"view_{entry['id']}"):
                        st.session_state.view_entry = entry
                        st.rerun()
                
                st.markdown("---")
        else:
            if search_term:
                st.info(f"No entries found matching '{search_term}'")
            else:
                display_empty_state() 