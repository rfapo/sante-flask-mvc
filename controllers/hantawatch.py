"""Hantawatch subdomain blueprint.

Serves the static Hantawatch outbreak-intelligence site (built by Onicio
and added 2026-05-14) at https://hantawatch.santehealth.co/. The blueprint
binds to the subdomain via Flask's subdomain matching; assets are served
from the same directory.

The site is intentionally public (no login required). Auth-protected
routes elsewhere in the Flask app are unaffected.
"""
from __future__ import annotations

from pathlib import Path
from flask import Blueprint, send_from_directory, abort

# subdomain='hantawatch' makes this blueprint respond only to
# hantawatch.<SERVER_NAME>. SERVER_NAME is set in config.py.
hantawatch_bp = Blueprint(
    "hantawatch",
    __name__,
    subdomain="hantawatch",
)

# Resolve the static directory absolutely so it works from any CWD.
STATIC_DIR = Path(__file__).resolve().parent.parent / "static" / "hantawatch"


@hantawatch_bp.route("/", methods=["GET"])
@hantawatch_bp.route("/index.html", methods=["GET"])
def index():
    """Landing page."""
    return send_from_directory(str(STATIC_DIR), "index.html")


@hantawatch_bp.route("/<path:filename>", methods=["GET"])
def static_assets(filename: str):
    """Serve any other asset (HTML, CSS, JS, images) under static/hantawatch/.

    send_from_directory enforces directory traversal protection.
    """
    target = STATIC_DIR / filename
    if not target.exists() or not target.is_file():
        abort(404)
    return send_from_directory(str(STATIC_DIR), filename)
