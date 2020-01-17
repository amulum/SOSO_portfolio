# Import flask package
import json
import os
from flask import Flask, request, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_claims, get_jwt_identity
from flask_cors import CORS

# Others
from datetime import timedelta
from functools import wraps

app = Flask(__name__)
CORS(app)

app.config['APP_DEBUG'] = True

# JWT Setup
app.config['JWT_SECRET_KEY'] = 'iuahdLIXwaDOIXhodihowdoqd'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)
jwt = JWTManager(app)

# decorator internal only


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        identity = get_jwt_identity()
        if identity != 'ADMIN':
            return {'status': 'FORBIDDEN', 'message': 'ONLY ADMIN CAN DO THIS'}, 403
        else:
            return fn(*args, **kwargs)
    return wrapper

# decorator seller only


def seller_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        identity = get_jwt_identity()
        if identity != 'VERIFIED_SELLER':
            return {'status': 'FORBIDDEN', 'message': 'Verified Seller ONLY!! Please register to ADMIN'}, 403
        else:
            return fn(*args, **kwargs)
    return wrapper

# decorator seller only


def user_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        identity = get_jwt_identity()
        if identity != 'CUSTOMER':
            return {'status': 'FORBIDDEN', 'message': 'PLEASE USE CUSTOMER ACCOUNT or REGISTER FIRST!!'}, 403
        else:
            return fn(*args, **kwargs)
    return wrapper


# DB Setup
# try:
env = os.environ.get('FLASK_ENV', 'development')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:jg46!32B@0.0.0.0:3306/portfolio' if (
    env == 'testing') else 'mysql+pymysql://root:jg46!32B@0.0.0.0:3306/portfolio_test'
# except Exception as e:
#     raise e

# app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:jg46!32B@localhost:3306/rest_training'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

# From app.py
@app.after_request
def after_request(response):
    try:
        requestData = request.get_json()
    except Exception as e:
        requestData = request.args.to_dict()
    if response.status_code == 200:
        app.logger.info("REQUEST_LOG\t%s", json.dumps({
            'status_code': response.status_code,
            'method': request.method,
            'code': response.status,
            'url': request.full_path,
            'request': requestData,
            'response': json.loads(response.data.decode('utf-8'))
        }))
    else:
        app.logger.error("REQUEST_LOG\t%s", json.dumps({
            'status_code': response.status_code,
            'method': request.method,
            'code': response.status,
            'url': request.full_path,
            'request': requestData,
            'response': json.loads(response.data.decode('utf-8'))
        }))
    return response


# path
from blueprints.seller.resources import bp_seller
app.register_blueprint(bp_seller, url_prefix='/seller')
from blueprints.customer.resources import bp_customer
app.register_blueprint(bp_customer, url_prefix='/user')
from blueprints.admin.resources import bp_admin
app.register_blueprint(bp_admin, url_prefix='/admin')
# from blueprints.ongkir.resources import bp_ongkir
# app.register_blueprint(bp_ongkir, url_prefix='/admin/ongkir')


db.create_all()
