# tests/conftest.py

import os
import sys
import pytest

# Ensure project root is on sys.path so "import server" works
ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from server.app import app as flask_app
from server.models import db
from server.seed import seed_data


@pytest.fixture(scope="session")
def app():
    """
    Creates a Flask application configured for testing, with an in-memory DB.
    Runs seed_data() once at the beginning of the test session.
    """
    flask_app.config["TESTING"] = True
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    with flask_app.app_context():
        db.drop_all()
        db.create_all()
        # Use existing seed script to populate data
        seed_data()
        yield flask_app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Flask test client fixture."""
    return app.test_client()


@pytest.fixture
def db_session(app):
    """
    Simple fixture to provide a clean DB session per test that needs to
    insert/update/delete data directly.
    """
    with app.app_context():
        yield db.session
        db.session.rollback()
