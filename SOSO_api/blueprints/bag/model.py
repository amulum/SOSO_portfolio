from blueprints import db
from flask_restful import fields
from datetime import datetime

class MyBag(db.Model):
    __tablename__ = 'mybag'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    customer_id = db.Column(db.Integer, db.ForeignKey('Customer.id', ondelete='CASCADE'), nullable = False)
    updated_at = db.Column(db.DateTime, default = None)
    details = db.relationship('MyBagDetails', backref='mybag', lazy='dynamic')

    mybag_fields = {
        'customer_id' : fields.Integer,
        'updated_at' : fields.String
    }

    def __init__(self, customer_id):
        self.customer_id = customer_id

    def __repr__(self):
        return '<Mybag %r>' % self.id

class MyBagDetails(db.Model):
    __tablename__ = 'bagdetails'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    mybag_id = db.Column(db.Integer, db.ForeignKey('mybag.id', ondelete='CASCADE'), nullable = False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id', ondelete='CASCADE'), nullable = False)
    amount = db.Column(db.Integer, nullable = False)
    product = db.relationship('Product', backref='bagdetails')

    def __init__(self, mybag_id, product_id, amount):
        self.mybag_id = mybag_id
        self.product_id = product_id
        self.amount = amount
    def __repr__(self):
        return '<MyBagDetails %r>' % self.mybag_id