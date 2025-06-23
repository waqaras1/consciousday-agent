"""
Display components for ConsciousDay Agent
Provides components for displaying AI insights and historical entries
"""

import streamlit as st
from datetime import datetime
from typing import Dict, Optional

def display_ai_insights(reflection: str):
    """
    Display AI-generated insights in a beautiful, modern format
    
    Args:
        reflection (str): AI-generated reflection and strategy text
    """
    st.markdown("---")
    
    # Main insights header with gradient styling
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    ">
        <h2 style="color: white; margin: 0; text-align: center; font-size: 28px;">
            🤖 AI Insights & Strategy
        </h2>
        <p style="color: rgba(255,255,255,0.9); text-align: center; margin: 10px 0 0 0; font-size: 14px;">
            Personalized analysis and actionable guidance for your day
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Parse and display sections
    sections = parse_ai_response(reflection)
    
    # Display each section in a beautiful card
    for section_type, content in sections.items():
        if content.strip():
            display_insight_section(section_type, content)

def parse_ai_response(reflection: str) -> dict:
    """
    Parse the AI response into structured sections
    
    Args:
        reflection (str): Raw AI response text
        
    Returns:
        dict: Parsed sections
    """
    sections = {
        'reflection': '',
        'dream': '',
        'energy': '',
        'strategy': ''
    }
    
    lines = reflection.split('\n')
    current_section = None
    current_content = []
    
    for line in lines:
        line = line.strip()
        
        # Detect section headers
        if '**Inner Reflection Summary**' in line or 'Inner Reflection' in line:
            if current_section and current_content:
                sections[current_section] = '\n'.join(current_content).strip()
            current_section = 'reflection'
            current_content = []
        elif '**Dream Interpretation Summary**' in line or 'Dream Interpretation' in line:
            if current_section and current_content:
                sections[current_section] = '\n'.join(current_content).strip()
            current_section = 'dream'
            current_content = []
        elif '**Energy/Mindset Insight**' in line or 'Energy/Mindset' in line:
            if current_section and current_content:
                sections[current_section] = '\n'.join(current_content).strip()
            current_section = 'energy'
            current_content = []
        elif '**Suggested Day Strategy**' in line or 'Day Strategy' in line:
            if current_section and current_content:
                sections[current_section] = '\n'.join(current_content).strip()
            current_section = 'strategy'
            current_content = []
        elif line and current_section:
            current_content.append(line)
    
    # Save the last section
    if current_section and current_content:
        sections[current_section] = '\n'.join(current_content).strip()
    
    return sections

def display_insight_section(section_type: str, content: str):
    """
    Display a single insight section with beautiful styling
    
    Args:
        section_type (str): Type of section (reflection, dream, energy, strategy)
        content (str): Content to display
    """
    # Section configuration
    section_config = {
        'reflection': {
            'title': '🧠 Inner Reflection Summary',
            'icon': '🧠',
            'color': '#4F46E5',
            'bg_color': '#EEF2FF',
            'border_color': '#C7D2FE'
        },
        'dream': {
            'title': '💭 Dream Interpretation',
            'icon': '💭',
            'color': '#7C3AED',
            'bg_color': '#F3E8FF',
            'border_color': '#DDD6FE'
        },
        'energy': {
            'title': '⚡ Energy & Mindset Insight',
            'icon': '⚡',
            'color': '#059669',
            'bg_color': '#ECFDF5',
            'border_color': '#A7F3D0'
        },
        'strategy': {
            'title': '🎯 Suggested Day Strategy',
            'icon': '🎯',
            'color': '#DC2626',
            'bg_color': '#FEF2F2',
            'border_color': '#FECACA'
        }
    }
    
    config = section_config.get(section_type, {
        'title': f'📝 {section_type.title()}',
        'icon': '📝',
        'color': '#6B7280',
        'bg_color': '#F9FAFB',
        'border_color': '#E5E7EB'
    })
    
    # Create the styled section
    st.markdown(f"""
    <div style="
        background: {config['bg_color']};
        border: 2px solid {config['border_color']};
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
    ">
        <div style="
            display: flex;
            align-items: center;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid {config['border_color']};
        ">
            <span style="
                font-size: 24px;
                margin-right: 12px;
            ">{config['icon']}</span>
            <h3 style="
                color: {config['color']};
                margin: 0;
                font-size: 20px;
                font-weight: 600;
            ">{config['title']}</h3>
        </div>
        <div style="
            color: #374151;
            line-height: 1.6;
            font-size: 15px;
        ">
            {format_content(content)}
        </div>
    </div>
    """, unsafe_allow_html=True)

def format_content(content: str) -> str:
    """
    Format content with proper HTML formatting
    
    Args:
        content (str): Raw content text
        
    Returns:
        str: Formatted HTML content
    """
    # Convert markdown-style formatting to HTML
    formatted = content
    
    # Handle bullet points
    formatted = formatted.replace('\n• ', '\n<li>').replace('\n- ', '\n<li>')
    formatted = formatted.replace('\n1. ', '\n<li>').replace('\n2. ', '\n<li>').replace('\n3. ', '\n<li>')
    
    # Wrap in list tags if contains list items
    if '<li>' in formatted:
        formatted = formatted.replace('\n<li>', '<li>')
        formatted = f'<ul style="margin: 10px 0; padding-left: 20px;">{formatted}</ul>'
    
    # Handle bold text
    formatted = formatted.replace('**', '<strong>').replace('**', '</strong>')
    
    # Handle line breaks
    formatted = formatted.replace('\n\n', '</p><p>')
    formatted = f'<p>{formatted}</p>'
    
    return formatted

def display_entry(entry: Dict):
    """
    Display a beautiful historical journal entry
    
    Args:
        entry (Dict): Entry data from database
    """
    # Format the date
    try:
        date_obj = datetime.strptime(entry['date'], "%Y-%m-%d")
        formatted_date = date_obj.strftime("%B %d, %Y")
    except:
        formatted_date = entry['date']
    
    # Main entry header
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 25px;
        border-radius: 15px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        color: white;
        text-align: center;
    ">
        <h2 style="margin: 0; font-size: 28px; font-weight: 700;">
            📅 {formatted_date}
        </h2>
        <p style="margin: 10px 0 0 0; opacity: 0.9; font-size: 16px;">
            Your conscious reflection for this day
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create tabs for different sections with enhanced styling
    tab1, tab2, tab3, tab4 = st.tabs(["📝 Journal", "💭 Dream", "🎯 Intention & Priorities", "🤖 AI Insights"])
    
    with tab1:
        st.markdown("""
        <div style="
            background: #EEF2FF;
            border: 2px solid #C7D2FE;
            border-radius: 12px;
            padding: 20px;
            margin: 10px 0;
        ">
            <h3 style="color: #4F46E5; margin: 0 0 15px 0; font-size: 20px;">
                🧠 Morning Journal
            </h3>
            <div style="color: #374151; line-height: 1.6; font-size: 15px;">
        """, unsafe_allow_html=True)
        st.write(entry['journal'])
        st.markdown("</div></div>", unsafe_allow_html=True)
    
    with tab2:
        st.markdown("""
        <div style="
            background: #F3E8FF;
            border: 2px solid #DDD6FE;
            border-radius: 12px;
            padding: 20px;
            margin: 10px 0;
        ">
            <h3 style="color: #7C3AED; margin: 0 0 15px 0; font-size: 20px;">
                💭 Dream Interpretation
            </h3>
            <div style="color: #374151; line-height: 1.6; font-size: 15px;">
        """, unsafe_allow_html=True)
        st.write(entry['dream'])
        st.markdown("</div></div>", unsafe_allow_html=True)
    
    with tab3:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div style="
                background: #ECFDF5;
                border: 2px solid #A7F3D0;
                border-radius: 12px;
                padding: 20px;
                margin: 10px 0;
                height: 100%;
            ">
                <h3 style="color: #059669; margin: 0 0 15px 0; font-size: 20px;">
                    🎯 Daily Intention
                </h3>
                <div style="color: #374151; line-height: 1.6; font-size: 15px;">
            """, unsafe_allow_html=True)
            st.write(entry['intention'])
            st.markdown("</div></div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="
                background: #FEF2F2;
                border: 2px solid #FECACA;
                border-radius: 12px;
                padding: 20px;
                margin: 10px 0;
                height: 100%;
            ">
                <h3 style="color: #DC2626; margin: 0 0 15px 0; font-size: 20px;">
                    ⚡ Top 3 Priorities
                </h3>
                <div style="color: #374151; line-height: 1.6; font-size: 15px;">
            """, unsafe_allow_html=True)
            st.write(entry['priorities'])
            st.markdown("</div></div>", unsafe_allow_html=True)
    
    with tab4:
        if entry['reflection'] and entry['strategy']:
            # Combine reflection and strategy
            full_insights = f"{entry['reflection']}\n\n{entry['strategy']}"
            display_ai_insights(full_insights)
        else:
            st.markdown("""
            <div style="
                background: #F9FAFB;
                border: 2px solid #E5E7EB;
                border-radius: 12px;
                padding: 30px;
                margin: 10px 0;
                text-align: center;
                color: #6B7280;
            ">
                <div style="font-size: 48px; margin-bottom: 15px;">🤖</div>
                <h3 style="margin: 0 0 10px 0; font-size: 20px;">
                    No AI Insights Available
                </h3>
                <p style="margin: 0; font-size: 14px;">
                    AI insights were not generated for this entry.
                </p>
            </div>
            """, unsafe_allow_html=True)

def display_entry_summary(entry: Dict):
    """
    Display a beautiful summary of an entry for list views
    
    Args:
        entry (Dict): Entry data from database
    """
    try:
        date_obj = datetime.strptime(entry['date'], "%Y-%m-%d")
        formatted_date = date_obj.strftime("%B %d, %Y")
    except:
        formatted_date = entry['date']
    
    with st.expander(f"📅 {formatted_date}", expanded=False):
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 100%);
            border: 2px solid #E2E8F0;
            border-radius: 12px;
            padding: 20px;
            margin: 10px 0;
        ">
            <div style="
                display: grid;
                grid-template-columns: 2fr 1fr;
                gap: 20px;
                align-items: start;
            ">
                <div>
                    <div style="
                        background: #EEF2FF;
                        border: 1px solid #C7D2FE;
                        border-radius: 8px;
                        padding: 15px;
                        margin-bottom: 15px;
                    ">
                        <h4 style="color: #4F46E5; margin: 0 0 8px 0; font-size: 16px;">
                            🎯 Intention
                        </h4>
                        <p style="color: #374151; margin: 0; font-size: 14px; line-height: 1.5;">
                            {entry['intention'][:100] + "..." if len(entry['intention']) > 100 else entry['intention']}
                        </p>
                    </div>
                    
                    <div style="
                        background: #F3E8FF;
                        border: 1px solid #DDD6FE;
                        border-radius: 8px;
                        padding: 15px;
                    ">
                        <h4 style="color: #7C3AED; margin: 0 0 8px 0; font-size: 16px;">
                            📝 Journal Preview
                        </h4>
                        <p style="color: #374151; margin: 0; font-size: 14px; line-height: 1.5;">
                            {entry['journal'][:150] + "..." if len(entry['journal']) > 150 else entry['journal']}
                        </p>
                    </div>
                </div>
                
                <div style="
                    background: #ECFDF5;
                    border: 1px solid #A7F3D0;
                    border-radius: 8px;
                    padding: 15px;
                ">
                    <h4 style="color: #059669; margin: 0 0 8px 0; font-size: 16px;">
                        ⚡ Priorities
                    </h4>
                    <div style="color: #374151; font-size: 14px; line-height: 1.5;">
                        {entry['priorities'].replace('\n', '<br>')}
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def display_loading_message():
    """
    Display a beautiful loading message while AI is processing
    """
    st.markdown("---")
    
    # Create a beautiful loading container
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 30px;
        border-radius: 15px;
        margin: 20px 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        text-align: center;
        color: white;
    ">
        <div style="
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 15px;
        ">
            <div style="
                width: 40px;
                height: 40px;
                border: 3px solid rgba(255,255,255,0.3);
                border-top: 3px solid white;
                border-radius: 50%;
                animation: spin 1s linear infinite;
                margin-right: 15px;
            "></div>
            <h3 style="margin: 0; font-size: 24px;">🤖 AI is analyzing your inputs...</h3>
        </div>
        <p style="margin: 10px 0 0 0; font-size: 16px; opacity: 0.9;">
            Processing your reflection and generating personalized insights
        </p>
        <p style="margin: 5px 0 0 0; font-size: 12px; opacity: 0.7;">
            This may take a few moments
        </p>
    </div>
    
    <style>
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    </style>
    """, unsafe_allow_html=True)

def display_success_message():
    """
    Display a beautiful success message after saving entry
    """
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #10B981 0%, #059669 100%);
        padding: 20px;
        border-radius: 12px;
        margin: 20px 0;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
        text-align: center;
        color: white;
        animation: slideIn 0.5s ease-out;
    ">
        <div style="
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 10px;
        ">
            <span style="font-size: 24px; margin-right: 10px;">✅</span>
            <h3 style="margin: 0; font-size: 20px;">Entry Saved Successfully!</h3>
        </div>
        <p style="margin: 0; font-size: 14px; opacity: 0.9;">
            Your reflection has been recorded and AI insights are ready below
        </p>
    </div>
    
    <style>
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    </style>
    """, unsafe_allow_html=True)

def display_error_message(error: str):
    """
    Display a beautiful error message
    
    Args:
        error (str): Error message to display
    """
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #EF4444 0%, #DC2626 100%);
        padding: 20px;
        border-radius: 12px;
        margin: 20px 0;
        box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
        text-align: center;
        color: white;
        animation: shake 0.5s ease-in-out;
    ">
        <div style="
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 10px;
        ">
            <span style="font-size: 24px; margin-right: 10px;">❌</span>
            <h3 style="margin: 0; font-size: 20px;">Error Occurred</h3>
        </div>
        <p style="margin: 0; font-size: 14px; opacity: 0.9;">
            {error}
        </p>
    </div>
    
    <style>
    @keyframes shake {{
        0%, 100% {{ transform: translateX(0); }}
        25% {{ transform: translateX(-5px); }}
        75% {{ transform: translateX(5px); }}
    }}
    </style>
    """, unsafe_allow_html=True)

def display_welcome_message():
    """
    Display a beautiful welcome message for new users
    """
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 25px;
        border-radius: 15px;
        margin-bottom: 30px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        color: white;
        text-align: center;
    ">
        <h2 style="margin: 0 0 10px 0; font-size: 28px; font-weight: 700;">
            🌟 Welcome to ConsciousDay Agent!
        </h2>
        <p style="margin: 0 0 20px 0; font-size: 16px; opacity: 0.9;">
            Start your day with intention and clarity. This AI assistant will help you:
        </p>
        <div style="
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 10px;
            margin: 20px 0;
            align-items: stretch;
        ">
            <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px; backdrop-filter: blur(10px); display: flex; flex-direction: column; justify-content: center; align-items: center; height: 100%;">
                <span style="font-size: 20px; display: block; margin-bottom: 8px;">🧠</span>
                <strong style="font-size: 13px;">Reflect on your morning thoughts</strong>
            </div>
            <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px; backdrop-filter: blur(10px); display: flex; flex-direction: column; justify-content: center; align-items: center; height: 100%;">
                <span style="font-size: 20px; display: block; margin-bottom: 8px;">💭</span>
                <strong style="font-size: 13px;">Interpret your dreams for insights</strong>
            </div>
            <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px; backdrop-filter: blur(10px); display: flex; flex-direction: column; justify-content: center; align-items: center; height: 100%;">
                <span style="font-size: 20px; display: block; margin-bottom: 8px;">🎯</span>
                <strong style="font-size: 13px;">Set clear intentions & priorities</strong>
            </div>
            <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px; backdrop-filter: blur(10px); display: flex; flex-direction: column; justify-content: center; align-items: center; height: 100%;">
                <span style="font-size: 20px; display: block; margin-bottom: 8px;">⚡</span>
                <strong style="font-size: 13px;">Generate personalized strategies</strong>
            </div>
        </div>
        <p style="margin: 20px 0 0 0; font-size: 16px; font-weight: 600;">
            Ready to begin? Fill out the form below to start your daily reflection.
        </p>
    </div>
    """, unsafe_allow_html=True)

def display_stats_summary():
    """
    Display a beautiful summary of user's journaling statistics
    """
    # Get current user ID from session state
    user_id = st.session_state.get('username')
    if not user_id:
        st.error("User not authenticated. Please log in.")
        return
    
    from database.db_operations import DatabaseManager
    db = DatabaseManager()
    stats = db.get_database_stats(user_id)
    
    if stats['total_entries'] > 0:
        # Build the HTML for each stat card on a single line to avoid whitespace issues
        total_entries_card = f'<div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 12px; backdrop-filter: blur(10px);"><div style="font-size: 32px; margin-bottom: 8px;">📝</div><div style="font-size: 28px; font-weight: 700; margin-bottom: 5px;">{stats["total_entries"]}</div><div style="font-size: 14px; opacity: 0.9;">Total Reflections</div></div>'

        if stats['earliest_date']:
            earliest = datetime.strptime(stats['earliest_date'], "%Y-%m-%d").strftime("%b %d")
            started_card = f'<div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 12px; backdrop-filter: blur(10px);"><div style="font-size: 32px; margin-bottom: 8px;">🚀</div><div style="font-size: 28px; font-weight: 700; margin-bottom: 5px;">{earliest}</div><div style="font-size: 14px; opacity: 0.9;">Started</div></div>'
        else:
            started_card = '<div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 12px; backdrop-filter: blur(10px);"><div style="font-size: 32px; margin-bottom: 8px;">🚀</div><div style="font-size: 28px; font-weight: 700; margin-bottom: 5px;">Today</div><div style="font-size: 14px; opacity: 0.9;">Started</div></div>'

        if stats['latest_date']:
            latest = datetime.strptime(stats['latest_date'], "%Y-%m-%d").strftime("%b %d")
            latest_card = f'<div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 12px; backdrop-filter: blur(10px);"><div style="font-size: 32px; margin-bottom: 8px;">📅</div><div style="font-size: 28px; font-weight: 700; margin-bottom: 5px;">{latest}</div><div style="font-size: 14px; opacity: 0.9;">Last Entry</div></div>'
        else:
            latest_card = '<div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 12px; backdrop-filter: blur(10px);"><div style="font-size: 32px; margin-bottom: 8px;">📅</div><div style="font-size: 28px; font-weight: 700; margin-bottom: 5px;">None</div><div style="font-size: 14px; opacity: 0.9;">Last Entry</div></div>'

        # Combine all cards into a single HTML block
        full_html = f"""
        <div style="background: linear-gradient(135deg, #10B981 0%, #059669 100%); padding: 25px; border-radius: 15px; margin: 20px 0; box-shadow: 0 8px 32px rgba(16, 185, 129, 0.2); color: white;">
            <h3 style="margin: 0 0 20px 0; text-align: center; font-size: 24px;">
                📊 Your Journaling Journey
            </h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 20px; text-align: center;">
                {total_entries_card}
                {started_card}
                {latest_card}
            </div>
        </div>
        """
        st.markdown(full_html, unsafe_allow_html=True)

def display_empty_state():
    """
    Display a beautiful empty state when no entries exist
    """
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%);
        padding: 40px;
        border-radius: 15px;
        margin: 20px 0;
        box-shadow: 0 8px 32px rgba(245, 158, 11, 0.2);
        text-align: center;
        color: white;
    ">
        <div style="font-size: 64px; margin-bottom: 20px;">📝</div>
        <h3 style="margin: 0 0 15px 0; font-size: 28px; font-weight: 700;">
            No Entries Yet
        </h3>
        <p style="margin: 0 0 20px 0; font-size: 18px; opacity: 0.9;">
            Start your conscious journey by creating your first reflection!
        </p>
        <p style="margin: 0; font-size: 16px; opacity: 0.8;">
            Your AI assistant is ready to help you gain insights from your daily reflections.
        </p>
        <div style="
            margin-top: 25px;
            padding: 15px;
            background: rgba(255,255,255,0.1);
            border-radius: 10px;
            backdrop-filter: blur(10px);
        ">
            <span style="font-size: 20px;">✨</span>
            <span style="margin-left: 10px; font-weight: 600;">Ready to begin your journey?</span>
        </div>
    </div>
    """, unsafe_allow_html=True) 