import json
import unittest
from http import HTTPStatus
from .. import create_app
from ..models.auth import User
from ..models.link import LinkModel
from ..utils import db
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required


class AuthTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app()

        self.appctx = self.app.app_context()

        self.appctx.push()

        self.client = self.app.test_client()

        db.create_all()

    def tearDown(self):
        db.drop_all()

        self.appctx.pop()

        self.app = None

        self.client = None
        
    def test_signup(self):
        signup_data = {
            'name': 'TestStudent',
            'email': 'testaccount@gmail.com',
            'password': 'testlaccount'
        }
        response = self.client.post('api/auth/signup', json=signup_data)
        user = User.query.filter_by(
            email='testaccount@gmail.com').first()
        assert user.name == "TestStudent"

        assert response.status_code == 201

    def test_login(self):
        login_data = {
            'email': 'johndoe@example.com',
            'password': 'password'
        }
        response = self.client.post('api/auth/login', json=login_data)
        assert response.status_code == 200
        
    #Get all shorrt links
    def test_getalllinks(self):
        user = User.query.filter_by(
            email='testaccount@gmail.com').first()
        token = create_access_token(identity=user)
    
        headers = {
            "Authorization": f"Bearer {token}"
        }
        links = LinkModel.query.all()
        response = self.client.get(
            '/api/link/all_link', json=links, headers=headers)
        assert response.status_code == 200
