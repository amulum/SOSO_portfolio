# Import
from blueprints import db
from flask_restful import fields
from datetime import datetime

# Create Model
class Admin(db.Model):
    __tablename__ = 'Admin'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    username = db.Column(db.String(255), nullable = False, unique = True)
    password = db.Column(db.String(255), nullable = False)
    created_at = db.Column(db.DateTime, default= datetime.now)
    login_at = db.Column(db.String(255), default= None)

    # yang nantinya diinfokan ke customer tentang info dirinya, id dan password dirahasiakan
    admin_fields = {
        'username': fields.String,
        'created_at': fields.DateTime,
        'login_at': fields.String
    }

    jwt_claim_fields = {
        'id' : fields.String,
        'username': fields.String,
    }

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<Admin %r>' % self.id