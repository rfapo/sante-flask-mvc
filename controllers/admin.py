from functools import wraps
from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from models import db, User, City, Settings, Indicator, Observation

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def admin_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash("Access denied. Admin privileges required.", "danger")
            return redirect(url_for("home"))
        return f(*args, **kwargs)
    return decorated_function


@admin_bp.route("/")
@admin_required
def dashboard():
    users_count = User.query.count()
    cities_count = City.query.count()
    openai_key = Settings.query.filter_by(key="openai_api_key").first()
    has_openai = bool(openai_key and openai_key.value)
    return render_template("admin/dashboard.html",
                          users_count=users_count,
                          cities_count=cities_count,
                          has_openai=has_openai)


@admin_bp.route("/users")
@admin_required
def users_list():
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template("admin/users.html", users=users)


@admin_bp.route("/users/create", methods=["GET", "POST"])
@admin_required
def users_create():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        is_admin = request.form.get("is_admin") == "on"

        if not username or not password:
            flash("Username and password are required.", "danger")
            return render_template("admin/user_form.html", user=None)

        if User.query.filter_by(username=username).first():
            flash("Username already exists.", "danger")
            return render_template("admin/user_form.html", user=None)

        if email and User.query.filter_by(email=email).first():
            flash("Email already exists.", "danger")
            return render_template("admin/user_form.html", user=None)

        user = User(
            username=username,
            email=email if email else None,
            password_hash=generate_password_hash(password),
            is_admin=is_admin
        )
        db.session.add(user)
        db.session.commit()
        flash(f"User '{username}' created successfully.", "success")
        return redirect(url_for("admin.users_list"))

    return render_template("admin/user_form.html", user=None)


@admin_bp.route("/users/<int:user_id>/edit", methods=["GET", "POST"])
@admin_required
def users_edit(user_id):
    user = User.query.get_or_404(user_id)

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        is_admin = request.form.get("is_admin") == "on"

        if not username:
            flash("Username is required.", "danger")
            return render_template("admin/user_form.html", user=user)

        existing = User.query.filter_by(username=username).first()
        if existing and existing.id != user_id:
            flash("Username already exists.", "danger")
            return render_template("admin/user_form.html", user=user)

        if email:
            existing_email = User.query.filter_by(email=email).first()
            if existing_email and existing_email.id != user_id:
                flash("Email already exists.", "danger")
                return render_template("admin/user_form.html", user=user)

        user.username = username
        user.email = email if email else None
        user.is_admin = is_admin

        if password:
            user.password_hash = generate_password_hash(password)

        db.session.commit()
        flash(f"User '{username}' updated successfully.", "success")
        return redirect(url_for("admin.users_list"))

    return render_template("admin/user_form.html", user=user)


@admin_bp.route("/users/<int:user_id>/delete", methods=["POST"])
@admin_required
def users_delete(user_id):
    user = User.query.get_or_404(user_id)

    if user.id == current_user.id:
        flash("You cannot delete your own account.", "danger")
        return redirect(url_for("admin.users_list"))

    username = user.username
    db.session.delete(user)
    db.session.commit()
    flash(f"User '{username}' deleted successfully.", "success")
    return redirect(url_for("admin.users_list"))


@admin_bp.route("/cities")
@admin_required
def cities_list():
    cities = City.query.order_by(City.created_at.desc()).all()
    return render_template("admin/cities.html", cities=cities)


@admin_bp.route("/cities/<int:city_id>/delete", methods=["POST"])
@admin_required
def cities_delete(city_id):
    city = City.query.get_or_404(city_id)
    city_name = city.name

    Indicator.query.filter_by(city_id=city_id).delete()
    db.session.delete(city)
    db.session.commit()
    flash(f"City '{city_name}' and all its data deleted successfully.", "success")
    return redirect(url_for("admin.cities_list"))


@admin_bp.route("/settings", methods=["GET", "POST"])
@admin_required
def settings():
    SETTING_KEYS = [
        ("llm_provider",   "openai"),
        ("openai_api_key", ""),
        ("openai_model",   "gpt-4o-mini"),
        ("gemini_api_key", ""),
        ("gemini_model",   "gemini-1.5-flash"),
    ]

    if request.method == "POST":
        values = {}
        for key, default in SETTING_KEYS:
            values[key] = request.form.get(key, default).strip()

        # Don't overwrite existing key value if the field came back empty
        # (we render password fields blank on GET to avoid leaking the key in HTML).
        for key in ("openai_api_key", "gemini_api_key"):
            if values[key] == "":
                existing = Settings.query.filter_by(key=key).first()
                if existing and existing.value:
                    values[key] = existing.value

        for key, _ in SETTING_KEYS:
            setting = Settings.query.filter_by(key=key).first()
            if setting:
                setting.value = values[key]
            else:
                db.session.add(Settings(key=key, value=values[key]))
        db.session.commit()

        current_app.config["LLM_PROVIDER"]   = values["llm_provider"]
        current_app.config["OPENAI_API_KEY"] = values["openai_api_key"]
        current_app.config["OPENAI_MODEL"]   = values["openai_model"]
        current_app.config["GEMINI_API_KEY"] = values["gemini_api_key"]
        current_app.config["GEMINI_MODEL"]   = values["gemini_model"]

        flash("Settings updated successfully.", "success")
        return redirect(url_for("admin.settings"))

    # GET — load current values; mask API keys (we only show whether they're set).
    current = {}
    for key, default in SETTING_KEYS:
        setting = Settings.query.filter_by(key=key).first()
        current[key] = setting.value if setting else default

    return render_template(
        "admin/settings.html",
        llm_provider=current["llm_provider"],
        openai_api_key_set=bool(current["openai_api_key"]),
        openai_model=current["openai_model"],
        gemini_api_key_set=bool(current["gemini_api_key"]),
        gemini_model=current["gemini_model"],
    )
