"""
Home page for ConsciousDay Agent
Main page with form and AI processing
"""

import streamlit as st
from components.forms import create_morning_form
from components.display import display_ai_insights, display_loading_message, display_success_message, display_error_message, display_welcome_message, display_stats_summary
from agent.conscious_agent import ConsciousAgent
from database.db_operations import DatabaseManager

def show_home_page():
    """
    Display the home page with form and AI processing
    """
    # Initialize session state
    if 'ai_response' not in st.session_state:
        st.session_state.ai_response = None
    if 'form_data' not in st.session_state:
        st.session_state.form_data = None
    
    # Display welcome message and stats
    display_welcome_message()

    if st.session_state.ai_response is None:
        display_stats_summary()
    
    # Create the morning form
    form_data = create_morning_form()
    
    # Process form submission
    if form_data:
        st.session_state.form_data = form_data
        
        # Show loading message
        display_loading_message()
        
        try:
            # Initialize AI agent
            agent = ConsciousAgent()
            
            # Process inputs with AI
            ai_response = agent.process_inputs(
                journal=form_data['journal'],
                intention=form_data['intention'],
                dream=form_data['dream'],
                priorities=form_data['priorities']
            )
            
            st.session_state.ai_response = ai_response
            
            # Save to database
            db = DatabaseManager()
            
            # Split AI response into reflection and strategy
            # This is a simple split - in a more sophisticated version, 
            # you might want to parse the response more carefully
            lines = ai_response.split('\n')
            reflection_lines = []
            strategy_lines = []
            in_strategy = False
            
            for line in lines:
                if '**Suggested Day Strategy' in line or 'Day Strategy' in line:
                    in_strategy = True
                if in_strategy:
                    strategy_lines.append(line)
                else:
                    reflection_lines.append(line)
            
            reflection = '\n'.join(reflection_lines).strip()
            strategy = '\n'.join(strategy_lines).strip()
            
            success = db.save_entry(
                date=form_data['date'],
                journal=form_data['journal'],
                intention=form_data['intention'],
                dream=form_data['dream'],
                priorities=form_data['priorities'],
                reflection=reflection,
                strategy=strategy
            )
            
            if success:
                display_success_message()
            else:
                display_error_message("Failed to save entry to database")
                
        except Exception as e:
            display_error_message(f"Error processing with AI: {str(e)}")
    
    # Display AI response if available
    if st.session_state.ai_response:
        display_ai_insights(st.session_state.ai_response)
        
        # Add a button to create new entry
        if st.button("📝 Create New Entry", type="primary"):
            st.session_state.ai_response = None
            st.session_state.form_data = None
            st.rerun() 