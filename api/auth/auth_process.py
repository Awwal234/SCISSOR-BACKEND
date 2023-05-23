from flask_restx import Namespace, Resource, fields
from flask import request
from http import HTTPStatus
from ..models.auth import User
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_refresh_token, create_access_token, jwt_required, get_jwt_identity

auth_namespace = Namespace('auth_process', description='Auth process for users')
signup_model = auth_namespace.model('SignUp', {
    'id': fields.Integer(),
    'name': fields.String(required=True, description='User name'),
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password'),
})
login_model = auth_namespace.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password'),
})

@auth_namespace.route('/signup')
class signupUser(Resource):
    @auth_namespace.expect(signup_model)
    @auth_namespace.marshal_with(signup_model)
    def post(self):
        '''
            Signup User to create a account.
        '''
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        password = generate_password_hash(data.get('password'))
        
        new_user = User(name=name, email=email, password=password)
        new_user.save()
        
        return new_user, HTTPStatus.CREATED
        
@auth_namespace.route('/login')
class LoginUser(Resource):
    @auth_namespace.expect(login_model)
    def post(self):
        '''
            Login User
        '''
        data = request.get_json()
        email = data['email']
        
        user = User.query.filter_by(email=email).first()
        
        if (user is not None) and check_password_hash(user.password, data['password']):
            access_token = create_access_token(identity=email)
            refresh_token = create_refresh_token(identity=email)
            response = {
                'access_token': access_token,
                'refresh_token': refresh_token
            }
            
            return response, HTTPStatus.CREATED
      
@auth_namespace.route('/refresh')
class RefreshToken(Resource):
    @jwt_required(refresh=True)
    def get(self):
        '''
            Refresh user Token
        '''
        
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        refresh_token = create_refresh_token(identity=current_user)
        response = {
            'access_token': access_token,
            'refresh_token': refresh_token
        }
        
        return response, HTTPStatus.CREATED
        
@auth_namespace.route('/getme')
class GetUserName(Resource):
    @jwt_required()
    def get(self):
        '''
            Get User Profile
        '''

        current_user = get_jwt_identity()
        user = User.query.filter_by(email=current_user).first()
        get_name = user.name

        response = {
            'email': current_user,
            'name': get_name,
        }

        return response, HTTPStatus.OK
        
        
#TODO: add rate limiting to my bitly code link