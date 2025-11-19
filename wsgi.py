#!/usr/bin/env python3
"""
WSGI entry point for Santé Flask MVC Application
"""

import os
import sys

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from app import create_app, load_settings_to_config
from models import db

application = create_app()

with application.app_context():
    db.create_all()

load_settings_to_config(application)

if __name__ == "__main__":
    application.run(host="0.0.0.0", port=5000, debug=True)
