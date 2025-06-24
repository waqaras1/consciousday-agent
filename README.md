# ConsciousDay Agent 🌅

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

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/waqaras1/consciousday-agent.git
   cd consciousday-agent
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp env_example.txt .env
   ```
   
   Edit `.env` and add your API key:
   ```env
   OPENROUTER_API_KEY=your_api_key_here
   # or
   OPENAI_API_KEY=your_api_key_here
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Access the app**
   - Open your browser to `http://localhost:8501`
   - Login with demo credentials:
     - Username: `demo`
     - Password: `demo123`

## 🔧 Configuration

### API Keys

**OpenRouter (Recommended)**
- Sign up at [OpenRouter](https://openrouter.ai/)
- Get your API key from the dashboard
- Set `OPENROUTER_API_KEY` in your `.env` file

**OpenAI (Alternative)**
- Sign up at [OpenAI Platform](https://platform.openai.com/)
- Get your API key from the dashboard
- Set `OPENAI_API_KEY` in your `.env` file

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENROUTER_API_KEY` | OpenRouter API key | - |
| `OPENAI_API_KEY` | OpenAI API key | - |
| `OPENROUTER_MODEL_NAME` | AI model to use | `openai/gpt-3.5-turbo` |
| `APP_URL` | Application URL | `http://localhost:8501` |
| `DB_PATH` | Database file path | `entries.db` |

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

## 🧪 Testing

Run the test suite:

```bash
python -m pytest tests/ -v
```

## 🚀 Deployment

### Streamlit Cloud

1. **Fork this repository** to your GitHub account

2. **Deploy to Streamlit Cloud**:
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub account
   - Select this repository
   - Set the main file path to `app.py`

3. **Configure secrets**:
   - In your Streamlit Cloud app settings
   - Add your API keys to the secrets section:
   ```toml
   OPENROUTER_API_KEY = "your_api_key_here"
   # or
   OPENAI_API_KEY = "your_api_key_here"
   ```

4. **Deploy** and access your app!

### Local Production

For local production deployment:

```bash
# Install production dependencies
pip install -r requirements.txt

# Set environment variables
export OPENROUTER_API_KEY="your_api_key_here"

# Run with production settings
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

## 🔒 Security Features

- **User Authentication**: Secure login system with role-based access
- **Data Isolation**: Users can only access their own journal entries
- **Input Validation**: All inputs are validated and sanitized
- **Error Handling**: Comprehensive error handling and logging
- **Environment Variables**: Sensitive data stored in environment variables

## 🛠️ Troubleshooting

### Common Issues

**1. API Key Error**
```
Error: API key not found
```
**Solution**: Make sure your API key is set in `.env` file or Streamlit secrets.

**2. Database Error**
```
Error: Database initialization failed
```
**Solution**: Check file permissions and ensure the app can write to the current directory.

**3. Authentication Error**
```
Error: Authentication system failed to initialize
```
**Solution**: Check if `config.yaml` exists and has proper permissions.

**4. Import Error**
```
ModuleNotFoundError: No module named 'langchain'
```
**Solution**: Install dependencies: `pip install -r requirements.txt`

### Debug Mode

Enable debug mode by setting in your `.env`:
```env
DEBUG=true
LOG_LEVEL=DEBUG
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Add tests for new functionality
5. Run tests: `python -m pytest tests/ -v`
6. Commit your changes: `git commit -am 'Add feature'`
7. Push to the branch: `git push origin feature-name`
8. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- AI powered by [LangChain](https://langchain.com/) and [OpenRouter](https://openrouter.ai/)
- Authentication by [Streamlit Authenticator](https://github.com/mkhorasani/Streamlit-Authenticator)

## 📞 Support

If you encounter any issues or have questions:

1. Check the [troubleshooting section](#troubleshooting)
2. Search existing [issues](https://github.com/waqaras1/consciousday-agent/issues)
3. Create a new issue with detailed information

---

**Made with ❤️ by Waqar Ahmed** 