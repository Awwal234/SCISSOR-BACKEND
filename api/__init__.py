from flask import Flask
from flask_cors import CORS
from datetime import timedelta
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_restx import Api
from .utils import db
from .auth.auth_process import auth_namespace
from .scissor.action import action_namespace


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dft6562589101753'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///scissor.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'eff56820lops_get6312'
    app.config['CACHE_TYPE'] = 'simple'
    app.config['CACHE_DEFAULT_TIME'] = 300
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=2)
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=30)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    JWTManager(app)
    Migrate(app, db)
    api = Api(app, title='Api for Application')
    api.add_namespace(auth_namespace, path='/api/auth')
    api.add_namespace(action_namespace, path='/api/link')
    CORS(app, origin=api)

    return app