"""Santé full interactive simulator — single-file React prototype served from a
fixed location, behind login_required. Lives outside the Flask app tree so it
can be updated independently.
"""
from __future__ import annotations

import os
from pathlib import Path
from flask import Blueprint, send_from_directory, abort
from flask_login import login_required

simulator_bp = Blueprint("simulator", __name__, url_prefix="/simulator")

# Resolve the simulator file. Production: /var/www/sante-simulator/.
DEFAULT_DIRS = [
    os.environ.get("SIMULATOR_DIR"),
    "/var/www/sante-simulator",
    str(Path(__file__).resolve().parent.parent.parent / "sante-scheme" / "docs" / "prototypes"),
]
STATIC_DIR = next((d for d in DEFAULT_DIRS if d and Path(d).is_dir()), "/var/www/sante-simulator")
INDEX_FILE = "sante-prototype.html"


@simulator_bp.route("/", methods=["GET"])
@login_required
def index():
    return send_from_directory(STATIC_DIR, INDEX_FILE)


@simulator_bp.route("/<path:filename>", methods=["GET"])
@login_required
def assets(filename: str):
    target = Path(STATIC_DIR) / filename
    if not target.exists() or not target.is_file():
        abort(404)
    return send_from_directory(STATIC_DIR, filename)
