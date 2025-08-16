#!/usr/bin/env python3
"""
Test script to verify the Flask application can be imported correctly
"""

import os
import sys

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

try:
    from app import create_app
    from models import db, User, City, Observation, Indicator
    from services.analytics import compute_indicators, compute_forecast
    from services.csv_loader import load_csv, get_city_series
    
    print("✅ All imports successful!")
    print("✅ Application structure is correct")
    
    # Test app creation
    app = create_app()
    print("✅ Flask app created successfully")
    
    # Test database models
    with app.app_context():
        print("✅ Database context working")
        print("✅ Models imported correctly")
        
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    sys.exit(1)

print("\n🎉 Application is ready to run!")
print("Use: python wsgi.py")
