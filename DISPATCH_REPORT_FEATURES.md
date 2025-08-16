# 🤖 Dispatch Report Features

## Overview

The **Generate Dispatch Report** functionality uses OpenAI's advanced AI models to automatically generate professional executive reports for health authorities and stakeholders. These reports provide comprehensive summaries of epidemiological data and actionable insights.

## Features

### 🎯 **AI-Powered Report Generation**
- **OpenAI Integration**: Uses GPT-4o-mini for intelligent analysis
- **Contextual Understanding**: AI analyzes city-specific epidemiological data
- **Professional Format**: Structured reports suitable for health authorities

### 📊 **Report Content Structure**
1. **Executive Summary**: High-level overview (2-3 sentences)
2. **Key Findings**: Critical insights from data analysis (3-4 bullet points)
3. **Risk Assessment**: Professional evaluation of current risk levels
4. **Recommendations**: Actionable advice for public health officials
5. **Next Steps**: Strategic guidance for continued monitoring

### 💾 **Export & Distribution**
- **TXT Format**: Clean text format for easy integration
- **Professional Naming**: Files named with city, state, and country
- **Download Ready**: Direct download from the web interface

## How It Works

### 1. **Data Collection**
The system automatically gathers:
- City information (name, state, country)
- Current epidemiological indicators (R(t), R0, hospitalization rate)
- Recent case trends (last 10 weeks)
- Risk level assessment

### 2. **AI Analysis**
OpenAI processes the data to generate:
- Contextual understanding of the situation
- Professional language appropriate for health authorities
- Actionable recommendations based on current trends

### 3. **Report Generation**
The AI creates a structured report including:
- Executive summary for quick decision-making
- Detailed analysis of key metrics
- Risk assessment with clear categorization
- Specific recommendations for public health actions

## Technical Implementation

### **Architecture**
- **Service Layer**: `services/report_generator.py`
- **Controller**: New routes in `controllers/dashboard.py`
- **Template**: Dedicated `templates/dispatch_report.html`
- **Configuration**: OpenAI API settings in `config.py`

### **API Integration**
```python
# OpenAI API Configuration
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
```

### **Routes**
- `POST /dashboard/<city_id>/generate-report` - Generate report
- `GET /dashboard/<city_id>/download-report` - Download as TXT

## Setup Requirements

### **Environment Variables**
```bash
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini  # Optional, defaults to gpt-4o-mini
```

### **Dependencies**
```bash
pip install openai==1.12.0
```

### **API Key Setup**
1. Get your OpenAI API key from [OpenAI Platform](https://platform.openai.com/)
2. Add it to your `.env` file
3. Ensure your account has access to the specified model

## Usage

### **Generating a Report**
1. Navigate to any city dashboard
2. Click the **"🤖 Generate Dispatch Report"** button
3. Wait for AI processing (typically 10-30 seconds)
4. Review the generated report

### **Downloading a Report**
1. After generating a report, click **"📥 Download as TXT"**
2. File will be named: `dispatch_report_[City]_[State]_[Country].txt`
3. Save to your local system for distribution

### **Report Distribution**
- **Health Authorities**: Share with local health departments
- **Stakeholders**: Distribute to government officials
- **Integration**: Import into other health information systems
- **Documentation**: Archive for compliance and reporting

## Customization

### **Prompt Engineering**
The AI prompt can be customized in `services/report_generator.py`:
- Adjust report structure
- Modify language style
- Add specific requirements
- Change output format

### **Model Selection**
Choose different OpenAI models based on needs:
- **gpt-4o-mini**: Fast, cost-effective (default)
- **gpt-4o**: Higher quality, more detailed
- **gpt-4-turbo**: Best quality, higher cost

### **Report Length**
Adjust `max_tokens` parameter for different report lengths:
- **500 tokens**: Brief summary
- **1000 tokens**: Standard report (default)
- **1500+ tokens**: Comprehensive analysis

## Security & Privacy

### **Data Handling**
- No epidemiological data is sent to OpenAI
- Only aggregated metrics and city information are processed
- Reports are generated locally and not stored on OpenAI servers

### **API Key Security**
- Store API keys in environment variables
- Never commit API keys to version control
- Use `.env` files for local development
- Use secure environment variables in production

## Cost Considerations

### **OpenAI Pricing** (as of 2024)
- **gpt-4o-mini**: ~$0.00015 per 1K tokens
- **gpt-4o**: ~$0.005 per 1K tokens
- **gpt-4-turbo**: ~$0.01 per 1K tokens

### **Typical Report Costs**
- **Standard Report**: ~$0.00015 per report (gpt-4o-mini)
- **gpt-4o**: ~$0.005 per report (gpt-4o)

## Troubleshooting

### **Common Issues**
1. **API Key Error**: Check your OpenAI API key configuration
2. **Model Access**: Ensure your OpenAI account has access to the specified model
3. **Rate Limits**: OpenAI has rate limits; implement retry logic if needed
4. **Token Limits**: Adjust `max_tokens` if reports are truncated

### **Error Handling**
The system includes comprehensive error handling:
- Invalid city IDs
- Missing epidemiological data
- OpenAI API failures
- Network connectivity issues

## Future Enhancements

### **Planned Features**
- **Multi-language Support**: Reports in different languages
- **Template Customization**: User-defined report templates
- **Batch Processing**: Generate reports for multiple cities
- **Scheduled Reports**: Automatic report generation
- **Integration APIs**: Direct integration with health systems

### **Advanced AI Features**
- **Trend Analysis**: Deeper pattern recognition
- **Predictive Insights**: Forward-looking recommendations
- **Comparative Analysis**: City-to-city comparisons
- **Custom Metrics**: User-defined indicators

## Support

For technical support or questions about the dispatch report functionality:
1. Check the main README.md for setup instructions
2. Verify your OpenAI API configuration
3. Review the error messages in the application logs
4. Ensure all dependencies are properly installed

---

*This feature transforms raw epidemiological data into actionable intelligence for public health decision-making.*
