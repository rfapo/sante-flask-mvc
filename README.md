# Santé – Intelligent Epidemiological Surveillance System

## 🎯 What is Santé?

**Santé** is an intelligent epidemiological surveillance system designed to monitor, analyze, and predict disease outbreaks in real-time. Built as a comprehensive web application using Flask MVC architecture, it provides public health officials, epidemiologists, and healthcare administrators with powerful tools for data-driven decision making.

### 🌍 The Challenge
In today's interconnected world, rapid response to disease outbreaks is crucial. Traditional surveillance methods often involve manual data collection, delayed analysis, and limited predictive capabilities. Public health officials need:
- **Real-time monitoring** of disease cases across multiple cities
- **Predictive analytics** to anticipate outbreak trends
- **Geospatial visualization** to identify risk hotspots
- **Executive reporting** for stakeholders and decision makers
- **Data integration** from multiple sources

### 💡 Our Solution
Santé addresses these challenges through an integrated platform that combines:
- **Automated Data Processing**: CSV upload and validation for epidemiological data
- **Intelligent Analytics**: AI-powered calculation of key epidemiological indicators (R(t), R0, hospitalization rates)
- **Predictive Modeling**: Machine learning-based forecasting of disease trends
- **Interactive Dashboards**: Real-time visualization of data with actionable insights
- **Geospatial Intelligence**: Interactive maps with risk assessment and heat mapping
- **AI-Generated Reports**: Professional executive summaries using OpenAI's GPT models
- **Multi-City Support**: Comparative analysis across different geographical regions

## 🏗️ Architecture Overview

This project is an MVP built with Flask following the MVC pattern:
- **Authentication** with Flask-Login (user: `admin`, password: `admin`)
- **Data Management**: Create/update city data via CSV upload
- **Dashboard**: Historical data visualization + predictive forecasting
- **Interactive Risk Maps**: OpenStreetMap integration with heatmap visualization
- **AI Integration**: OpenAI-powered executive report generation
- **Modern UI**: Fully responsive interface built with Tailwind CSS

## 🚀 How to Run

```bash
# 1. Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment variables (optional)
cp env_example .env
# Edit .env file if needed

# 4. Initialize database
export FLASK_APP=main.py  # On Windows: set FLASK_APP=main.py
flask init-db

# 5. Run application
python main.py
# or
flask run
```

The application will be available at http://localhost:5000

## 📁 Project Structure

```
sante_flask_mvc/
├── main.py              # Main application entry point
├── app.py               # Flask application configuration (legacy)
├── wsgi.py              # Alternative WSGI entry point
├── run.py               # Alternative entry point
├── config.py            # Application configuration
├── models.py            # Data models (SQLAlchemy)
├── controllers/         # Controllers (Blueprints)
│   ├── auth.py         # Authentication
│   ├── cities.py       # City management
│   └── dashboard.py    # Monitoring dashboard
├── services/            # Business logic services
│   ├── analytics.py    # Indicator calculations
│   └── csv_loader.py   # CSV processing
├── templates/           # HTML templates
├── static/              # Static files
├── env_example          # Environment configuration example
└── requirements.txt     # Python dependencies
```

## 📊 Expected CSV Format
Required columns: `city,state,country,week_label,cases`

### Available Sample Files:
- **`sample_data.csv`** - Recife, Brazil (original sample data)
- **`new_york_data.csv`** - New York, USA (sample data)
- **`freetown_data.csv`** - Freetown, Sierra Leone (sample data)

See the "Sample CSV Files" section on the upload page to download examples.

## 🔧 Core Features

### 📈 Epidemiological Intelligence
- **Real-time Monitoring**: Track disease cases across multiple cities
- **Predictive Analytics**: AI-powered forecasting of outbreak trends
- **Risk Assessment**: Dynamic calculation of transmission rates and risk levels
- **Multi-indicator Analysis**: R(t), R0, hospitalization rates, and trend analysis

### 🗺️ Geospatial Intelligence
- **Interactive Risk Maps**: OpenStreetMap integration with dynamic heatmaps
- **Risk Zone Visualization**: Color-coded risk assessment based on epidemiological indicators
- **Geographic Comparison**: Analyze disease patterns across different regions
- **Spatial Analytics**: Identify outbreak hotspots and transmission patterns

### 🤖 AI-Powered Insights
- **Executive Reports**: Automated generation of professional health reports
- **Intelligent Analysis**: AI-driven interpretation of epidemiological data
- **Stakeholder Communication**: Professional reports for health authorities
- **Predictive Insights**: Machine learning-based trend analysis

### 📱 Modern User Experience
- **Responsive Design**: Mobile-first interface built with Tailwind CSS
- **Real-time Updates**: Live dashboard with current data
- **Interactive Visualizations**: Charts, graphs, and maps for data exploration
- **Professional Interface**: Clean, intuitive design for healthcare professionals

## 🆕 Recently Implemented Features

### 🗺️ Interactive Risk Mapping
- **OpenStreetMap Integration**: High-quality, free base maps
- **Dynamic Heatmaps**: Risk visualization based on R(t) with color-coded intensity
- **Risk Zones**: Multiple areas with different risk intensity levels
- **Informative Popups**: Click markers to see detailed city information
- **Visual Legend**: Color-coded risk levels (High/Medium/Low)

### 🌐 English Interface
- **Professional Design**: Modern, responsive login interface
- **Intuitive Upload**: User-friendly CSV upload interface
- **Comprehensive Dashboard**: All elements translated to English
- **Navigation**: Menu and navigation in English
- **User Feedback**: Flash messages and notifications in English

### 🤖 AI Executive Reports
- **Automated Generation**: AI-powered executive summaries
- **Intelligent Analysis**: Executive summary of epidemiological data
- **Export Functionality**: Download in TXT format for distribution
- **Integration Ready**: Prepared for integration with other health systems
- **Professional Quality**: Reports suitable for health authorities

## ✅ Issues Resolved

- ✅ **Import Errors**: Fixed relative imports to absolute imports
- ✅ **MVC Structure**: Adjusted to work correctly
- ✅ **Dashboard**: Updated to follow exact visual pattern from conceptual file
- ✅ **Execution**: Multiple entry points created (main.py, wsgi.py, run.py)
- ✅ **Imports**: All imports now absolute and working correctly
- ✅ **Mapping**: Implemented real map with OpenStreetMap and heatmap
- ✅ **Translation**: Interface completely in English

## 📋 Use Cases

### 🏥 Public Health Officials
- Monitor disease outbreaks across multiple cities
- Generate executive reports for stakeholders
- Analyze transmission patterns and risk factors
- Make data-driven decisions for public health interventions

### 🔬 Epidemiologists
- Track disease progression over time
- Analyze transmission rates and reproduction numbers
- Identify outbreak hotspots and risk zones
- Generate professional reports for publication

### 🏛️ Government Agencies
- Real-time surveillance of public health threats
- Evidence-based policy making
- Resource allocation based on risk assessment
- Communication with international health organizations

### 🏢 Healthcare Organizations
- Monitor local disease patterns
- Prepare for potential outbreaks
- Coordinate with public health authorities
- Track resource utilization and capacity planning

## 🚀 Technology Stack

### Backend
- **Framework**: Flask 3.0.3 - Lightweight, flexible Python web framework
- **Database**: SQLAlchemy 2.0.23 - Modern Python ORM with type safety
- **Authentication**: Flask-Login 0.6.3 - Secure user session management
- **Data Processing**: Pandas 2.2.2 - Powerful data manipulation and analysis

### Frontend
- **CSS Framework**: Tailwind CSS - Utility-first CSS framework for rapid UI development
- **Charts**: Chart.js - Interactive JavaScript charts and graphs
- **Maps**: Leaflet.js + OpenStreetMap - Free, high-quality mapping solution
- **Advanced Visualization**: Kepler.gl - Uber's geospatial analysis platform

### AI & Intelligence
- **Language Models**: OpenAI GPT-4o-mini - Advanced AI for report generation
- **Predictive Analytics**: Custom algorithms for epidemiological forecasting
- **Risk Assessment**: Dynamic calculation of transmission rates and risk levels

### Infrastructure
- **Development**: Flask development server with hot reload
- **Production Ready**: WSGI-compatible for production deployment
- **Database**: SQLite for development, PostgreSQL ready for production
- **Environment**: Flexible configuration via environment variables

## 🔮 Future Roadmap

### Phase 2: Advanced Analytics
- **Machine Learning Models**: Enhanced predictive algorithms
- **Real-time Data Feeds**: Integration with health APIs
- **Advanced Geospatial**: 3D visualization and spatial analysis
- **Mobile Applications**: Native mobile apps for field workers

### Phase 3: Enterprise Features
- **Multi-tenant Architecture**: Support for multiple organizations
- **Advanced Security**: Role-based access control and audit logging
- **API Integration**: RESTful APIs for third-party integrations
- **Scalability**: Microservices architecture and load balancing

### Phase 4: Global Scale
- **International Support**: Multi-language and multi-currency
- **Global Data Sources**: Integration with WHO and CDC data
- **Collaborative Features**: Cross-organization data sharing
- **Advanced Reporting**: Custom report builders and dashboards

## 📚 Documentation

- **Complete Documentation**: See `DOCUMENTACAO_COMPLETA.md` for comprehensive technical details
- **OpenAI Setup**: See `OPENAI_SETUP.md` for AI integration configuration
- **Map Features**: See `MAP_FEATURES.md` for geospatial functionality details
- **Demo Guide**: See `DEMO_GUIDE.md` for demonstration instructions
- **Dispatch Reports**: See `DISPATCH_REPORT_FEATURES.md` for AI report generation

## 🤝 Contributing

This project is designed as an MVP for demonstration and educational purposes. Contributions are welcome for:
- Bug fixes and improvements
- New features and enhancements
- Documentation improvements
- Testing and quality assurance

## 📄 License

This project is provided as-is for educational and demonstration purposes. The data used is fictional and for demonstration only.

## 🆘 Support

For technical issues:
1. Use `python main.py` directly
2. Verify all dependencies are installed: `pip install -r requirements.txt`
3. Ensure virtual environment is activated
4. Check logs for detailed error information

## 🔑 Default Access

- **Username**: `admin`
- **Password**: `admin`

---

*Santé - Transforming Public Health Surveillance Through Intelligent Technology*
