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
    
    # Get observations for Kepler.gl data
    from models import Observation
    observations = Observation.query.filter_by(city_id=city_id).order_by(Observation.id.asc()).all()
    
    # Prepare data for Kepler.gl
    kepler_data = []
    for obs in observations:
        kepler_data.append({
            'week': obs.week_label,
            'cases': obs.cases,
            'city_name': city.name,
            'state': city.state,
            'country': city.country,
            'latitude': get_city_coordinates(city.name)[0],
            'longitude': get_city_coordinates(city.name)[1],
            'rt': ind.rt,
            'r0': ind.r0,
            'hospitalization_rate': ind.hospitalization_rate
        })
    
    return render_template(
        "dashboard.html",
        city=city,
        labels=labels,
        values=values,
        forecast=forecast,
        ind=ind,
        kepler_data=kepler_data,
    )

def get_city_coordinates(city_name):
    """Get coordinates for common cities"""
    city_coordinates = {
        'Recife': [-8.0476, -34.8770],
        'São Paulo': [-23.5505, -46.6333],
        'Rio de Janeiro': [-22.9068, -43.1729],
        'New York': [40.7128, -74.0060],
        'London': [51.5074, -0.1278],
        'Tokyo': [35.6762, 139.6503],
        'Freetown': [8.4844, -13.2284]
    }
    return city_coordinates.get(city_name, [0, 0])

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

@dashboard_bp.route("/<int:city_id>/kepler")
@login_required
def view_kepler(city_id):
    """View Kepler.gl visualization page"""
    city = City.query.get_or_404(city_id)
    ind = Indicator.query.filter_by(city_id=city_id).order_by(Indicator.id.desc()).first()
    if not ind:
        abort(404)
    
    # Get observations for Kepler.gl data
    from models import Observation
    observations = Observation.query.filter_by(city_id=city_id).order_by(Observation.id.asc()).all()
    
    # Prepare data for Kepler.gl
    kepler_data = []
    for obs in observations:
        kepler_data.append({
            'week': obs.week_label,
            'cases': obs.cases,
            'city_name': city.name,
            'state': city.state,
            'country': city.country,
            'latitude': get_city_coordinates(city.name)[0],
            'longitude': get_city_coordinates(city.name)[1],
            'rt': ind.rt,
            'r0': ind.r0,
            'hospitalization_rate': ind.hospitalization_rate
        })
    
    return render_template(
        "kepler_view.html",
        city=city,
        ind=ind,
        kepler_data=kepler_data,
        processed_data=None,
        error_message=None
    )

@dashboard_bp.route("/<int:city_id>/process-kepler-data", methods=["POST"])
@login_required
def process_kepler_data(city_id):
    """Process data with OpenAI for Kepler.gl visualization"""
    try:
        # Check if OpenAI API key is configured
        if not current_app.config.get('OPENAI_API_KEY'):
            flash("OpenAI API key not configured. Please contact your administrator.", "danger")
            return redirect(url_for("dashboard.view_kepler", city_id=city_id))
        
        city = City.query.get_or_404(city_id)
        ind = Indicator.query.filter_by(city_id=city_id).order_by(Indicator.id.desc()).first()
        if not ind:
            abort(404)
        
        # Get observations for Kepler.gl data
        from models import Observation
        observations = Observation.query.filter_by(city_id=city_id).order_by(Observation.id.asc()).all()
        
        # Prepare raw data for OpenAI processing
        raw_data = []
        for obs in observations:
            raw_data.append({
                'week': obs.week_label,
                'cases': obs.cases,
                'city_name': city.name,
                'state': city.state,
                'country': city.country,
                'latitude': get_city_coordinates(city.name)[0],
                'longitude': get_city_coordinates(city.name)[1],
                'rt': ind.rt,
                'r0': ind.r0,
                'hospitalization_rate': ind.hospitalization_rate
            })
        
        # Process with OpenAI to enhance data for Kepler.gl
        generator = ReportGenerator()
        processed_data, error = generator.process_kepler_data(raw_data, city, ind)
        
        if error:
            return render_template(
                "kepler_view.html",
                city=city,
                ind=ind,
                kepler_data=raw_data,
                processed_data=None,
                error_message=error
            )
        
        return render_template(
            "kepler_view.html",
            city=city,
            ind=ind,
            kepler_data=raw_data,
            processed_data=processed_data,
            error_message=None
        )
        
    except Exception as e:
        flash(f"Error processing data: {str(e)}", "danger")
        return redirect(url_for("dashboard.view_kepler", city_id=city_id))

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
