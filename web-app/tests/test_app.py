import datetime
import pytest
from app import app
from db import speeches_collection, users_collection
from bson.objectid import ObjectId
from unittest.mock import patch, MagicMock
import io


@pytest.fixture
def tester():
    """Set up Flask test client."""
    app.config["TESTING"] = True
    with app.test_client() as tester:
        yield tester

def test_login_page(tester):
    """Test that the login page loads."""
    response = tester.get("/login")
    assert response.status_code == 200

def test_index_redirects_not_loggedin(tester):
    """Test that index redirects if not logged in."""
    response = tester.get("/")
    assert response.status_code == 302
    assert "/login" in response.location

def test_index_loggedin(tester):
    """Test index redirects to dashboard when correctly logged in."""
    tester.post("/signup", data={
        "username": "testindex",
        "password": "password123",
        "password2": "password123"
    })
    response = tester.get("/", follow_redirects=True)
    assert response.status_code == 200
    

def test_dashboard_not_loggedin(tester):
    """Test that dashboard redirects to login if not logged in."""
    response = tester.get("/dashboard")
    assert response.status_code == 302
    assert "/login" in response.location


def test_record_not_loggedin(tester):
    """Test that record page redirects to login if not logged in."""
    response = tester.get("/record")
    assert response.status_code == 302
    assert "/login" in response.location


def test_submit_not_loggedin(tester):
    """Test that submitting redirects to login if not logged in."""
    response = tester.post("/submit")
    assert response.status_code == 302
    assert "/login" in response.location


def test_logout_tologin(tester):
    """Test that pressing logout redirects to login."""
    response = tester.get("/logout")
    assert response.status_code == 302
    assert "/login" in response.location


def test_signup_page(tester):
    """Test that the signup page loads."""
    response = tester.get("/signup")
    assert response.status_code == 200

def test_loggedin_signup(tester):
    """Test signup redirects to dashboard if already logged in."""
    tester.post("/signup", data={
        "username": "alreadysigned",
        "password": "password123",
        "password2": "password123"
    })
    response = tester.get("/signup", follow_redirects=True)
    assert response.status_code == 200

def test_emptylogin_username(tester):
    """Test login with empty username shows error."""
    response = tester.post("/login", data={
        "username": "",
        "password": "Testing"
    })
    assert response.status_code == 200
    assert b"Enter a username and password." in response.data

def test_wrong_login(tester):
    """Test login with incorrect username shows error."""
    response = tester.post("/login", data={
        "username": "fakeuser1234",
        "password": "wrongpassword"
    })
    assert response.status_code == 200
    assert b"Invalid username or password." in response.data

def test_login_wrong_password(tester):
    """Test login with correct username but wrong password shows error."""
    tester.post("/signup", data={
        "username": "wronguser",
        "password": "correctpassword",
        "password2": "correctpassword"
    })
    tester.get("/logout")
    response = tester.post("/login", data={
        "username": "wronguser",
        "password": "wrongpassword"
    })
    assert response.status_code == 200
    assert b"Invalid username or password" in response.data

