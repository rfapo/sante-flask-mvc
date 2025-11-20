# 📚 Complete Documentation - Santé Flask MVC

## 🎯 Project Overview

**Santé** is an intelligent epidemiological surveillance system designed to monitor, analyze, and predict disease outbreaks in real-time. Built as a comprehensive web application using Flask MVC architecture, it provides public health officials, epidemiologists, and healthcare administrators with powerful tools for data-driven decision making.

### 🎯 Main Objectives
- **Epidemiological Surveillance**: Monitor disease cases across different cities
- **Predictive Analytics**: Calculate epidemiological indicators (R(t), R0, hospitalization rates)
- **Geospatial Visualization**: Interactive maps with risk assessment and heat mapping
- **Executive Reporting**: AI-generated reports for health authorities
- **Intelligent Dashboard**: Modern interface for epidemiological data analysis

---

## 🏗️ System Architecture

### 📐 Architectural Pattern
The project follows the **MVC (Model-View-Controller)** pattern with clear separation of responsibilities:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     VIEWS       │    │   CONTROLLERS   │    │     MODELS      │
│  (Templates)    │◄──►│  (Blueprints)   │◄──►│  (SQLAlchemy)   │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   STATIC FILES  │    │    SERVICES     │    │   DATABASE      │
│  (CSS, JS, IMG) │    │  (Business Logic)│   │   (SQLite)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 🔄 Data Flow
1. **CSV Upload** → **Parser** → **Database** → **Analytics** → **Dashboard**
2. **User Input** → **Controller** → **Service** → **Model** → **Response**
3. **Data Request** → **API** → **AI Service** → **Report Generation**

---

## 🛠️ Technology Stack

### 🐍 Backend
- **Framework**: Flask 3.0.3
- **ORM**: SQLAlchemy 2.0.23 + Flask-SQLAlchemy 3.1.1
- **Authentication**: Flask-Login 0.6.3
- **Security**: Werkzeug 0.3.0
- **Data Processing**: Pandas 2.2.2
- **AI Integration**: OpenAI API (GPT-4o-mini)
- **Configuration**: python-dotenv 1.0.0

### 🌐 Frontend
- **CSS Framework**: Tailwind CSS (via CDN)
- **Charts**: Chart.js
- **Maps**: Leaflet.js + OpenStreetMap
- **Advanced Visualization**: Kepler.gl
- **Fonts**: Google Fonts (Inter)
- **Responsiveness**: Mobile-first design

### 🗄️ Database
- **DBMS**: SQLite (development)
- **Configuration**: PostgreSQL support via environment variables
- **Migrations**: Flask CLI commands for initialization

### 🚀 Infrastructure
- **Server**: Flask Development Server
- **Port**: 5000 (configurable)
- **Host**: 0.0.0.0 (configurable)
- **Environment**: Development and production support

---

## 📁 Module Structure

### 🎮 Controllers (Controllers)
Location: `controllers/`

#### 🔐 Auth Controller (`auth.py`)
- **Responsibility**: User authentication management
- **Features**:
  - User login
  - User logout
  - Credential validation
- **Routes**:
  - `POST /login` - Authentication
  - `GET /logout` - Session termination

#### 🏙️ Cities Controller (`cities.py`)
- **Responsibility**: City and epidemiological data management
- **Features**:
  - City listing
  - CSV file upload
  - Data validation
- **Routes**:
  - `GET /cities/` - City list
  - `GET/POST /cities/upload` - CSV upload

#### 📊 Dashboard Controller (`dashboard.py`)
- **Responsibility**: Data visualization and analysis
- **Features**:
  - Main city dashboard
  - Executive report generation
  - Kepler.gl visualization
  - Interactive risk mapping
- **Routes**:
  - `GET /dashboard/<city_id>` - City dashboard
  - `POST /dashboard/<city_id>/generate-report` - Report generation
  - `GET /dashboard/<city_id>/kepler` - Kepler.gl visualization

### 🔧 Services (Services)
Location: `services/`

#### 📈 Analytics Service (`analytics.py`)
- **Responsibility**: Epidemiological calculations
- **Features**:
  - R(t) calculation - Transmission rate
  - R0 calculation - Basic reproduction number
  - Hospitalization rate estimation
  - Simple trend-based forecasting

#### 📁 CSV Loader Service (`csv_loader.py`)
- **Responsibility**: CSV file processing
- **Features**:
  - Required column validation
  - Epidemiological data parsing
  - Database persistence
  - Format error handling

#### 🤖 Report Generator Service (`report_generator.py`)
- **Responsibility**: AI-powered report generation
- **Features**:
  - OpenAI API integration
  - Executive report generation
  - Intelligent data analysis
  - Professional formatting for health authorities

### 🗃️ Models (Models)
Location: `models.py`

#### 👤 User Model
- **Fields**:
  - `id`: Unique identifier
  - `username`: Username
  - `password_hash`: Password hash
  - `created_at`: Creation date
- **Relationships**: None

#### 🏙️ City Model
- **Fields**:
  - `id`: Unique identifier
  - `name`: City name
  - `state`: State/Province
  - `country`: Country
  - `created_at`: Creation date
- **Relationships**:
  - `observations`: List of epidemiological observations
  - `indicators`: List of calculated indicators

#### 📊 Observation Model
- **Fields**:
  - `id`: Unique identifier
  - `city_id`: City reference
  - `week_label`: Week label (e.g., "Wk 40")
  - `cases`: Number of cases
- **Relationships**:
  - `city`: Associated city

#### 📈 Indicator Model
- **Fields**:
  - `id`: Unique identifier
  - `city_id`: City reference
  - `rt`: Transmission rate (R(t))
  - `r0`: Basic reproduction number
  - `hospitalization_rate`: Hospitalization rate (%)
  - `computed_at`: Calculation date
- **Relationships**:
  - `city`: Associated city

---

## 🎨 Templates and Interface

### 🎭 Template System
- **Engine**: Jinja2 (Flask standard)
- **Base Template**: `base.html` with responsive layout
- **Style**: Design system based on Tailwind CSS

### 📱 Main Pages

#### 🔐 Login (`login.html`)
- Authentication form
- Credential validation
- Error/success messages

#### 🏠 Home (`index.html`)
- Home page after login
- System summary
- Main navigation

#### 📤 Upload (`upload.html`)
- CSV upload interface
- File validation
- Visual feedback

#### 🏙️ City List (`city_list.html`)
- Registered cities table
- Summary indicators
- Dashboard links

#### 📊 Dashboard (`dashboard.html`)
- Historical case charts
- Epidemiological indicators
- Interactive risk map
- Advanced feature buttons

#### 🗺️ Kepler Visualization (`kepler_view.html`)
- Kepler.gl interface
- Advanced geospatial analysis
- Spatial data analysis

#### 📋 Executive Report (`dispatch_report.html`)
- AI-generated report
- Professional formatting
- Export options

---

## 🔌 Configuration and Environment Variables

### ⚙️ Configuration File (`config.py`)
```python
class Config:
    SECRET_KEY = "dev-secret-change-me"
    SQLALCHEMY_DATABASE_URI = "sqlite:///sante.db"
    UPLOAD_FOLDER = "static/uploads"
    ALLOWED_EXTENSIONS = {"csv"}
    OPENAI_API_KEY = None
    OPENAI_MODEL = "gpt-4o-mini"
```

### 🌍 Environment Variables (`env_example`)
```bash
FLASK_APP=main.py
FLASK_ENV=development
SECRET_KEY=dev-secret-change-me-in-production
DATABASE_URL=sqlite:///sante.db
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini
```

---

## 🚀 Application Entry Points

### 🎯 Main File (`main.py`)
- **Function**: Main application entry point
- **Configuration**: Flask application creation
- **Initialization**: Database and admin user
- **Execution**: Development server

### 🌐 WSGI (`wsgi.py`)
- **Function**: Production entry point
- **Configuration**: WSGI server compatible
- **Usage**: Production deployment

### ▶️ Runner (`run.py`)
- **Function**: Alternative entry point
- **Configuration**: Simplified configuration
- **Usage**: Development and testing

---

## 🔐 Authentication System

### 👤 Default User
- **Username**: `admin`
- **Password**: `admin`
- **Type**: Administrator user

### 🔒 Security Features
- **Password Hashing**: Werkzeug security
- **Sessions**: Flask-Login
- **Route Protection**: `@login_required`
- **Automatic Logout**: Session management

---

## 📊 Analysis Features

### 🧮 Epidemiological Indicators

#### R(t) - Transmission Rate
- **Calculation**: `(current_cases / previous_cases)`
- **Interpretation**:
  - R(t) > 1: Epidemic growing
  - R(t) = 1: Epidemic stable
  - R(t) < 1: Epidemic declining

#### R0 - Basic Reproduction Number
- **Default Value**: 1.3 (configurable)
- **Meaning**: Average number of secondary infections

#### Hospitalization Rate
- **Calculation**: 3% + intensity factor
- **Base**: Case trend

### 📈 Forecasting
- **Method**: Simple decay (10% per week)
- **Period**: 3 future weeks
- **Base**: Last observed value

---

## 🗺️ Mapping Features

### 🗺️ Interactive Risk Mapping
- **Technology**: OpenStreetMap + Leaflet.js
- **Features**:
  - R(t)-based risk heatmap
  - City markers
  - Informative popups
  - Visual legend

### 🌍 Kepler.gl Visualization
- **Technology**: Kepler.gl (Uber)
- **Features**:
  - Advanced geospatial analysis
  - Multiple data layers
  - Temporal and spatial filters
  - Visualization export

---

## 🤖 AI Integration

### 🧠 OpenAI Integration
- **Model**: GPT-4o-mini
- **Features**:
  - Executive report generation
  - Intelligent epidemiological analysis
  - Health authority recommendations
  - Professional formatting

### 📋 Executive Reports
- **Content**:
  - Executive summary
  - Key findings
  - Risk assessment
  - Recommendations
  - Next steps

---

## 📁 CSV File Structure

### 📋 Expected Format
```csv
city,state,country,week_label,cases
Recife,PE,Brazil,Wk 40,350
Recife,PE,Brazil,Wk 42,420
```

### 🔍 Validation
- **Required Columns**: `city`, `state`, `country`, `week_label`, `cases`
- **Date Format**: Weeks in "Wk XX" format
- **Data Types**: Cases as integers

### 📊 Sample Files
- **`sample_data.csv`**: Recife, Brazil
- **`new_york_data.csv`**: New York, USA
- **`freetown_data.csv`**: Freetown, Sierra Leone

---

## 🛠️ CLI Commands

### 🗄️ Database Initialization
```bash
flask init-db
```
**Features**:
- Table creation
- Default admin user
- Upload folder

### 🚀 Application Execution
```bash
# Option 1
python main.py

# Option 2
flask run

# Option 3
python wsgi.py

# Option 4
python run.py
```

---

## 🔧 Dependencies and Libraries

### 📦 Python Dependencies (`requirements.txt`)
```
Flask==3.0.3              # Web framework
Flask-Login==0.6.3         # User authentication
Flask-SQLAlchemy==3.1.1    # Flask ORM
Werkzeug==3.0.3            # WSGI utilities
pandas==2.2.2              # Data manipulation
SQLAlchemy==2.0.23         # Base ORM
python-dotenv==1.0.0       # Environment variables
openai>=1.50.0             # OpenAI API
```

### 🌐 Frontend Dependencies (CDN)
- **Tailwind CSS**: Utility-first CSS framework
- **Chart.js**: Chart library
- **Leaflet.js**: Mapping library
- **Google Fonts**: Inter typography

---

## 🚀 Deployment and Production

### 🐳 Docker Support
- **Kepler.gl**: Docker container for advanced visualizations
- **Configuration**: Dockerfile for Jupyter environment
- **Port**: 8888 (Jupyter Notebook)

### 🌍 Production Configuration
- **WSGI Server**: Gunicorn, uWSGI
- **Database**: PostgreSQL, MySQL
- **Environment Variables**: Secure configuration
- **Secret Key**: Unique secret key

---

## 📊 Metrics and Monitoring

### 📈 Performance Indicators
- **Response Time**: CSV upload and processing
- **Memory Usage**: Data processing
- **Reliability**: Upload success rate

### 🔍 Logs and Debugging
- **Flask Logs**: Standard application logs
- **Error Handling**: Structured error handling
- **Debug Mode**: Development mode

---

## 🔮 Roadmap and Future Improvements

### 🚀 Planned Features
- **REST API**: External integration endpoints
- **Caching**: Redis for performance
- **Testing**: Automated test suite
- **CI/CD**: Continuous integration pipeline
- **Monitoring**: Real-time metrics

### 🔧 Technical Improvements
- **Microservices**: Distributed architecture
- **Caching**: Query optimization
- **Security**: JWT authentication, rate limiting
- **Scalability**: Load balancing, clustering

---

## 📚 Resources and Documentation

### 🔗 Useful Links
- **Flask**: https://flask.palletsprojects.com/
- **SQLAlchemy**: https://www.sqlalchemy.org/
- **Tailwind CSS**: https://tailwindcss.com/
- **Kepler.gl**: https://kepler.gl/
- **OpenAI API**: https://openai.com/api/

### 📖 Additional Documentation
- **README.md**: Installation and usage guide
- **Templates**: Usage examples
- **CSV Files**: Sample data
- **Configuration**: Environment variables

---

## 🤝 Contribution and Development

### 🛠️ Development Setup
1. **Repository clone**
2. **Virtual environment creation**
3. **Dependency installation**
4. **Environment configuration**
5. **Database initialization**

### 📝 Code Standards
- **PEP 8**: Python style
- **Type Hints**: Type annotations
- **Docstrings**: Function documentation
- **Error Handling**: Exception handling

---

## 📄 License and Terms

### 📜 Legal Information
- **Project**: MVP for demonstration
- **Usage**: Educational and development
- **Data**: Fictional examples
- **API Keys**: Required configuration for AI features

---

## 📞 Support and Contact

### 🆘 Troubleshooting
- **Logs**: Check application logs
- **Dependencies**: Correct package installation
- **Configuration**: Environment variables
- **Database**: Initialization and permissions

### 📧 Communication
- **Issues**: GitHub Issues for bugs
- **Documentation**: README and code comments
- **Examples**: Sample CSV files

---

*Documentation automatically generated based on complete repository analysis of Santé Flask MVC*
