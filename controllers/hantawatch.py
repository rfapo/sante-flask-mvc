"""Hantawatch subdomain blueprint — KEPT AS A FALLBACK PATH.

Status (2026-05-14): the production deployment serves
https://hantawatch.santehealth.co/ via **nginx static** directly
(no Flask involvement) — see /etc/nginx/sites-available/sante. The Flask
blueprint here is dead code in production: app.py only registers it when
SERVER_NAME is set in config, and SERVER_NAME is intentionally UNSET on
the EC2 instance (.env doesn't define it).

Why the pivot from Flask blueprint to nginx-static:
- Setting SERVER_NAME + SUBDOMAIN_MATCHING in Flask caused demo.santehealth.co
  to 404 because Flask started rejecting that subdomain as unmatched.
- The hantawatch project is pure static (HTML/CSS/JS) — nginx serves it
  more cleanly and with better caching than going through gunicorn.
- Keeping this blueprint as code lets a future contributor add a dynamic
  endpoint (e.g., a /api/hantavirus-feed JSON proxy) without re-wiring
  the architecture: set SERVER_NAME=santehealth.co + add a corresponding
  nginx `location /api/` block that proxies back to the Flask socket.

If anyone reactivates this path, also update the nginx config to remove
the static `root` directive for hantawatch.santehealth.co (or keep both
and route by location prefix).
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
