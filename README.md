# ConsciousDay Agent 

A powerful AI-powered journaling assistant that helps you reflect on your mornings, interpret dreams, set intentions, and create actionable daily strategies.

## ✨ Features

- **🌅 Morning Reflection**: Capture your thoughts and feelings each morning
- **💭 Dream Interpretation**: Get AI insights into your dreams
- **🎯 Intention Setting**: Set clear daily intentions
- **📋 Priority Planning**: Define your top 3 priorities
- **🤖 AI Insights**: Get personalized analysis and actionable strategies
- **📚 History Tracking**: Review past reflections and insights
- **👤 User Authentication**: Secure multi-user system with admin features
- **📊 Progress Analytics**: Track your journaling journey

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- An API key from [OpenRouter](https://openrouter.ai/) or [OpenAI](https://platform.openai.com/)


## 🏗️ Project Structure

```
consciousday-agent/
├── app.py                 # Main Streamlit application
├── agent/
│   └── conscious_agent.py # AI agent implementation
├── components/
│   ├── auth.py           # Authentication system
│   ├── display.py        # UI display components
│   └── forms.py          # Form components
├── database/
│   └── db_operations.py  # Database operations
├── views/
│   ├── home.py           # Home page
│   └── history.py        # History page
├── tests/
│   └── test_db.py        # Database tests
├── config.yaml           # Authentication config
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## 🚀 Deployment

### Streamlit Cloud


## 🔒 Security Features

- **User Authentication**: Secure login system with role-based access
- **Data Isolation**: Users can only access their own journal entries
- **Input Validation**: All inputs are validated and sanitized
- **Error Handling**: Comprehensive error handling and logging
- **Environment Variables**: Sensitive data stored in environment variables


## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- AI powered by [LangChain](https://langchain.com/) and [OpenRouter](https://openrouter.ai/)
- Authentication by [Streamlit Authenticator](https://github.com/mkhorasani/Streamlit-Authenticator)

---

**Made with ❤️ by Waqar Ahmed** 
