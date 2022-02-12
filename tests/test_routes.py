"""
This file contains the functional tests for the routes.
These tests use GETs and POSTs to different URLs to check for the proper behavior.
Resources:
    https://flask.palletsprojects.com/en/1.1.x/testing/ 
    https://www.patricksoftwareblog.com/testing-a-flask-application-using-pytest/ 
"""
import os
import pytest
from app import create_app, db
from app.Model.models import User, Post
from config import Config



class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SECRET_KEY = 'bad-bad-key'
    WTF_CSRF_ENABLED = False
    DEBUG = True
    TESTING = True


@pytest.fixture(scope='module')
def test_client():
    app = create_app(config_class=TestConfig)

    db.init_app(app)
    testing_client = app.test_client()

    ctx = app.app_context()
    ctx.push()

    yield testing_client

    ctx.pop()

def new_user(uname, uemail,passwd, utype):
    user = User(username=uname, email=uemail, usertype = utype)
    user.set_password(passwd)
    return user

@pytest.fixture
def init_database():
    db.create_all()
 
    user1 = new_user(uname='test', uemail='test@wsu.edu',passwd='1234')
    db.session.add(user1)
    db.session.commit()
    yield
    db.drop_all()

'''
    GET testing (Ensuring each page is properly loaded when requested)
'''
# Auth_routes testing
def test_register_page(test_client):
    response = test_client.get('/register')
    assert response.status_code == 200
    assert b"Register" in response.data

def test_login_page(test_client):
    response = test_client.get('/login')
    assert response.status_code == 200
    assert b"Login" in response.data

# Routes testing
def test_index_page(test_client):
    response = test_client.get('/')
    assert response.status_code == 200
    assert b"Research Outreach" in response.data

'''
    Testing to ensure that these pages cannot be accessed if @login_required is needed
    and user is not logged in
'''
def test_home_page(test_client):
    response = test_client.get('/home')
    assert response.status_code != 200 # home wont load when not logged in
    assert b"login" in response.data

def test_setup_page(test_client):
    response = test_client.get('/setup')
    assert response.status_code != 200
    assert b"login" in response.data

def test_submittedapps_page(test_client):
    response = test_client.get('/submittedapps')
    assert response.status_code != 200
    assert b"login" in response.data

def test_edit_page(test_client):
    response = test_client.get('/edit')
    assert response.status_code != 200
    assert b"login" in response.data

def test_post_page(test_client):
    response = test_client.get('/post')
    assert response.status_code != 200
    assert b"login" in response.data




