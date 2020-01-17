# Import
from blueprints import db
from flask_restful import fields
from datetime import datetime

# Create Model


class Customer(db.Model):
    __tablename__ = 'Customer'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), default='default@domain.com')
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    cust_address = db.relationship('ShippingAddress', backref='Customer', lazy='dynamic')
    cust_order = db.relationship('Order', backref='customer', lazy='dynamic')

    # yang nantinya diinfokan ke customer tentang info dirinya, id dan password dirahasiakan
    customer_fields = {
        'username': fields.String,
        'email': fields.String,
        'first_name': fields.String,
        'last_name': fields.String
    }

    admin_fields = {
        'id': fields.Integer,
        'username': fields.String,
        'password': fields.String,
        'email': fields.String,
        'first_name': fields.String,
        'last_name': fields.String,
    }

    jwt_claim_fields = {
        'id': fields.String,
        'username': fields.String,
    }

    def __init__(self, username, password, first_name, last_name, email):
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    def __repr__(self):
        return '<Customer %r>' % self.id


class ShippingAddress(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    address_name = db.Column(db.String(255), nullable=False)
    address_cid = db.Column(db.ForeignKey('Customer.id', ondelete='CASCADE'), nullable=False)
    address = db.Column(db.String(1000), nullable=False)
    country = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(255), nullable=False)
    postal_code = db.Column(db.String(6), nullable=False)
    phone_number = db.Column(db.String(14), nullable=False)
    address_order = db.relationship('Order', backref='shipping_address', lazy='dynamic')

    customer_fields = {
        'address_name': fields.String,
        'address': fields.String,
        'country': fields.String,
        'city': fields.String,
        'postal_code': fields.String,
        'phone_number': fields.String}

    def __init__(self, address_name, address_cid, address, country, city, postal_code, phone_number):
        self.address_name = address_name
        self.address_cid = address_cid
        self.address = address
        self.country = country
        self.city = city
        self.postal_code = postal_code
        self.phone_number = phone_number

    def __repr__(self):
        return f'<Address {self.address_name} from cust {self.address_cid}>'


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_cid = db.Column(db.ForeignKey('Customer.id', ondelete='CASCADE'), nullable=False)
    order_addrid = db.Column(db.ForeignKey('shipping_address.id', ondelete='CASCADE'), nullable=False)
    issue_date = db.Column(db.DateTime, nullable=False)
    is_deliver = db.Column(db.Boolean, default=False)
    delivery_date = db.Column(db.DateTime, default=None)
    # True if direct order from item page and checkout False when order created from bag
    is_direct_order = db.Column(db.Boolean, default=False)
    details = db.relationship('OrderDetails', backref='order', lazy='dynamic')

    customer_fields = {
        'id' : fields.Integer,
        'order_cid': fields.String,
        'order_addrid': fields.String,
        'issue_date': fields.DateTime,
        'is_deliver': fields.String,
        'delivery_date': fields.String,
    }

    def __init__(self, order_cid, order_addrid, issue_date):
        self.order_cid = order_cid
        self.order_addrid = order_addrid
        self.issue_date = issue_date

    def __repr__(self):
        return f'<Order {self.id} from cust {self.order_cid}>'


class OrderDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # foreign key for orderdetails from order id
    ordetails_oid = db.Column(db.ForeignKey('order.id', ondelete='CASCADE'), nullable=False)
    # foreign key for orderdetails from product id
    ordetails_pid = db.Column(db.ForeignKey('product.id', ondelete='CASCADE'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    product = db.relationship('Product', backref='order_details')

    customer_fields = {
        'ordetails_oid': fields.Integer,
        'ordetails_pid': fields.Integer,
        'quantity': fields.Integer
    }

    def __init__(self, ordetails_oid, ordetails_pid, quantity):
        self.ordetails_oid = ordetails_oid
        self.ordetails_pid = ordetails_pid

    def __repr__(self):
        return f'<DetailsOrder{self.id}, OrderID{self.ordetails_oid}, ProductID{self.ordetails_pid}>'


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    payment_oid = db.Column(db.ForeignKey('order.id', ondelete='CASCADE'), nullable=False)
    payment_type = db.Column(db.String(30), nullable=False)
    issue_date = db.Column(db.DateTime, default=None)
    is_paid = db.Column(db.Boolean, default=False)
    date_paid = db.Column(db.DateTime, default=None)
    amount = db.Column(db.Integer, default=None)

    admin_fields = {
        'id':  fields.Integer,
        'payment_oid': fields.Integer,
        'payment_type': fields.String,
        'issue_date': fields.DateTime,
        'is_paid': fields.Boolean,
        'date_paid': fields.DateTime,
        'amount': fields.Integer
    }

    def __init__(self, payment_oid, payment_type, issue_date, is_paid, amount):
        self.payment_oid = payment_oid
        self.payment_type = payment_type
        self.issue_date = issue_date
        self.amount = amount
        self.is_paid = is_paid

    def __repr__(self):
        return f'<Payment {self.id} orderID {self.payment_oid}, >'
