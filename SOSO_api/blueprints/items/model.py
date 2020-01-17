from blueprints import db
from flask_restful import fields
from datetime import datetime


class Stock(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    stock_pid = db.Column(db.Integer, db.ForeignKey('product.id', ondelete='CASCADE'), nullable = False)
    recent_qty = db.Column(db.Integer, default=0)
    qty_onupdate = db.Column(db.Integer, nullable = False)
    updated_at = db.Column(db.DateTime, default = None)
    current_qty = db.Column(db.Integer, default = 0)

    stock_fields = {
        'stock_pid' : fields.Integer,
        'recent_qty' : fields.Integer,
        'qty_onupdate' : fields.Integer,
        'updated_at' : fields.DateTime,
        'current_qty' : fields.Integer
    }
    
    seller_fields = {
        'recent_qty' : fields.Integer,
        'qty_onupdate' : fields.Integer,
        'updated_at' : fields.DateTime,
        'current_qty' : fields.Integer
    }

    def __init__(self, stock_pid, recent_qty, qty_onupdate, updated_at, current_qty):
        self.recent_qty = recent_qty
        self.qty_onupdate = qty_onupdate
        self.stock_pid = stock_pid
        self.updated_at = updated_at
        self.current_qty = current_qty
    
    def __repr__(self):
        return f'<Stock for ProductId {self.stock_pid}>'

    
# department have virtual column cat and sub cat
class Department(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(30), nullable = False, unique = True)
    categories = db.relationship('Category', backref='department', lazy ='dynamic')
    sub_categories = db.relationship('Subcategory', backref ='department', lazy='dynamic')
    products = db.relationship('Product', backref='department', lazy='dynamic')

    def __init__(self, name):
        self.name = name

# category have virtual column subcat
class Category(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(30), nullable = False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    sub_categories = db.relationship('Subcategory', backref ='category', lazy='dynamic')
    products = db.relationship('Product', backref='category', lazy='dynamic')

    def __init__(self, department_id, name):
        self.name = name
        self.department_id = department_id

class Subcategory(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(30), nullable = False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))

    def __init__(self, department_id, category_id, name):
        self.name = name
        self.category_id = category_id
        self.department_id = department_id

# product can be called in seller so seller must have virtual column of product
class Product(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(255), nullable = False)
    sub_name = db.Column(db.String(255), nullable = False)
    price = db.Column(db.Integer, default = None)
    discount = db.Column(db.Integer, default = 0)
    sell_price = db.Column(db.Integer, default = None)
    image_path = db.Column(db.String(1000), default = None)
    seller_id = db.Column(db.Integer, db.ForeignKey('Seller.id', ondelete='CASCADE'), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    subcategory_id = db.Column(db.Integer, db.ForeignKey('subcategory.id'))
    stock = db.relationship('Stock', backref='product')

# field dari product yang nantinya akan diinfokan ke seller
    seller_fields = {
        'id' : fields.Integer,
        'department_id' : fields.Integer,
        'category_id' : fields.Integer,
        'subcategory_id' : fields.Integer,
        'name' : fields.String,
        'sub_name' : fields.String,
        'price' : fields.Integer,
        'discount' : fields.Integer,
        'sell_price' : fields.Integer,
        'image_path' : fields.String
    }
    cust_fields = {
        'id' : fields.Integer,
        'department_id' : fields.Integer,
        'category_id' : fields.Integer,
        'subcategory_id' : fields.Integer,
        'name' : fields.String,
        'sub_name' : fields.String,
        'price' : fields.Integer,
        'discount' : fields.Integer,
        'sell_price' : fields.Integer,
        'image_path' : fields.String
    }


    def __init__(self, department_id, category_id, subcategory_id, name, sub_name, price, discount, sell_price, seller_id, image_path):
        self.department_id = department_id,
        self.category_id = category_id,
        self.subcategory_id = subcategory_id
        self.name = name,
        self.sub_name = sub_name,
        self.price = price,
        self.discount = discount,
        self.sell_price = sell_price,
        self.seller_id = seller_id,
        self.image_path = image_path

    def __repr__(self):
        return '<Product %r>' % self.name
