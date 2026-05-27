"""Worldcup 2026 demo prototype — served as a Flask blueprint behind login_required.

The static files live outside the Flask app tree (deployed to
/var/www/worldcup-2026/ on the EC2 host) so they can be updated independently
without redeploying Flask. Set WORLDCUP_2026_DIR env var to override the default
location; in development it falls back to a sibling dir.
"""
from __future__ import annotations

import os
from pathlib import Path
from flask import Blueprint, send_from_directory, abort
from flask_login import login_required

worldcup_bp = Blueprint("worldcup", __name__, url_prefix="/worldcup-2026")

# Resolve the static directory. Production: /var/www/worldcup-2026 (deployed).
# Dev: prototype sources at ../sante-scheme/docs/prototypes/worldcup-2026 relative to repo.
DEFAULT_DIRS = [
    os.environ.get("WORLDCUP_2026_DIR"),
    "/var/www/worldcup-2026",
    str(Path(__file__).resolve().parent.parent.parent / "sante-scheme" / "docs" / "prototypes" / "worldcup-2026"),
]
STATIC_DIR = next((d for d in DEFAULT_DIRS if d and Path(d).is_dir()), "/var/www/worldcup-2026")


@worldcup_bp.route("/", methods=["GET"])
@worldcup_bp.route("/index.html", methods=["GET"])
@login_required
def index():
    return send_from_directory(STATIC_DIR, "index.html")


@worldcup_bp.route("/<path:filename>", methods=["GET"])
@login_required
def assets(filename: str):
    """Serve any other file (HTML, CSS, JS, images) under the deploy dir.

    send_from_directory enforces directory-traversal protection.
    """
    target = Path(STATIC_DIR) / filename
    if not target.exists() or not target.is_file():
        abort(404)
    return send_from_directory(STATIC_DIR, filename)
