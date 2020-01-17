# ADMIN RESOURCE
# admin can get user and seller all and by id.
# admin can delete seller or user
# realnya kalo user or seller melanggar ketentuan maka akan di banned atau delete account
# kedepannya admin bisa create affilate link for spesific item yang bisa digunakan oleh user


# import flask
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from blueprints import app, db, admin_required
# import jwt
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_claims

# import model
from .model import Admin
from ..bag.model import *
from ..items.model import *
from blueprints.customer.model import Customer
from blueprints.seller.model import Seller

# Password Encription
from password_strength import PasswordPolicy
import hashlib

# import library
from datetime import datetime
from sqlalchemy import desc

bp_admin = Blueprint('admin', __name__)
api = Api(bp_admin)

class AdminGetToken(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', location='json', required=True)
        parser.add_argument('password', location='json', required=True)
        args = parser.parse_args()
        
        password_digest = hashlib.md5(args['password'].encode()).hexdigest()
        qry = Admin.query
        selected_admin = qry.filter_by(username=args['username']).first()
        if selected_admin:
            if selected_admin.password == password_digest:
                selected_admin.login_at = datetime.now().strftime("%a, %d %b %Y %X")
                db.session.commit()
                token = create_access_token(identity = 'ADMIN', user_claims={'username': args['username']})
                return {'token': token}, 200
        # INVALID USERNAME
        return {'status': 'FAILED', 'message': 'PLEASE CHECK USERNAME OR PASSWORD'}, 403

# /admin/register
class RegisterAdmin(Resource):
    @admin_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', location='json', required = True)
        parser.add_argument('password', location='json', required = True)
        args = parser.parse_args()

        # Setup the policy
        policy = PasswordPolicy.from_names(
            length = 8
        )
        # Validating the password policy
        validation = policy.test(args['password'])

        if validation == []:    
            password_digest = hashlib.md5(args['password'].encode()).hexdigest()
            # Creating object
            new_admin = Admin(args['username'], password_digest)
            db.session.add(new_admin)
            db.session.commit()

            app.logger.debug('DEBUG : %s', new_admin)

            return {'message' : 'New Admin Created!!!', 'Detail' : marshal(new_admin, Admin.admin_fields)}, 200, {'Content-Type':'application/json'}
        return {'status': 'FAILED', 'message': 'PLEASE ENTER PASSWORD WITH SPECIFIC FORMAT'}, 400


class AdminRootPath(Resource):
    # get by username in body json else get all
    @admin_required
    def get(self):
        # body json not none
        parser = reqparse.RequestParser()
        parser.add_argument('username', location='json')
        args = parser.parse_args()
        qry = Admin.query
        if args['username']:
            selected_admin = qry.filter_by(username=args['username']).first()
            if selected_admin:
                return marshal(selected_admin,Admin.admin_fields), 200, {'Content-Type':'application/json'}
            return {'message': 'Admin with specify username not found!'}, 404, {'Content-Type':'application/json'}

        # else no json body will get all admin
        lst_admin = qry.all()
        if lst_admin:
            admin_result = []
            for each_admin in lst_admin:
                admin_result.append(marshal(each_admin, Admin.admin_fields))
            return admin_result, 200, {'Content-Type':'application/json'}
        return {'message':'No admin account here, HOW CAN YOU ACCESS THIS PATH!!!'}, 404, {'Content-Type':'application/json'}

    @admin_required
    def delete(self):
        # required body json for username input
        parser = reqparse.RequestParser()
        parser.add_argument('username', location='json', required= True)
        args = parser.parse_args()
        selected_username = args['username']
        if args['username']:
            qry = Admin.query
            selected_admin = qry.filter_by(username=selected_username).first()
            if selected_admin:
                db.session.delete(selected_admin)
                db.session.commit()
                return {'message': f'Delete Admin Succesful with username = {selected_username}'} , 200, {'Content-Type':'application/json'}
        return {'message': 'Admin with specify username not found!'}, 404, {'Content-Type':'application/json'}

class AdminResourceForSeller(Resource):
    @admin_required
    # admin search seller by id or brand_name or username
    def get(self):
        # body json not none
        parser = reqparse.RequestParser()
        parser.add_argument('id', location='json')
        parser.add_argument('username', location='json')
        parser.add_argument('brand_name', location='json')
        args = parser.parse_args()
        qry = Seller.query

        # username or id filled
        if args['id'] or args['username'] or args['brand_name']:
            if args['id']: selected_seller = qry.filter_by(id=args['id']).first()
            if args['username']: selected_seller = qry.filter_by(username=args['username']).first()
            if args['brand_name']: selected_seller = qry.filter_by(brand_name=args['brand_name']).first()
            if selected_seller:
                return marshal(selected_seller,Seller.admin_fields), 200, {'Content-Type':'application/json'}
            return {'message': 'Seller not found!'}, 404, {'Content-Type':'application/json'}

        # else no json body will get all admin
        lst_seller = qry.all()
        if lst_seller:
            seller_result = []
            for each_seller in lst_seller:
                seller_result.append(marshal(each_seller, Seller.admin_fields))
            return seller_result, 200, {'Content-Type':'application/json'}
        return {'message':'No admin account here'}, 404, {'Content-Type':'application/json'}

    @admin_required
    # delete seller
    def delete(self):
        # required body json for username input
        parser = reqparse.RequestParser()
        parser.add_argument('id', location='json')
        parser.add_argument('username', location='json')
        parser.add_argument('brand_name', location='json')
        args = parser.parse_args()
        # input username or id
        qry = Seller.query
        if args['id'] or args['username'] or args['brand_name']:
            if args['id']: selected_seller = qry.filter_by(id=args['id']).first()
            if args['username']: selected_seller = qry.filter_by(username=args['username']).first()
            if args['brand_name']: selected_seller = qry.filter_by(brand_name=args['brand_name']).first()
            if selected_seller:
                db.session.delete(selected_seller)
                db.session.commit()
                return {'message': f'Delete Seller Success', 'details': marshal(selected_seller, Seller.admin_fields)} , 200, {'Content-Type':'application/json'}
        # username or id not found
        return {'message': 'Seller not found!'}, 404, {'Content-Type':'application/json'}

class AdminResourceForCust(Resource):
    @admin_required
    def get(self):
        # body json not none
        parser = reqparse.RequestParser()
        parser.add_argument('id', location='json')
        parser.add_argument('username', location='json')
        args = parser.parse_args()  
        qry = Customer.query
        # username or id filled
        if args['id'] or args['username']:
            if args['id']: selected_customer = qry.filter_by(id=args['id']).first()
            if args['username']: selected_customer = qry.filter_by(username=args['username']).first()
            if selected_customer:
                return marshal(selected_customer,Customer.admin_fields), 200, {'Content-Type':'application/json'}
            return {'message': 'Customer not found!'}, 404, {'Content-Type':'application/json'}
        # else no json body will get all admin
        lst_cust = qry.all()
        if lst_cust:
            customer_result = []
            for each_cust in lst_cust:
                customer_result.append(marshal(each_cust, Customer.admin_fields))
            return customer_result, 200, {'Content-Type':'application/json'}
        return {'message':'No customer account here'}, 404, {'Content-Type':'application/json'}

    @admin_required
    def delete(self):
        # required body json for username input
        parser = reqparse.RequestParser()
        parser.add_argument('id', location='json')
        parser.add_argument('username', location='json')
        args = parser.parse_args()
        qry = Customer.query
        if args['id']: selected_cust = qry.filter_by(id=args['id']).first()
        if args['username']: selected_cust = qry.filter_by(username=args['username']).first()
        if selected_cust:
            db.session.delete(selected_cust)
            db.session.commit()
            return {'message': f'Delete User Succesful', 'details':marshal(selected_cust,Customer.admin_fields)} , 200, {'Content-Type':'application/json'}
        return {'message': 'User with specify id or username not found!'}, 404, {'Content-Type':'application/json'}

class AdminResourceForPopular(Resource):
    # get popular item
    @admin_required
    def get(self):
        # MyBagDetails saat ini akan menggambarkan table Order
        # Table order tidak dimasukkan kedalam api dengan alasan keamanan
        # MyBagDetails ID yang diibaratkan sama dengan Order ID
        # popular item didapat dari order yg memuat item X entah brapapun amount-nya
        # dan akan di hitung dengan method count untuk order id dan group berdasarkan product id

        # reference query
        dum = db.session.query(MyBagDetails.product_id, db.func.count(MyBagDetails.id)).group_by(MyBagDetails.product_id).order_by(desc(db.func.count(MyBagDetails.id))).first()

        count_product = db.func.count(MyBagDetails.id)
        product_id = MyBagDetails.product_id
        qry = db.session.query(product_id, count_product).group_by(product_id).order_by(desc(count_product)).first()
        result_pid = qry[0]
        selected_product = Product.query.filter_by(id=result_pid).first()

        popular_item = {
            'Popular Item' : f'Product ID {result_pid}',
            'details' : marshal(selected_product, Product.cust_fields)
        }
        
        return popular_item, 200, {'Content-Type':'application/json'}


api.add_resource(AdminGetToken, '/login')
api.add_resource(RegisterAdmin, '/register')
api.add_resource(AdminRootPath, '')
api.add_resource(AdminResourceForSeller, '/seller')
api.add_resource(AdminResourceForCust, '/user')
api.add_resource(AdminResourceForPopular, '/popular')
