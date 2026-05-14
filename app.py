import os
from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, login_required, current_user
from werkzeug.security import generate_password_hash
from config import Config
from models import db, User, City, Settings
from controllers.auth import auth_bp
from controllers.cities import cities_bp
from controllers.dashboard import dashboard_bp
from controllers.admin import admin_bp
from controllers.hantawatch import hantawatch_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Init extensions
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(cities_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(admin_bp)
    # Hantawatch subdomain (public static site at hantawatch.<SERVER_NAME>).
    # Only active when SERVER_NAME is set in config (production); skipped in dev.
    if app.config.get("SERVER_NAME"):
        app.register_blueprint(hantawatch_bp)

    # Routes
    @app.route("/")
    def home():
        # Landing page explaining the Santé context
        if current_user.is_authenticated:
            return render_template("index.html")
        return redirect(url_for("auth.login"))

    # CLI command to (re)create DB
    @app.cli.command("init-db")
    def init_db():
        with app.app_context():
            db.drop_all()
            db.create_all()
            os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
            print("Database initialized.")

    # CLI command to create root admin user
    @app.cli.command("create-root")
    def create_root():
        import click
        email = os.environ.get("ROOT_ADMIN_EMAIL")
        if not email:
            email = click.prompt("Enter email for root admin")
        with app.app_context():
            if User.query.filter_by(email=email).first():
                print(f"Root admin already exists: {email}")
                return
            password = click.prompt("Enter password for root admin", hide_input=True, confirmation_prompt=True)
            root = User(
                username="root",
                email=email,
                password_hash=generate_password_hash(password),
                is_admin=True
            )
            db.session.add(root)
            db.session.commit()
            print(f"Created root admin: {email}")

    return app

def load_settings_to_config(app):
    """Load settings from database into app config"""
    with app.app_context():
        for setting in Settings.query.all():
            if setting.key == "openai_api_key":
                app.config["OPENAI_API_KEY"] = setting.value
            elif setting.key == "openai_model":
                app.config["OPENAI_MODEL"] = setting.value


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
        os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    load_settings_to_config(app)
    app.run(host="0.0.0.0", port=5000, debug=True)
