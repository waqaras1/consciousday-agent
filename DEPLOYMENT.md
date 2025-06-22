# Deployment Guide - ConsciousDay Agent

This guide will help you deploy the ConsciousDay Agent to various platforms.

## Local Development

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd aykays-project
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the project root:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Run tests**
   ```bash
   pytest tests/
   ```

## Streamlit Cloud Deployment

1. **Push to GitHub**
   - Create a new repository on GitHub
   - Push your code to the repository

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Set the main file path to `app.py`
   - Add your secrets in the Streamlit Cloud dashboard:
     - Go to Settings → Secrets
     - Add your API key:
       ```toml
       OPENAI_API_KEY = "your_api_key_here"
       ```

3. **Deploy**
   - Click "Deploy"
   - Your app will be available at `https://your-app-name.streamlit.app`

## Environment Variables

The following environment variables can be configured:

- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `OPENROUTER_API_KEY`: Alternative API key for OpenRouter
- `TOGETHER_API_KEY`: Alternative API key for Together AI

## Database

The application uses SQLite for local storage. The database file (`entries.db`) will be created automatically when you first run the application.

For production deployments, consider:
- Using a cloud database (PostgreSQL, MySQL)
- Implementing proper backup strategies
- Setting up data retention policies

## Security Considerations

1. **API Keys**: Never commit API keys to version control
2. **Authentication**: The app includes optional authentication using Streamlit Authenticator
3. **Data Privacy**: All data is stored locally by default
4. **HTTPS**: Use HTTPS in production deployments

## Troubleshooting

### Common Issues

1. **API Key Error**
   - Ensure your API key is correctly set in environment variables
   - Check that you have sufficient credits in your OpenAI account

2. **Database Errors**
   - Ensure the application has write permissions in the project directory
   - Check that SQLite is available in your environment

3. **Import Errors**
   - Make sure all dependencies are installed: `pip install -r requirements.txt`
   - Check that you're using the correct Python version (3.8+)

### Getting Help

- Check the Streamlit documentation: https://docs.streamlit.io
- Review the LangChain documentation: https://python.langchain.com
- Open an issue in the project repository

## Performance Optimization

1. **Caching**: The app uses Streamlit's session state for caching
2. **Database Indexing**: Consider adding indexes for frequently queried fields
3. **API Rate Limiting**: Implement rate limiting for API calls
4. **Response Caching**: Cache AI responses to reduce API costs

## Monitoring

Consider implementing:
- Application logging
- Error tracking (e.g., Sentry)
- Performance monitoring
- Usage analytics 