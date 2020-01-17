# SELLER RESOURCES #
# contain crud for seller but create and delete seller only authorized for admin
# contain crud product authorized for seller only

# import flask
from flask import Blueprint, jsonify
from flask_restful import Api, Resource, reqparse, marshal
from blueprints import app, db
from blueprints import seller_required, admin_required
from sqlalchemy import literal, desc, asc

from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_claims
# import model
from .model import Seller
from ..items.model import *
from ..items.model import Stock
# Password Encription
from password_strength import PasswordPolicy
import hashlib

from datetime import datetime


# Creating blueprint
bp_seller = Blueprint('seller', __name__)
api = Api(bp_seller)

# SELLER LOGIN PAGE
class SellerCreateTokenResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', location='json', required=True)
        parser.add_argument('password', location='json', required=True)
        args = parser.parse_args()

        # Verified Seller
        password_digest = hashlib.md5(args['password'].encode()).hexdigest()
        qry = Seller.query
        selected_seller = qry.filter_by(username= args['username']).filter_by(password=password_digest).first()
        if selected_seller:
            token = create_access_token(identity = 'VERIFIED_SELLER', user_claims={'id': selected_seller.id, 'username': args['username']})
            return {'token': token}, 200

        # INVALID USERNAME
        return {'status': 'FAILED', 'message': 'PLEASE CHECK USERNAME OR PASSWORD'}, 403

# REGISTER NEW SELLER
class RegisterSeller(Resource):
    @admin_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', location='json', required=True)
        parser.add_argument('password', location='json', required=True)
        parser.add_argument('brand_name', location='json', required=True)
        parser.add_argument('email', location='json', required=True)
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
            new_seller = Seller(brand_name=args['brand_name'], username=args['username'], password=password_digest, email=args['email'])
            print(new_seller)
            db.session.add(new_seller)
            db.session.commit()

            app.logger.debug('DEBUG : %s', new_seller)

            return {'message' : 'New Seller Created!!!', 'Detail' : marshal(new_seller, Seller.seller_fields)}, 200, {'Content-Type':'application/json'}
        return {'status': 'FAILED', 'message': 'PLEASE ENTER PASSWORD WITH SPECIFIC FORMAT'}, 400


# SELLER INFO SELF
class SellerInfoSelf(Resource):
    @seller_required
    def get(self):
        qry = Seller.query
        claims = get_jwt_claims()
        selected_seller = qry.filter_by(username=claims['username']).first()
        
        app.logger.debug('DEBUG : %s', selected_seller)

        return marshal(selected_seller, Seller.seller_fields), 200, {'Content-Type':'application/json'}


class SellerEditSelf(Resource):
    # put method must input all argument except username
    @seller_required
    def put(self):
        claims = get_jwt_claims()
        parser = reqparse.RequestParser()
        parser.add_argument('password', location='json', required=True)
        parser.add_argument('brand_name', location='json', required=True)
        parser.add_argument('email', location='json', required=True)
        parser.add_argument('about_brand', location='json', required=True)
        parser.add_argument('banner_image', location='json', required=True)
        parser.add_argument('brand_video', location='json', required=True)
        args = parser.parse_args()

        policy = PasswordPolicy.from_names(
            length = 8
        )
        # Validating the password policy
        validation = policy.test(args['password'])

        if validation == []:    
            password_digest = hashlib.md5(args['password'].encode()).hexdigest()
            # search selected cust
            qry = Seller.query
            selected_seller = qry.filter_by(id=claims['id']).first()
            # edit each elemen
            selected_seller.password = password_digest
            selected_seller.brand_name = args['brand_name']
            selected_seller.email = args['email']
            selected_seller.about_brand = args['about_brand']
            selected_seller.banner_image = args['banner_image']
            selected_seller.brand_video = args['brand_video']
            db.session.commit()

            app.logger.debug('DEBUG : %s', selected_seller)

            return {'message' : 'Your profile UPDATED!', 'Detail' : marshal(selected_seller, Seller.seller_fields)}, 200, {'Content-Type':'application/json'}
        
        # password format doesnt match to policy
        return {'status': 'FAILED', 'message': 'PLEASE ENTER PASSWORD WITH SPECIFIC FORMAT'}, 400

    @seller_required
    def patch(self):
        claims = get_jwt_claims()
        parser = reqparse.RequestParser()
        parser.add_argument('password', location='json')
        parser.add_argument('brand_name', location='json')
        parser.add_argument('email', location='json')
        parser.add_argument('about_brand', location='json')
        parser.add_argument('banner_image', location='json')
        parser.add_argument('brand_video', location='json')
        args = parser.parse_args()

        policy = PasswordPolicy.from_names(
            length = 8
        )

        # search selected cust
        qry = Seller.query
        selected_seller = qry.filter_by(id=claims['id']).first()
        
        # edit per elemen if its not none
        if args['brand_name']: selected_seller.brand_name = args['brand_name']
        if args['email']: selected_seller.email = args['email']
        if args['about_brand']: selected_seller.about_brand = args['about_brand']
        if args['banner_image']: selected_seller.banner_image = args['banner_image']
        if args['brand_video']: selected_seller.brand_video = args['brand_video']
        if args['password']:
            validation = policy.test(args['password'])
            # Validating the password policy
            if validation == []:    
                password_digest = hashlib.md5(args['password'].encode()).hexdigest()
                selected_seller.password = password_digest
                
        db.session.commit()
        app.logger.debug('DEBUG : %s', selected_seller)

        return {'message' : 'Your profile UPDATED!', 'Detail' : marshal(selected_seller, Product.seller_fields)}, 200, {'Content-Type':'application/json'}


class SellerProduct(Resource):
    @seller_required
    def post(self):
        claims = get_jwt_claims()
        parser = reqparse.RequestParser()
        parser.add_argument('department_id', location='json', required = True)
        parser.add_argument('category_id', location='json', required = True)
        parser.add_argument('subcategory_id', location='json', required = True)
        parser.add_argument('name', location='json', required = True)
        parser.add_argument('sub_name', location='json', required = True)
        parser.add_argument('price', location='json', required = True)
        parser.add_argument('image_path', location='json', required = True)
        parser.add_argument('discount', location='json')
        args = parser.parse_args()

        if args['discount']:
            if int(args['discount']) != 0 and int(args['discount']) < 100:
                selling_price = int(args['price']) * (100-int(args['discount']))/100
        else:
            selling_price = int(args['price'])

        new_product  = Product(
            seller_id= claims['id'],
            department_id= args['department_id'],
            category_id= args['category_id'],
            subcategory_id= args['subcategory_id'],
            name= args['name'],
            sub_name= args['sub_name'],
            price= args['price'],
            discount= args['discount'],
            sell_price= selling_price,
            image_path= args['image_path']
        )
        db.session.add(new_product)
        db.session.commit()

        app.logger.debug('DEBUG : %s', new_product)

        return {'message' : 'New Product Created!!!', 'Detail' : marshal(new_product, Product.seller_fields)}, 200, {'Content-Type':'application/json'}

    @seller_required
    def get(self):
        claims = get_jwt_claims()
        parser = reqparse.RequestParser()
        parser.add_argument('page', location='json', default = 1)
        parser.add_argument('limit', location='json', default = 10)
        parser.add_argument("order_by", location="json", help="invalid order-by value", choices=("id", "price"))
        parser.add_argument("sort", location="json", help="invalid sort value", choices=("desc","asc"))
        # filter product element
        parser.add_argument('id', location='json')
        parser.add_argument('department_id', location='json')
        parser.add_argument('name', location='json')
        args = parser.parse_args()
        
        # search by input department_id or args name contain in field name
        qry = Product.query.filter_by(seller_id=claims['id'])
        if args['id']:
            qry = qry.filter_by(id= args['id'])
        if args['department_id']:
            qry = qry.filter_by(department_id= args['department_id'])
        if args['name']:
            qry = qry.filter(Product.name.contains(args['name']))

        # sort and order
        if args["order_by"] == "id":
            if args["sort"] == "desc": qry = qry.order_by(desc(Product.id))
            else: qry = qry.order_by(Product.id)
        elif args["order_by"] == "price":
            if args["sort"] == "desc": qry = qry.order_by(desc(Product.sell_price))
            else: qry = qry.order_by(Product.sell_price)

        # pagination
        offset = (int(args["page"]) - 1)*int(args["limit"])
        qry = qry.limit(int(args['limit'])).offset(offset)

        lst_product = qry.all()
        if lst_product:
            product_result = []
            for index in range(len(lst_product)):
                marshal_product = (marshal(lst_product[index], Product.seller_fields))
                format_product = {
                    'Product' : index+1,
                    'Details' : marshal_product
                }
                product_result.append(format_product)

            app.logger.debug('DEBUG : %s', product_result)
            # pagination format
            return {
                'page': args['page'],
                'limit_per_page' : args['limit'],
                'result' : product_result
                }, 200, {'Content-Type':'application/json'}
        # product not found
        return {'message':'Product Not Found'}, 404, {'Content-Type':'application/json'}
    
    # cannot edit department, cate, and subcate
    # input product id in params and editable field in json body
    @seller_required
    def patch(self):
        claims = get_jwt_claims()
        parser = reqparse.RequestParser()
        parser.add_argument('id', location='json',required=True)
        # editable field
        parser.add_argument('name', location='json')
        parser.add_argument('sub_name', location='json')
        parser.add_argument('price', location='json')
        parser.add_argument('discount', location='json')
        args = parser.parse_args()

        qry = Product.query
        selected_product = qry.filter_by(id=args['id']).filter_by(seller_id=claims['id']).first()
        if selected_product:
            # edit field if json body filled
            if args['name']: selected_product.name = args['name']
            if args['sub_name']: selected_product.sub_name = args['sub_name']
            if args['price']: selected_product.price = args['price']
            if args['discount']:
                selected_product.discount = args['discount']
                selected_product.sell_price = int(selected_product.price) *(100-int(args['discount']))/100
            else:
                selected_product.sell_price = int(selected_product.price) *(100-int(selected_product.discount))/100
            db.session.commit()
            app.logger.debug('DEBUG : %s', selected_product)
            return marshal(selected_product, Product.seller_fields), 200, {'Content-Type':'application/json'}
        # else product not found
        return {'message':'Product Not Found'}, 404, {'Content-Type':'application/json'}
    
    # put method can edit all field except id
    @seller_required
    def put(self):
        claims = get_jwt_claims()
        parser = reqparse.RequestParser()
        parser.add_argument('id', location='json',required=True)
        # editable field
        parser.add_argument('department_id', location='json', required = True)
        parser.add_argument('category_id', location='json', required = True)
        parser.add_argument('subcategory_id', location='json', required = True)
        parser.add_argument('name', location='json', required = True)
        parser.add_argument('sub_name', location='json', required = True)
        parser.add_argument('price', location='json', required = True)
        parser.add_argument('discount', location='json')
        args = parser.parse_args()

        qry = Product.query
        selected_product = qry.filter_by(id=args['id']).filter_by(seller_id=claims['id']).first()
        if selected_product:
            # edit field if json body filled
            selected_product.department_id = args['department_id']
            selected_product.category_id = args['category_id']
            selected_product.subcategory_id = args['subcategory_id']
            selected_product.name = args['name']
            selected_product.sub_name = args['sub_name']
            selected_product.price = args['price']
            # special case discount
            if args['discount']:
                selected_product.discount = args['discount']
                selected_product.sell_price = int(selected_product.price) *(100-int(args['discount']))/100
            else:
                selected_product.sell_price = int(selected_product.price) *(100-int(selected_product.discount))/100
            db.session.commit()
            app.logger.debug('DEBUG : %s', selected_product)
            return marshal(selected_product, Product.seller_fields), 200, {'Content-Type':'application/json'}
        # else product not found
        return {'message':'Product Not Found'}, 404, {'Content-Type':'application/json'}

    # input id in param
    @seller_required
    def delete(self):
        claims = get_jwt_claims()
        parser = reqparse.RequestParser()
        parser.add_argument('id', location='json',required=True)
        args = parser.parse_args()
        qry = Product.query
        selected_product = qry.filter_by(id=args['id']).first()
        if selected_product:
            db.session.delete(selected_product)
            db.session.commit()
            return {
                'message': 'Delete Product Succesful',
                'details': marshal(selected_product,Product.seller_fields)
            } , 200, {'Content-Type':'application/json'}
            
        return {'message': 'Product with specify id not found!'}, 404, {'Content-Type':'application/json'}
        

# stock product only for specific seller
class SellerStockProduct(Resource):
    # qty on update bisa + atau -
    # kalo negatif brarti dikurangi aja 
    @seller_required
    def post(self):
        claims = get_jwt_claims()
        parser = reqparse.RequestParser()
        parser.add_argument('stock_pid', location='json', required = True)
        parser.add_argument('qty_onupdate', location='json', required = True)
        args = parser.parse_args()

        # filter product by seller id 
        qry = Product.query.filter_by(seller_id=claims['id'])
        # filter product by selected product_id
        selected_product = qry.filter_by(id=args['stock_pid']).first()
        selected_stock = selected_product.stock
        # qty onupdate harus > 0 untuk create row stock logikanya kalo awal masukin stock kita input angka 0 maka siasia stock
        if selected_product and selected_stock == [] and int(args['qty_onupdate']) > 0:
            new_stock = Stock(
                stock_pid = args['stock_pid'],
                recent_qty= args['qty_onupdate'],
                qty_onupdate = args['qty_onupdate'],
                updated_at = datetime.now(),
                current_qty = int(args['qty_onupdate'])
                )
            db.session.add(new_stock)
            db.session.commit()
            return {
                'message': 'Add Stock Succesful',
                'details': marshal(new_stock,Stock.stock_fields)
            } , 200, {'Content-Type':'application/json'}

        elif selected_product and selected_stock:
            # product found and row stock filled
            # edit element stockqty
            selected_stock = selected_stock[0]
            selected_stock.recent_qty = selected_stock.current_qty
            selected_stock.qty_onupdate = args['qty_onupdate']
            selected_stock.updated_at = datetime.now()
            selected_stock.current_qty = int(selected_stock.current_qty) + int(args['qty_onupdate'])
            db.session.commit()
            return {
                'message': 'Add Stock Succesful',
                'details': marshal(selected_stock,Stock.stock_fields)
            } , 200, {'Content-Type':'application/json'}

        elif int(args['qty_onupdate']) < 1:
            return {'message': 'Qty must be > 1 to add new stock row with selected product id'}, 400, {'Content-Type':'application/json'}

        else:
            # search product by input porduct id not found return 404
            return {'message': 'Product with specify id not found or check your input field!'}, 404, {'Content-Type':'application/json'}

    @seller_required
    def get(self):
        # get selected product id with stock
        # stock not found
        claims = get_jwt_claims()
        parser = reqparse.RequestParser()
        parser.add_argument('stock_pid', location='json', required = True)
        args = parser.parse_args()

        # filter product by seller id 
        qry = Product.query.filter_by(seller_id=claims['id'])
        # filter product by selected product_id
        selected_product = qry.filter_by(id=args['stock_pid']).first()
        if selected_product:
            print(selected_product)
            print(selected_product.stock)
            if selected_product.stock != []:
                selected_stock = selected_product.stock[0]
                return {
                    'message': 'Add Stock Succesful',
                    'details': marshal(selected_stock, Stock.stock_fields)
                } , 200, {'Content-Type':'application/json'}
            # else stock not found
            return {'message': 'This porduct has no stock '}, 404, {'Content-Type':'application/json'}
        # else product not found
        return {'message': 'Product with specify product id not found'}, 404, {'Content-Type':'application/json'}
        

# JWT TESTING
class SellerTestJWT(Resource):
    @jwt_required
    def post(self):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        claims = marshal(claims, Seller.jwt_claim_fields)
        identity = get_jwt_identity()
        return {'claims' : claims, 'identity' : identity}, 200

api.add_resource(SellerCreateTokenResource, '/login')
api.add_resource(RegisterSeller, '/register')
api.add_resource(SellerInfoSelf, '/me')
api.add_resource(SellerEditSelf, '/edit')
api.add_resource(SellerProduct, '/product')
api.add_resource(SellerStockProduct, '/product/stock')


api.add_resource(SellerTestJWT, '/jwt')