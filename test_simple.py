#!/usr/bin/env python3
"""
Simple test script to verify imports work correctly
"""

import os
import sys

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

print("Testing imports...")

try:
    print("✅ Importing config...")
    from config import Config
    print("✅ Config imported successfully")
    
    print("✅ Importing models...")
    from models import db, User, City, Observation, Indicator
    print("✅ Models imported successfully")
    
    print("✅ Importing services...")
    from services.analytics import compute_indicators, compute_forecast
    from services.csv_loader import load_csv, get_city_series
    print("✅ Services imported successfully")
    
    print("✅ Importing controllers...")
    from controllers.auth import auth_bp
    from controllers.cities import cities_bp
    from controllers.dashboard import dashboard_bp
    print("✅ Controllers imported successfully")
    
    print("\n🎉 All imports successful!")
    print("✅ Application structure is correct")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Python path: {sys.path[:3]}...")
    sys.exit(1)
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    sys.exit(1)

print("\n🚀 Ready to run the application!")
print("Use: python main.py")
