import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required
from werkzeug.utils import secure_filename
from models import db, City, Indicator
from services.csv_loader import load_csv

cities_bp = Blueprint("cities", __name__, url_prefix="/cities")

def _allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in {"csv"}

@cities_bp.route("/")
@login_required
def list_cities():
    cities = City.query.order_by(City.created_at.desc()).all()
    ind_map = {i.city_id: i for i in Indicator.query.all()}
    return render_template("city_list.html", cities=cities, ind_map=ind_map)

@cities_bp.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    if request.method == "POST":
        file = request.files.get("file")
        if not file or file.filename == "":
            flash("Please choose a CSV file.", "warning")
            return redirect(request.url)
        if not _allowed_file(file.filename):
            flash("Invalid file type. Please upload a CSV.", "danger")
            return redirect(request.url)
        filename = secure_filename(file.filename)
        upload_path = os.path.join(current_app.config["UPLOAD_FOLDER"])
        os.makedirs(upload_path, exist_ok=True)
        # Save a copy (optional)
        file.seek(0)
        file.save(os.path.join(upload_path, filename))
        file.stream.seek(0)  # rewind for parsing
        try:
            city = load_csv(file.stream)
        except Exception as e:
            current_app.logger.exception("CSV parsing failed")
            flash(f"Error processing CSV: {e}", "danger")
            return redirect(request.url)
        flash(f"City '{city.name}' processed and dashboard created.", "success")
        return redirect(url_for("dashboard.view_city", city_id=city.id))
    return render_template("upload.html")
