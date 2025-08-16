from flask import Blueprint, render_template, abort
from flask_login import login_required
from models import db, City, Indicator
from services.csv_loader import get_city_series

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")

@dashboard_bp.route("/<int:city_id>")
@login_required
def view_city(city_id):
    city = City.query.get_or_404(city_id)
    labels, values, forecast = get_city_series(city_id)
    ind = Indicator.query.filter_by(city_id=city_id).order_by(Indicator.id.desc()).first()
    if not ind:
        abort(404)
    return render_template(
        "dashboard.html",
        city=city,
        labels=labels,
        values=values,
        forecast=forecast,
        ind=ind,
    )
