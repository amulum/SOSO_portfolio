# Import
from blueprints import db
from flask_restful import fields

# Create Model
class Seller(db.Model):
    __tablename__ = 'Seller'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    brand_name = db.Column(db.String(255), nullable = False)
    username = db.Column(db.String(255), nullable = False, unique = True)
    password = db.Column(db.String(255), nullable = False)
    email = db.Column(db.String(255), nullable = False)
    about_brand = db.Column(db.String(255), default = 'later')
    banner_image = db.Column(db.String(255), default = 'later')
    brand_video = db.Column(db.String(255), default = 'later')
    products = db.relationship('Product', backref='seller', lazy ='dynamic')

    # yang nantinya diinfokan ke seller tentang info dirinya, id dirahasiakan
    seller_fields = {
        'brand_name': fields.String,
        'username': fields.String,
        'email' : fields.String,
        'about_brand' : fields.String,
        'banner_image' : fields.String,
        'brand_video' : fields.String,

    }

    admin_fields = {
        'id' : fields.Integer,
        'brand_name': fields.String,
        'username': fields.String,
        'password' : fields.String,
        'email' : fields.String,
        'about_brand' : fields.String,
        'banner_image' : fields.String,
        'brand_video' : fields.String,

    }

    jwt_claim_fields = {
        'id' : fields.String,
        'username': fields.String,
    }

    def __init__(self, brand_name, username, password, email):
        self.brand_name = brand_name
        self.username = username
        self.password = password
        self.email = email
        

    def __repr__(self):
        return '<Seller %r>' % self.id