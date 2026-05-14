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
    # NOTE: hard-coded fallback removed 2026-05-14 because GitHub push-protection
    # flags any pk.* token. Set MAPBOX_TOKEN env var (or put it in .env / .env.example)
    # for the Kepler maps to render. Without the token, maps still work but with
    # the default light tiles only.
    MAPBOX_TOKEN = os.environ.get("MAPBOX_TOKEN", "")

    # Subdomain matching — required for the hantawatch blueprint.
    # Production: SERVER_NAME=santehealth.co (blueprint registers + responds to hantawatch.santehealth.co).
    # Dev: leave SERVER_NAME unset (blueprint is skipped in app.py so `flask run` works on http://localhost:5000 as before).
    SERVER_NAME = os.environ.get("SERVER_NAME")
    SUBDOMAIN_MATCHING = bool(SERVER_NAME)
