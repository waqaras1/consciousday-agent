"""
Display components for ConsciousDay Agent
Provides components for displaying AI insights and historical entries
"""

import streamlit as st
from datetime import datetime
from typing import Dict, Optional

def display_ai_insights(reflection: str):
    """
    Display AI-generated insights in a beautiful format
    
    Args:
        reflection (str): AI-generated reflection and strategy text
    """
    st.markdown("---")
    st.markdown("## 🤖 AI Insights")
    
    # Create a nice container for the insights
    with st.container(border=True):
        # Split the reflection into sections
        sections = reflection.split('**')
        
        for i, section in enumerate(sections):
            if section.strip():
                if i % 2 == 0:  # Regular text
                    st.markdown(section)
                else:  # Bold headers
                    st.markdown(f"**{section}**")

def display_entry(entry: Dict):
    """
    Display a historical journal entry
    
    Args:
        entry (Dict): Entry data from database
    """
    # Format the date
    try:
        date_obj = datetime.strptime(entry['date'], "%Y-%m-%d")
        formatted_date = date_obj.strftime("%B %d, %Y")
    except:
        formatted_date = entry['date']
    
    st.markdown(f'<div class="card"><h2>📅 {formatted_date}</h2></div>', unsafe_allow_html=True)
    
    # Create tabs for different sections
    tab1, tab2, tab3, tab4 = st.tabs(["📝 Journal", "💭 Dream", "🎯 Intention & Priorities", "🤖 AI Insights"])
    
    with tab1:
        st.markdown("### Morning Journal")
        st.write(entry['journal'])
    
    with tab2:
        st.markdown("### Dream")
        st.write(entry['dream'])
    
    with tab3:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Intention")
            st.write(entry['intention'])
        
        with col2:
            st.markdown("### Top 3 Priorities")
            st.write(entry['priorities'])
    
    with tab4:
        if entry['reflection'] and entry['strategy']:
            # Combine reflection and strategy
            full_insights = f"{entry['reflection']}\n\n{entry['strategy']}"
            display_ai_insights(full_insights)
        else:
            st.info("No AI insights available for this entry.")

def display_entry_summary(entry: Dict):
    """
    Display a summary of an entry for list views
    
    Args:
        entry (Dict): Entry data from database
    """
    try:
        date_obj = datetime.strptime(entry['date'], "%Y-%m-%d")
        formatted_date = date_obj.strftime("%B %d, %Y")
    except:
        formatted_date = entry['date']
    
    with st.expander(f"📅 {formatted_date}"):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("**Intention:**")
            st.write(entry['intention'][:100] + "..." if len(entry['intention']) > 100 else entry['intention'])
            
            st.markdown("**Journal Preview:**")
            journal_preview = entry['journal'][:150] + "..." if len(entry['journal']) > 150 else entry['journal']
            st.write(journal_preview)
        
        with col2:
            st.markdown("**Priorities:**")
            st.write(entry['priorities'])

def display_loading_message():
    """
    Display a loading message while AI is processing
    """
    st.markdown("---")
    with st.spinner("🤖 AI is analyzing your inputs and generating insights..."):
        st.markdown("""
        <div style="text-align: center; padding: 20px;">
            <p>Processing your reflection...</p>
            <p style="font-size: 12px; color: #666;">This may take a few moments</p>
        </div>
        """, unsafe_allow_html=True)

def display_success_message():
    """
    Display a success message after saving entry
    """
    st.success("✅ Entry saved successfully! Your reflection has been recorded.")

def display_error_message(error: str):
    """
    Display an error message
    
    Args:
        error (str): Error message to display
    """
    st.error(f"❌ Error: {error}")

def display_welcome_message():
    """
    Display welcome message for new users
    """
    st.markdown("""
    <div class="card">
        <h3>🌟 Welcome to ConsciousDay Agent!</h3>
        <p>Start your day with intention and clarity. This AI assistant will help you:</p>
        <ul>
            <li>Reflect on your morning thoughts and feelings</li>
            <li>Interpret your dreams for deeper insights</li>
            <li>Set clear intentions and priorities</li>
            <li>Generate personalized strategies for your day</li>
        </ul>
        <p><strong>Ready to begin?</strong> Fill out the form below to start your daily reflection.</p>
    </div>
    """, unsafe_allow_html=True)

def display_stats_summary():
    """
    Display a summary of user's journaling statistics
    """
    from database.db_operations import DatabaseManager
    db = DatabaseManager()
    stats = db.get_database_stats()
    
    if stats['total_entries'] > 0:
        with st.container(border=True):
            st.markdown("### 📊 Your Journaling Journey")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Reflections", stats['total_entries'])
            
            with col2:
                if stats['earliest_date']:
                    earliest = datetime.strptime(stats['earliest_date'], "%Y-%m-%d").strftime("%b %d")
                    st.metric("Started", earliest)
                else:
                    st.metric("Started", "Today")
            
            with col3:
                if stats['latest_date']:
                    latest = datetime.strptime(stats['latest_date'], "%Y-%m-%d").strftime("%b %d")
                    st.metric("Last Entry", latest)
                else:
                    st.metric("Last Entry", "None")

def display_empty_state():
    """
    Display empty state when no entries exist
    """
    st.markdown("""
    <div class="card" style="text-align: center;">
        <h3>📝 No Entries Yet</h3>
        <p>Start your conscious journey by creating your first reflection!</p>
        <p>Your AI assistant is ready to help you gain insights from your daily reflections.</p>
    </div>
    """, unsafe_allow_html=True) 