# 🤖 OpenAI Setup Guide

## Quick Fix for "proxies" Error

If you're getting the error `__init__() got an unexpected keyword argument 'proxies'`, follow these steps:

### 1. Update Dependencies
```bash
pip install --upgrade openai
# or specifically
pip install openai>=1.50.0
```

### 2. Restart Your Application
After updating, restart your Flask application:
```bash
python main.py
```

## Complete Setup Guide

### 1. Get OpenAI API Key
1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign in or create an account
3. Navigate to "API Keys" section
4. Create a new API key
5. Copy the key (it starts with `sk-`)

### 2. Configure Environment Variables

#### Option A: Create .env file
```bash
# Create .env file in your project root
touch .env
```

Add these lines to your `.env` file:
```bash
FLASK_APP=main.py
FLASK_ENV=development
SECRET_KEY=dev-secret-change-me-in-production
DATABASE_URL=sqlite:///sante.db
OPENAI_API_KEY=sk-your-actual-api-key-here
OPENAI_MODEL=gpt-4o-mini
```

#### Option B: Export in terminal
```bash
export OPENAI_API_KEY="sk-your-actual-api-key-here"
export OPENAI_MODEL="gpt-4o-mini"
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Verify Configuration
Check if your API key is loaded:
```python
import os
print("API Key:", os.environ.get('OPENAI_API_KEY')[:10] + "..." if os.environ.get('OPENAI_API_KEY') else "Not set")
```

## Troubleshooting

### Common Issues

#### 1. "proxies" Error
**Problem**: `__init__() got an unexpected keyword argument 'proxies'`
**Solution**: Update OpenAI library to version 1.50.0 or higher

#### 2. "API key not configured"
**Problem**: OpenAI API key not found in environment
**Solution**: 
- Check your `.env` file exists
- Verify the API key is correct
- Restart your application after setting environment variables

#### 3. "Invalid API key"
**Problem**: API key format is incorrect
**Solution**: 
- Ensure key starts with `sk-`
- Check for extra spaces or characters
- Verify the key is active in OpenAI dashboard

#### 4. "Model not found"
**Problem**: Specified model doesn't exist or isn't accessible
**Solution**: 
- Use `gpt-4o-mini` (most accessible)
- Check your OpenAI account has access to the model
- Verify model name spelling

### 5. Rate Limiting
**Problem**: Too many requests to OpenAI API
**Solution**: 
- Wait a few minutes between requests
- Check your OpenAI usage limits
- Consider upgrading your OpenAI plan

## Testing the Integration

### 1. Test API Key
```python
from openai import OpenAI

client = OpenAI(api_key="your-api-key")
try:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Hello"}],
        max_tokens=10
    )
    print("✅ API connection successful!")
except Exception as e:
    print(f"❌ API connection failed: {e}")
```

### 2. Test in Application
1. Start your Flask app
2. Navigate to any city dashboard
3. Click "🤖 Generate Dispatch Report"
4. Check for any error messages

## Security Notes

### ⚠️ Important Security Practices
- **Never commit API keys** to version control
- **Use .env files** for local development
- **Use environment variables** in production
- **Rotate API keys** regularly
- **Monitor API usage** in OpenAI dashboard

### Production Deployment
```bash
# Set environment variables securely
export OPENAI_API_KEY="sk-production-key"
export OPENAI_MODEL="gpt-4o-mini"

# Or use your deployment platform's secure environment variable system
```

## Cost Management

### OpenAI Pricing (as of 2024)
- **gpt-4o-mini**: ~$0.00015 per 1K tokens
- **gpt-4o**: ~$0.005 per 1K tokens
- **gpt-4-turbo**: ~$0.01 per 1K tokens

### Typical Report Costs
- **Standard Report**: ~$0.00015 per report (gpt-4o-mini)
- **Comprehensive Report**: ~$0.005 per report (gpt-4o)

### Set Usage Limits
1. Go to OpenAI Platform
2. Navigate to "Usage Limits"
3. Set monthly spending limits
4. Monitor usage regularly

## Support

If you continue to have issues:

1. **Check OpenAI Status**: [status.openai.com](https://status.openai.com)
2. **Verify API Key**: Test in OpenAI Playground
3. **Check Logs**: Look for detailed error messages
4. **Update Dependencies**: Ensure all packages are current

---

*This setup guide should resolve the "proxies" error and get your OpenAI integration working properly.*
