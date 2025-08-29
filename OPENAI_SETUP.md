# 🤖 OpenAI Integration Setup Guide

## 🚀 Quick Start

This guide will help you set up OpenAI integration for the Santé epidemiological surveillance system, enabling AI-powered executive report generation and intelligent data analysis.

## ⚡ Quick Fix for "proxies" Error

If you encounter the error `__init__() got an unexpected keyword argument 'proxies'`, follow these steps:

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

## 🔑 Complete Setup Guide

### 1. Get OpenAI API Key
1. Visit [OpenAI Platform](https://platform.openai.com/)
2. Sign in or create an account
3. Navigate to "API Keys" section
4. Create a new API key
5. Copy the key (it starts with `sk-`)

### 2. Configure Environment Variables

#### Option A: Create .env file (Recommended)
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

## 🔧 Troubleshooting

### Common Issues and Solutions

#### 1. "proxies" Error
**Problem**: `__init__() got an unexpected keyword argument 'proxies'`
**Solution**: Update OpenAI library to version 1.50.0 or higher
**Cause**: Incompatibility between older OpenAI library versions and newer Flask/Werkzeug versions

#### 2. "API key not configured"
**Problem**: OpenAI API key not found in environment
**Solution**: 
- Check your `.env` file exists and is in the project root
- Verify the API key variable name is correct (`OPENAI_API_KEY`)
- Restart your application after setting environment variables
- Ensure no spaces around the `=` sign in `.env` file

#### 3. "Invalid API key"
**Problem**: API key format is incorrect
**Solution**: 
- Ensure key starts with `sk-`
- Check for extra spaces or characters
- Verify the key is active in OpenAI dashboard
- Copy the key exactly as shown in OpenAI platform

#### 4. "Model not found"
**Problem**: Specified model doesn't exist or isn't accessible
**Solution**: 
- Use `gpt-4o-mini` (most accessible and cost-effective)
- Check your OpenAI account has access to the model
- Verify model name spelling (case-sensitive)
- Consider upgrading your OpenAI plan if needed

#### 5. Rate Limiting
**Problem**: Too many requests to OpenAI API
**Solution**: 
- Wait a few minutes between requests
- Check your OpenAI usage limits in the dashboard
- Consider upgrading your OpenAI plan
- Implement request throttling in your application

## 🧪 Testing the Integration

### 1. Test API Key Connection
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
    print(f"Response: {response.choices[0].message.content}")
except Exception as e:
    print(f"❌ API connection failed: {e}")
```

### 2. Test in Santé Application
1. Start your Flask app: `python main.py`
2. Navigate to any city dashboard
3. Click "🤖 Generate Dispatch Report" button
4. Check for any error messages in the console
5. Verify the report is generated successfully

### 3. Test Report Generation
```python
# Test the report generator service directly
from services.report_generator import ReportGenerator
import os

# Set API key for testing
os.environ['OPENAI_API_KEY'] = 'your-test-key'

try:
    generator = ReportGenerator()
    # Test with a sample city ID (you'll need valid data in your database)
    report, error = generator.generate_dispatch_report(1)
    if error:
        print(f"❌ Error: {error}")
    else:
        print(f"✅ Report generated: {report[:100]}...")
except Exception as e:
    print(f"❌ Service error: {e}")
```

## 🔒 Security Best Practices

### ⚠️ Critical Security Guidelines
- **Never commit API keys** to version control (add `.env` to `.gitignore`)
- **Use .env files** for local development only
- **Use secure environment variables** in production
- **Rotate API keys** regularly (every 90 days recommended)
- **Monitor API usage** in OpenAI dashboard
- **Set spending limits** to prevent unexpected charges

### Production Deployment Security
```bash
# Set environment variables securely (never in code)
export OPENAI_API_KEY="sk-production-key"
export OPENAI_MODEL="gpt-4o-mini"

# Or use your deployment platform's secure environment variable system
# (Heroku, AWS, Docker, etc.)
```

### Environment File Security
```bash
# Ensure .env is in .gitignore
echo ".env" >> .gitignore

# Set proper file permissions
chmod 600 .env
```

## 💰 Cost Management

### OpenAI Pricing (as of 2024)
- **gpt-4o-mini**: ~$0.00015 per 1K tokens (most cost-effective)
- **gpt-4o**: ~$0.005 per 1K tokens (higher quality)
- **gpt-4-turbo**: ~$0.01 per 1K tokens (highest quality)

### Typical Report Costs in Santé
- **Standard Epidemiological Report**: ~$0.00015 per report (gpt-4o-mini)
- **Comprehensive Health Analysis**: ~$0.005 per report (gpt-4o)
- **Executive Summary**: ~$0.0005 per report (gpt-4o-mini)

### Setting Usage Limits
1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Navigate to "Usage Limits" section
3. Set monthly spending limits (recommended: start with $10-20)
4. Monitor usage regularly
5. Set up billing alerts

## 🎯 Santé-Specific Features

### AI-Powered Epidemiological Reports
Once configured, Santé will automatically generate:
- **Executive Summaries**: Professional reports for health authorities
- **Risk Assessments**: AI-analyzed transmission patterns
- **Recommendations**: Data-driven public health guidance
- **Trend Analysis**: Intelligent interpretation of epidemiological data

### Report Customization
The AI generates reports based on:
- Current transmission rates (R(t))
- Basic reproduction numbers (R0)
- Hospitalization trends
- Geographic risk factors
- Historical case patterns

## 🆘 Support and Troubleshooting

### Getting Help

1. **Check OpenAI Status**: [status.openai.com](https://status.openai.com)
2. **Verify API Key**: Test in [OpenAI Playground](https://platform.openai.com/playground)
3. **Check Application Logs**: Look for detailed error messages in Flask console
4. **Update Dependencies**: Ensure all packages are current
5. **Test API Connection**: Use the test scripts above

### Common Error Messages

| Error | Solution |
|-------|----------|
| `API key not configured` | Set `OPENAI_API_KEY` in environment |
| `Invalid API key` | Check key format and validity |
| `Model not found` | Use `gpt-4o-mini` or check model access |
| `Rate limit exceeded` | Wait and check usage limits |
| `Insufficient credits` | Add billing information to OpenAI account |

### Debug Mode
Enable Flask debug mode for detailed error information:
```bash
export FLASK_ENV=development
export FLASK_DEBUG=1
python main.py
```

## 🔮 Advanced Configuration

### Custom Model Selection
```bash
# Use different models based on your needs
export OPENAI_MODEL="gpt-4o"        # Higher quality, higher cost
export OPENAI_MODEL="gpt-4o-mini"   # Balanced quality and cost
export OPENAI_MODEL="gpt-3.5-turbo" # Lower cost, good performance
```

### Temperature and Token Settings
Modify `services/report_generator.py` to adjust AI behavior:
```python
response = client.chat.completions.create(
    model=self.model,
    messages=[...],
    max_tokens=1000,        # Control report length
    temperature=0.7,         # Control creativity (0.0-1.0)
    top_p=0.9               # Control response diversity
)
```

---

*This setup guide will get your OpenAI integration working with Santé, enabling intelligent epidemiological analysis and professional report generation.*
