import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Security: Require SECRET_KEY in production, use dev default only for development
    SECRET_KEY = os.environ.get("SECRET_KEY")
    if not SECRET_KEY:
        import sys
        if 'pytest' not in sys.modules:  # Allow missing key during tests
            print("WARNING: Using development SECRET_KEY. Set SECRET_KEY environment variable for production!")
        SECRET_KEY = "dev-secret-change-me-not-for-production"

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "sqlite:///" + os.path.join(BASE_DIR, "sante.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")
    ALLOWED_EXTENSIONS = {"csv"}

    # OpenAI Configuration
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
    OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")

    # Mapbox Configuration (for Kepler.gl maps)
    # Get your token at: https://account.mapbox.com/access-tokens/
    MAPBOX_TOKEN = os.environ.get("MAPBOX_TOKEN", "pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw")
