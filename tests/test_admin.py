import pytest
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from models import db, User, City, Settings
from werkzeug.security import generate_password_hash


@pytest.fixture
def app():
    """Create and configure a test application instance."""
    from flask import Flask
    from flask_login import LoginManager
    from models import db as _db
    from controllers.auth import auth_bp
    from controllers.cities import cities_bp
    from controllers.dashboard import dashboard_bp
    from controllers.admin import admin_bp

    import os
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    test_app = Flask(__name__,
                     template_folder=os.path.join(base_dir, 'templates'),
                     static_folder=os.path.join(base_dir, 'static'))
    test_app.config['TESTING'] = True
    test_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    test_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    test_app.config['SECRET_KEY'] = 'test-secret'
    test_app.config['WTF_CSRF_ENABLED'] = False
    test_app.config['UPLOAD_FOLDER'] = '/tmp/uploads'

    _db.init_app(test_app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(test_app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    test_app.register_blueprint(auth_bp)
    test_app.register_blueprint(cities_bp)
    test_app.register_blueprint(dashboard_bp)
    test_app.register_blueprint(admin_bp)

    @test_app.route("/")
    def home():
        from flask_login import current_user
        from flask import render_template, redirect, url_for
        if current_user.is_authenticated:
            return render_template("index.html")
        return redirect(url_for("auth.login"))

    with test_app.app_context():
        _db.create_all()
        # Create root admin user for tests
        root = User(
            username="root",
            email="testadmin@example.com",
            password_hash=generate_password_hash("TestPassword123!"),
            is_admin=True
        )
        _db.session.add(root)
        _db.session.commit()
        yield test_app
        _db.drop_all()


@pytest.fixture
def client(app):
    """Create a test client."""
    return app.test_client()


@pytest.fixture
def auth_client(client, app):
    """Create an authenticated test client as admin."""
    with app.app_context():
        client.post('/login', data={
            'username': 'testadmin@example.com',
            'password': 'TestPassword123!'
        })
    return client


class TestAuthentication:
    """Test authentication functionality."""

    def test_login_page_loads(self, client):
        """Test that login page loads correctly."""
        response = client.get('/login')
        assert response.status_code == 200
        assert b'Sign in' in response.data

    def test_login_with_email(self, client):
        """Test login with email works."""
        response = client.post('/login', data={
            'username': 'testadmin@example.com',
            'password': 'TestPassword123!'
        }, follow_redirects=True)
        assert response.status_code == 200
        assert b'Login successful' in response.data

    def test_login_with_username(self, client):
        """Test login with username works."""
        response = client.post('/login', data={
            'username': 'root',
            'password': 'TestPassword123!'
        }, follow_redirects=True)
        assert response.status_code == 200
        assert b'Login successful' in response.data

    def test_login_invalid_credentials(self, client):
        """Test login with invalid credentials fails."""
        response = client.post('/login', data={
            'username': 'wrong@email.com',
            'password': 'wrongpassword'
        }, follow_redirects=True)
        assert response.status_code == 200
        assert b'Invalid credentials' in response.data

    def test_logout(self, auth_client):
        """Test logout works."""
        response = auth_client.get('/logout', follow_redirects=True)
        assert response.status_code == 200
        assert b'Logged out' in response.data


class TestAdminAccess:
    """Test admin access control."""

    def test_admin_dashboard_requires_login(self, client):
        """Test that admin dashboard requires login."""
        response = client.get('/admin/', follow_redirects=True)
        assert b'Sign in' in response.data

    def test_admin_dashboard_requires_admin_role(self, client, app):
        """Test that admin dashboard requires admin role."""
        # Create non-admin user
        with app.app_context():
            user = User(
                username="regular",
                email="regular@test.com",
                password_hash=generate_password_hash("password"),
                is_admin=False
            )
            db.session.add(user)
            db.session.commit()

        # Login as non-admin
        client.post('/login', data={
            'username': 'regular',
            'password': 'password'
        })

        response = client.get('/admin/', follow_redirects=True)
        assert b'Access denied' in response.data

    def test_admin_dashboard_loads_for_admin(self, auth_client):
        """Test that admin dashboard loads for admin user."""
        response = auth_client.get('/admin/')
        assert response.status_code == 200
        assert b'Admin Dashboard' in response.data


class TestUserManagement:
    """Test user management functionality."""

    def test_users_list(self, auth_client):
        """Test that users list loads."""
        response = auth_client.get('/admin/users')
        assert response.status_code == 200
        assert b'User Management' in response.data

    def test_create_user_form(self, auth_client):
        """Test that create user form loads."""
        response = auth_client.get('/admin/users/create')
        assert response.status_code == 200
        assert b'Create New User' in response.data

    def test_create_user(self, auth_client, app):
        """Test creating a new user."""
        response = auth_client.post('/admin/users/create', data={
            'username': 'newuser',
            'email': 'newuser@test.com',
            'password': 'newpassword',
            'is_admin': ''
        }, follow_redirects=True)

        assert response.status_code == 200
        assert b'created successfully' in response.data

        with app.app_context():
            user = User.query.filter_by(username='newuser').first()
            assert user is not None
            assert user.email == 'newuser@test.com'
            assert not user.is_admin

    def test_create_admin_user(self, auth_client, app):
        """Test creating an admin user."""
        response = auth_client.post('/admin/users/create', data={
            'username': 'adminuser',
            'email': 'admin@test.com',
            'password': 'adminpassword',
            'is_admin': 'on'
        }, follow_redirects=True)

        assert response.status_code == 200

        with app.app_context():
            user = User.query.filter_by(username='adminuser').first()
            assert user is not None
            assert user.is_admin

    def test_create_user_duplicate_username(self, auth_client):
        """Test creating user with duplicate username fails."""
        response = auth_client.post('/admin/users/create', data={
            'username': 'root',
            'email': 'another@test.com',
            'password': 'password'
        }, follow_redirects=True)

        assert response.status_code == 200
        assert b'already exists' in response.data

    def test_edit_user(self, auth_client, app):
        """Test editing a user."""
        # Create user to edit
        with app.app_context():
            user = User(
                username="toedit",
                email="toedit@test.com",
                password_hash=generate_password_hash("password"),
                is_admin=False
            )
            db.session.add(user)
            db.session.commit()
            user_id = user.id

        response = auth_client.post(f'/admin/users/{user_id}/edit', data={
            'username': 'edited',
            'email': 'edited@test.com',
            'password': '',
            'is_admin': 'on'
        }, follow_redirects=True)

        assert response.status_code == 200
        assert b'updated successfully' in response.data

        with app.app_context():
            user = User.query.get(user_id)
            assert user.username == 'edited'
            assert user.is_admin

    def test_delete_user(self, auth_client, app):
        """Test deleting a user."""
        # Create user to delete
        with app.app_context():
            user = User(
                username="todelete",
                email="todelete@test.com",
                password_hash=generate_password_hash("password"),
                is_admin=False
            )
            db.session.add(user)
            db.session.commit()
            user_id = user.id

        response = auth_client.post(f'/admin/users/{user_id}/delete', follow_redirects=True)

        assert response.status_code == 200
        assert b'deleted successfully' in response.data

        with app.app_context():
            user = User.query.get(user_id)
            assert user is None


class TestCityManagement:
    """Test city management functionality."""

    def test_cities_list(self, auth_client):
        """Test that cities list loads."""
        response = auth_client.get('/admin/cities')
        assert response.status_code == 200
        assert b'City Management' in response.data

    def test_delete_city(self, auth_client, app):
        """Test deleting a city."""
        # Create city to delete
        with app.app_context():
            city = City(
                name="TestCity",
                state="TestState",
                country="TestCountry"
            )
            db.session.add(city)
            db.session.commit()
            city_id = city.id

        response = auth_client.post(f'/admin/cities/{city_id}/delete', follow_redirects=True)

        assert response.status_code == 200
        assert b'deleted successfully' in response.data

        with app.app_context():
            city = City.query.get(city_id)
            assert city is None


class TestSettings:
    """Test settings functionality."""

    def test_settings_page_loads(self, auth_client):
        """Test that settings page loads."""
        response = auth_client.get('/admin/settings')
        assert response.status_code == 200
        assert b'Settings' in response.data

    def test_save_openai_settings(self, auth_client, app):
        """Test saving OpenAI settings."""
        response = auth_client.post('/admin/settings', data={
            'openai_api_key': 'sk-test-key-12345',
            'openai_model': 'gpt-4o'
        }, follow_redirects=True)

        assert response.status_code == 200
        assert b'Settings updated' in response.data

        with app.app_context():
            key_setting = Settings.query.filter_by(key='openai_api_key').first()
            model_setting = Settings.query.filter_by(key='openai_model').first()
            assert key_setting.value == 'sk-test-key-12345'
            assert model_setting.value == 'gpt-4o'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
