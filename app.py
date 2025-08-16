import os
from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, login_required, current_user
from werkzeug.security import generate_password_hash
from config import Config
from models import db, User, City
from controllers.auth import auth_bp
from controllers.cities import cities_bp
from controllers.dashboard import dashboard_bp

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

    # Routes
    @app.route("/")
    def home():
        # Landing page explaining the Santé context
        if current_user.is_authenticated:
            return render_template("index.html")
        return redirect(url_for("auth.login"))

    # CLI command to (re)create DB and seed admin user
    @app.cli.command("init-db")
    def init_db():
        with app.app_context():
            db.drop_all()
            db.create_all()
            if not User.query.filter_by(username="admin").first():
                admin = User(username="admin", password_hash=generate_password_hash("admin"))
                db.session.add(admin)
                db.session.commit()
                print("Created admin user: admin / admin")
            os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
            print("Database initialized.")

    return app

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
        # Seed admin if missing
        from sqlalchemy import select
        from models import User
        if not User.query.filter_by(username="admin").first():
            from werkzeug.security import generate_password_hash
            admin = User(username="admin", password_hash=generate_password_hash("admin"))
            db.session.add(admin)
            db.session.commit()
            print("Created admin user: admin / admin")
        os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    app.run(host="0.0.0.0", port=5000, debug=True)
