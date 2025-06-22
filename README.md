# ConsciousDay Agent

"Reflect inward. Act with clarity."

A journaling-based AI assistant that reads a user's morning inputs and provides emotional insights and a daily strategy.

## Features

- **Morning Journal Input**: Free-form journaling for daily reflections
- **Dream Recording**: Capture and interpret dreams
- **Intention Setting**: Define your daily intention
- **Priority Planning**: Set top 3 priorities for the day
- **AI-Powered Insights**: Get emotional insights and strategic planning
- **Historical View**: Review previous entries by date
- **Secure Storage**: All data stored locally in SQLite database

## Tech Stack

- **UI**: Streamlit
- **LLM Agent Framework**: LangChain
- **AI API**: OpenRouter/Together AI
- **Database**: SQLite
- **Authentication**: Streamlit Auth (optional)


## Usage

1. Open the app in your browser
2. Fill in the morning form with:
   - Morning Journal (free-form)
   - Dream (free-form)
   - Intention of the Day
   - Top 3 Priorities
3. Submit to get AI-generated insights
4. View previous entries by selecting a date

## Project Structure

```
aykays-project/
├── app.py                 # Main Streamlit application
├── agent/
│   ├── __init__.py
│   └── conscious_agent.py # LangChain agent implementation
├── components/
│   ├── __init__.py
│   ├── forms.py          # Form components
│   └── display.py        # Display components
├── database/
│   ├── __init__.py
│   └── db_operations.py  # Database operations
├── views/
│   ├── __init__.py
│   ├── home.py           # Home page
│   └── history.py        # History page
├── tests/
│   ├── __init__.py
│   └── test_db.py        # Database tests
├── requirements.txt
├── .env.example
└── README.md
```

## Database Schema

```sql
CREATE TABLE entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    journal TEXT,
    intention TEXT,
    dream TEXT,
    priorities TEXT,
    reflection TEXT,
    strategy TEXT
);
```
## Deployment

The app can be deployed on Streamlit Cloud or any other platform that supports Streamlit applications.

## License

MIT License 