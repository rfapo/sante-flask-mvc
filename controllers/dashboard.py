from flask import Blueprint, render_template, abort, request, jsonify, flash, redirect, url_for, current_app
from flask_login import login_required
from models import db, City, Indicator
from services.csv_loader import get_city_series
from services.report_generator import ReportGenerator

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

@dashboard_bp.route("/<int:city_id>/generate-report", methods=["POST"])
@login_required
def generate_report(city_id):
    """Generate dispatch report using OpenAI"""
    try:
        # Check if OpenAI API key is configured
        if not current_app.config.get('OPENAI_API_KEY'):
            flash("OpenAI API key not configured. Please contact your administrator.", "danger")
            return redirect(url_for("dashboard.view_city", city_id=city_id))
        
        generator = ReportGenerator()
        report, error = generator.generate_dispatch_report(city_id)
        
        if error:
            flash(f"Error generating report: {error}", "danger")
            return redirect(url_for("dashboard.view_city", city_id=city_id))
        
        # Get city data for the template
        city = City.query.get_or_404(city_id)
        
        # Store report in session or pass to template
        return render_template(
            "dispatch_report.html",
            city_id=city_id,
            city=city,
            report=report
        )
        
    except ValueError as e:
        flash(f"Configuration error: {str(e)}", "danger")
        return redirect(url_for("dashboard.view_city", city_id=city_id))
    except Exception as e:
        flash(f"Error generating report: {str(e)}", "danger")
        return redirect(url_for("dashboard.view_city", city_id=city_id))

@dashboard_bp.route("/<int:city_id>/download-report")
@login_required
def download_report(city_id):
    """Download dispatch report as text file"""
    try:
        # Check if OpenAI API key is configured
        if not current_app.config.get('OPENAI_API_KEY'):
            flash("OpenAI API key not configured. Please contact your administrator.", "danger")
            return redirect(url_for("dashboard.view_city", city_id=city_id))
        
        generator = ReportGenerator()
        report, error = generator.generate_dispatch_report(city_id)
        
        if error:
            flash(f"Error generating report: {error}", "danger")
            return redirect(url_for("dashboard.view_city", city_id=city_id))
        
        city = City.query.get_or_404(city_id)
        filename = f"dispatch_report_{city.name}_{city.state}_{city.country}.txt"
        
        from flask import Response
        return Response(
            report,
            mimetype="text/plain",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
        
    except ValueError as e:
        flash(f"Configuration error: {str(e)}", "danger")
        return redirect(url_for("dashboard.view_city", city_id=city_id))
    except Exception as e:
        flash(f"Error downloading report: {str(e)}", "danger")
        return redirect(url_for("dashboard.view_city", city_id=city_id))
