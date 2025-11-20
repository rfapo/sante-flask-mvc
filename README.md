# Santé – Intelligent Epidemiological Surveillance System

> ⚠️ **SECURITY WARNING**: This application includes default development credentials (`admin`/`admin`).
> **NEVER use these credentials in production**. See the [Security](#-security) section below for proper setup.

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
- **Authentication** with Flask-Login and role-based access control
  - ⚠️ Default dev credentials: user: `admin`, password: `admin` (**DEVELOPMENT ONLY**)
  - Admin panel at `/admin` for user management and settings
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

# 3. Configure environment variables
cp .env.example .env
# Edit .env file with your configuration:
# - Set a strong SECRET_KEY (generate with: openssl rand -hex 32)
# - Add your OPENAI_API_KEY for AI report generation
# - Add your MAPBOX_TOKEN for Kepler.gl maps (optional)

# 4. Initialize database and create admin user
export FLASK_APP=app.py  # On Windows: set FLASK_APP=app.py
flask init-db
flask create-root  # Follow prompts to create your admin account

# 5. Run application
python app.py
# or
python wsgi.py
# or
flask run
```

The application will be available at http://localhost:5000

## 📁 Project Structure

```
sante_flask_mvc/
├── app.py                # Flask application factory and CLI commands
├── wsgi.py              # WSGI entry point for production deployment
├── config.py            # Application configuration
├── models.py            # Data models (SQLAlchemy)
├── controllers/         # Controllers (Blueprints)
│   ├── auth.py         # Authentication
│   ├── cities.py       # City management
│   ├── dashboard.py    # Monitoring dashboard
│   └── admin.py        # Admin panel
├── services/            # Business logic services
│   ├── analytics.py    # Indicator calculations
│   └── csv_loader.py   # CSV processing
├── templates/           # HTML templates (Jinja2)
├── static/              # Static files (CSS, JS, images)
├── data/                # Data directory
│   └── samples/        # Sample CSV files for testing
├── docs/                # Documentation
│   ├── COMPLETE_DOCUMENTATION.md
│   ├── DEMO_GUIDE.md
│   ├── DISPATCH_REPORT_FEATURES.md
│   ├── MAP_FEATURES.md
│   ├── OPENAI_SETUP.md
│   └── SECURITY.md
├── tests/               # Test suite
├── .env.example         # Environment configuration template
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

## 📊 Expected CSV Format
Required columns: `city,state,country,week_label,cases`

### Available Sample Files:
Sample files are located in `data/samples/`:
- **`sample_data.csv`** - Recife, Brazil (original sample data)
- **`new_york_data.csv`** - New York, USA (sample data)
- **`freetown_data.csv`** - Freetown, Sierra Leone (sample data)

You can also download examples from the "Sample CSV Files" section on the upload page.

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
- ✅ **Admin Panel**: Full user management and settings configuration at `/admin`
- ✅ **Security**: Hardcoded credentials removed, environment variable configuration
- ✅ **Project Organization**: Docs moved to `docs/`, sample data to `data/samples/`
- ✅ **Imports**: All imports now absolute and working correctly
- ✅ **Mapping**: Implemented real map with OpenStreetMap and heatmap
- ✅ **Kepler.gl Integration**: Advanced geospatial visualization
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

All documentation is located in the `docs/` directory:

- **[Complete Documentation](docs/COMPLETE_DOCUMENTATION.md)** - Comprehensive technical details
- **[Security Guidelines](docs/SECURITY.md)** - Security best practices and configuration
- **[OpenAI Setup](docs/OPENAI_SETUP.md)** - AI integration configuration
- **[Map Features](docs/MAP_FEATURES.md)** - Geospatial functionality details
- **[Demo Guide](docs/DEMO_GUIDE.md)** - Demonstration instructions
- **[Dispatch Reports](docs/DISPATCH_REPORT_FEATURES.md)** - AI report generation

## 🤝 Contributing

This project is designed as an MVP for demonstration and educational purposes. Contributions are welcome for:
- Bug fixes and improvements
- New features and enhancements
- Documentation improvements
- Testing and quality assurance

## 📄 License

This project is provided as-is for educational and demonstration purposes. The data used is fictional and for demonstration only.

## 🔒 Security

**IMPORTANT**: Please read the [Security Guidelines](docs/SECURITY.md) before deploying to production.

### Quick Security Checklist

- ✅ Change default admin credentials immediately
- ✅ Set a strong `SECRET_KEY` in environment variables (use `openssl rand -hex 32`)
- ✅ Never commit `.env` files or database files to version control
- ✅ Use HTTPS in production (SSL/TLS certificates)
- ✅ Keep dependencies updated (`pip list --outdated`)
- ✅ Review firewall rules and access controls
- ✅ Set up regular database backups

### Environment Variables

Required for production:
- `SECRET_KEY` - Strong random key for session encryption
- `ROOT_ADMIN_EMAIL` - Your admin email address
- `OPENAI_API_KEY` - For AI report generation (optional but recommended)
- `MAPBOX_TOKEN` - For Kepler.gl maps (optional)

See `.env.example` for complete configuration template.

## 🆘 Support

For technical issues:
1. Use `python app.py` or `python wsgi.py` to run the application
2. Verify all dependencies are installed: `pip install -r requirements.txt`
3. Ensure virtual environment is activated
4. Check environment variables are configured correctly
5. Check logs for detailed error information
6. Review [Security Guidelines](docs/SECURITY.md) for security-related issues

## 🔑 Development Access

⚠️ **DEVELOPMENT ONLY - NOT FOR PRODUCTION**

Default test credentials (if not using `flask create-root`):
- **Username**: `admin`
- **Password**: `admin`

**For production**: Always create a secure admin account using:
```bash
flask create-root
```
This will prompt you to create an admin account with your email and a strong password.

---

*Santé - Transforming Public Health Surveillance Through Intelligent Technology*
