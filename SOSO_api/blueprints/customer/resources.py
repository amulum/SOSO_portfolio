# CUSTOMER RESOURCES #
# contain: login authentication, get self profile, register user/customer, edit some editable field


# import flask
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from blueprints import app, db, user_required, admin_required   
# import jwt
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_claims
# import model
from .model import *
from ..items.model import *
from ..bag.model import *
# Password Encription
from password_strength import PasswordPolicy
import hashlib
from sqlalchemy import desc
from datetime import datetime


# Creating blueprint
bp_customer = Blueprint('customer', __name__)
api = Api(bp_customer)

# CUSTOMER a.k.a. USER LOGIN

# CREATE TOKEN FOR REGISTERED CUSTOMER


class CustomerCreateTokenResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', location='json', required=True)
        parser.add_argument('password', location='json', required=True)
        args = parser.parse_args()
        password_digest = hashlib.md5(args['password'].encode()).hexdigest()
        # CUSTOMER
        qry = Customer.query
        selected_cust = qry.filter_by(username=args['username']).filter_by(
            password=password_digest).first()
        # set identity and user_claims seller can be used later
        if selected_cust:
            token = create_access_token(identity='CUSTOMER', user_claims={
                'id': selected_cust.id, 'username': args['username']})
            return {'token': token}, 200
        return {'status': 'FAILED', 'message': 'PLEASE CHECK USERNAME OR PASSWORD'}, 403
    # handshake
    def options(self):
        return {}, 200


# REGISTER NEW CUSTOMER OPEN FOR PUBLIC
class RegisterCustomer(Resource):
    # handshake
    def options(self):
        return {}, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', location='json', required=True)
        parser.add_argument('password', location='json', required=True)
        parser.add_argument('first_name', location='json', required=True)
        parser.add_argument('last_name', location='json', required=True)
        parser.add_argument('email', location='json', required=True)
        args = parser.parse_args()

        # Setup the policy
        policy = PasswordPolicy.from_names(
            length=8
        )
        # Validating the password policy
        validation = policy.test(args['password'])

        if validation == []:
            password_digest = hashlib.md5(
                args['password'].encode()).hexdigest()
            # Creating object
            new_cust = Customer(username=args['username'], password=password_digest,
                                first_name=args['first_name'], last_name=args['last_name'], email=args['email'])
            db.session.add(new_cust)
            db.session.commit()

            app.logger.debug('DEBUG : %s', new_cust)

            return {'message': 'New Customer Created!!!', 'Detail': marshal(new_cust, Customer.customer_fields)}, 200, {'Content-Type': 'application/json'}
        return {'status': 'FAILED', 'message': 'PLEASE ENTER PASSWORD WITH SPECIFIC FORMAT'}, 400


# CUSTOMER METHOD FOR EDIT SELF
class CustomerEditSelf(Resource):
    # handshake
    def options(self):
        return {}, 200

    # put method must input all argument except username
    @user_required
    def put(self):
        claims = get_jwt_claims()
        parser = reqparse.RequestParser()
        parser.add_argument('password', location='json', required=True)
        parser.add_argument('first_name', location='json', required=True)
        parser.add_argument('last_name', location='json', required=True)
        parser.add_argument('email', location='json', required=True)
        args = parser.parse_args()

        policy = PasswordPolicy.from_names(
            length=8
        )
        # Validating the password policy
        validation = policy.test(args['password'])

        if validation == []:
            password_digest = hashlib.md5(
                args['password'].encode()).hexdigest()
            # search selected cust
            qry = Customer.query
            selected_cust = qry.filter_by(id=claims['id']).first()
            # edit each elemen
            selected_cust.password = password_digest
            selected_cust.email = args['email']
            selected_cust.first_name = args['first_name']
            selected_cust.last_name = args['last_name']
            db.session.commit()

            app.logger.debug('DEBUG : %s', selected_cust)

            return {'message': 'Your profile UPDATED!', 'Detail': marshal(selected_cust, Customer.customer_fields)}, 200, {'Content-Type': 'application/json'}

        # password format doesnt match to policy
        return {'status': 'FAILED', 'message': 'PLEASE ENTER PASSWORD WITH SPECIFIC FORMAT'}, 400

    @user_required
    def patch(self):
        claims = get_jwt_claims()
        parser = reqparse.RequestParser()
        parser.add_argument('password', location='json')
        parser.add_argument('first_name', location='json')
        parser.add_argument('last_name', location='json')
        parser.add_argument('email', location='json')
        args = parser.parse_args()

        policy = PasswordPolicy.from_names(
            length=8
        )

        # search selected cust
        qry = Customer.query
        selected_cust = qry.filter_by(id=claims['id']).first()

        # edit per elemen if its not none
        if args['email']:
            selected_cust.email = args['email']
        if args['first_name']:
            selected_cust.first_name = args['first_name']
        if args['last_name']:
            selected_cust.last_name = args['last_name']
        if args['password']:
            validation = policy.test(args['password'])
            # Validating the password policy
            if validation == []:
                password_digest = hashlib.md5(
                    args['password'].encode()).hexdigest()
                selected_cust.password = password_digest

        db.session.commit()
        app.logger.debug('DEBUG : %s', selected_cust)

        return {'message': 'Your profile UPDATED!', 'Detail': marshal(selected_cust, Customer.customer_fields)}, 200, {'Content-Type': 'application/json'}



# CUSTOMER METHOD FOR GET INFO ABOUT SELF
class CustomerInfoSelf(Resource):
    # handshake
    def options(self):
        return {}, 200

    @user_required
    def get(self):
        qry = Customer.query
        claims = get_jwt_claims()
        selected_cust = qry.filter_by(username=claims['username']).first()

        app.logger.debug('DEBUG : %s', selected_cust)

        return marshal(selected_cust, Customer.customer_fields), 200, {'Content-Type': 'application/json'}


# GET PRODUCT ALL BY CUSTOMER
class CustomerGetProduct(Resource):
    # user or customer only can get product by name or get by department name
    # next feature affilate user can get item by department, cate, and sub cate
        # handshake
    def options(self):
        return {}, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', location='json')
        parser.add_argument('page', location='json', default = 1)
        parser.add_argument('limit', location='json', default = 10)
        parser.add_argument("order_by", location="json", help="invalid order-by value", choices=("id", "price"))
        parser.add_argument("sort", location="json", help="invalid sort value", choices=("desc","asc"))
        parser.add_argument('name', location='json')
        args = parser.parse_args()
        qry = Product.query

        # args name filled
        if args['name']:
            qry = qry.filter(Product.name.contains(args['name']))
        # args id filled
        if args['id']:
            qry = qry.filter_by(id=args['id'])
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
                marshal_product = (
                    marshal(lst_product[index], Product.cust_fields))
                format_product = {
                    'Product': index+1,
                    'Details': marshal_product
                }
                product_result.append(format_product)

            app.logger.debug('DEBUG : %s', product_result)
            # pagination format
            return {
                'page': args['page'],
                'limit_per_page': args['limit'],
                'result': product_result
            }, 200, {'Content-Type': 'application/json'}
        # product not found
        return {'message': 'Product Not Found'}, 404, {'Content-Type': 'application/json'}

# BAG METHOD FOR CUSTOMER
class CustomerBag(Resource):
    # handshake
    def options(self):
        return {}, 200

    # post an item to bag
    # automatically create my bag and create my bag details
    @user_required
    def get(self):
        claims = get_jwt_claims()
        parser = reqparse.RequestParser()
        parser.add_argument('page', location='json', default=1)
        parser.add_argument('limit', location='json', default=5)
        args = parser.parse_args()
        bag_user = MyBag.query.filter_by(customer_id=claims['id']).first()
        print(bag_user)
        if bag_user == None:
            selected_bag = MyBag(customer_id=claims['id'])
            db.session.add(selected_bag)
            db.session.commit()
        else:
            selected_bag = bag_user
        
        # case no product in bag
        if selected_bag.details.all() == []:
            return {'status' : 'Bag was there but no details'}, 200, {'Content-Type': 'application/json'}
        
        # CASE there is product in bag
        # aggregate sub_total and total items
        sub_total = 0
        total_items = 0
        for detail in selected_bag.details.all():
            total_items += detail.amount
            sub_total += detail.amount * detail.product.sell_price
        # pagination
        offset = (int(args["page"]) - 1)*int(args["limit"])
        lst_details = selected_bag.details.limit(
            int(args['limit'])).offset(offset).all()

        # response json format for better experience
        result_details = []
        for detail in lst_details:
            selected_product = detail.product  # no need to .all() only 1 item bcs one to one
            marshal_product = marshal(selected_product, Product.cust_fields)
            marshal_product['qty_item'] = detail.amount
            result_details.append(marshal_product)

        bag_format = {
            'page': args['page'],
            'per_page': args['limit'],
            'bag_info': marshal(selected_bag, MyBag.mybag_fields),
            'total_item': total_items,
            'sub_total': sub_total,
            'details': result_details
        }
        return bag_format, 200, {'Content-Type': 'application/json'}

    @user_required
    def post(self):
        claims = get_jwt_claims()
        parser = reqparse.RequestParser()
        parser.add_argument('product_id', location='json', required=True)
        parser.add_argument('amount', location='json', required=True)
        args = parser.parse_args()
        # cek bag udah ada blm kalo blm create dulu kalo udah ada lanjut ke add product+ amount
        bag_user = MyBag.query.filter_by(customer_id=claims['id']).first()
        if bag_user == None:
            # create new bag if user/customer doesnt have bag
            selected_bag = MyBag(customer_id=claims['id'])
            db.session.add(selected_bag)
            db.session.commit()
        else:
            # return same variable for simplified code and reset updated_at
            bag_user.updated_at = datetime.now()
            selected_bag = bag_user

        # check product id, when it fails return product not found
        selected_product = Product.query.filter_by(
            id=args['product_id']).first()
        if selected_product:
            # check input product id in bag or not, if it does
            isproduct_inbag = selected_bag.details.filter_by(
                product_id=args['product_id']).first()
            if isproduct_inbag:
                # just add current amount with input amount
                if int(isproduct_inbag.amount) + int(args['amount']) == 0:
                    # delete product in bag
                    delete_product = MyBagDetails.query.filter_by(product_id=args['product_id']).filter_by(mybag_id=selected_bag.id).first() 
                    db.session.delete(delete_product)
                    db.session.commit()
                # else add qty product
                isproduct_inbag.amount = int(
                    isproduct_inbag.amount) + int(args['amount'])
            else:
                new_details = MyBagDetails(
                    mybag_id=selected_bag.id, product_id=args['product_id'], amount=args['amount'])
                db.session.add(new_details)
            # commit change
            db.session.commit()
        else:
            return {'message': 'Product Not Found'}, 404, {'Content-Type': 'application/json'}

        # query all details in selected_bag
        lst_details = selected_bag.details.all()
        result_details = []
        sub_total = 0
        total_items = 0
        for detail in lst_details:
            selected_product = detail.product  # no need to .all() only 1 item bcs one to one
            marshal_product = marshal(selected_product, Product.cust_fields)
            marshal_product['qty_item'] = detail.amount
            total_items += detail.amount
            sub_total += detail.amount * detail.product.sell_price
            result_details.append(marshal_product)

        # for readable
        bag_format = {
            'bag_info': marshal(selected_bag, MyBag.mybag_fields),
            'total_item(s)': total_items,
            'sub_total': sub_total,
            'details': result_details
        }
        return bag_format, 200, {'Content-Type': 'application/json'}

    # edit amout of my bag details with input product id
    @user_required
    def patch(self):
        claims = get_jwt_claims()
        parser = reqparse.RequestParser()
        parser.add_argument('product_id', location='json', required=True)
        parser.add_argument('amount', location='json', required=True)
        args = parser.parse_args()
        # query get customer's bag
        selected_bag = MyBag.query.filter_by(customer_id=claims['id']).first()

        selected_details = selected_bag.details.filter_by(
            product_id=args['product_id']).first()
        if selected_details:
            selected_details.amount = args['amount']
            db.session.commit()
            return {'message': 'Update MyBag Succesful!'}, 200, {'Content-Type': 'application/json'}
        # true next step, else return not found
        return {'message': 'Product Not Found in My Bag'}, 404, {'Content-Type': 'application/json'}

    # use db relationship in my bag to remove bag item with spesific product id
    @user_required
    def delete(self):
        claims = get_jwt_claims()
        parser = reqparse.RequestParser()
        parser.add_argument('product_id', location='json', required=True)
        args = parser.parse_args()
        # query get customer's bag
        selected_bag = MyBag.query.filter_by(customer_id=claims['id']).first()

        selected_details = selected_bag.details.filter_by(
            product_id=args['product_id']).first()
        if selected_details:
            db.session.delete(selected_details)
            db.session.commit()
            return {'message': 'Update MyBag Succesful!'}, 200, {'Content-Type': 'application/json'}
        # true next step, else return not found
        return {'message': 'Product Not Found in MyBag'}, 404, {'Content-Type': 'application/json'}
class CustomerAddressCheckout(Resource):
  # handshake
  def options(self):
    return {}, 200

  @user_required
  def post(self):
    claims = get_jwt_claims()
    parser = reqparse.RequestParser()
    parser.add_argument('name', location='json')
    args = parser.parse_args()

    qry = ShippingAddress.query
    qry = qry.filter_by(address_cid= claims['id']) #filter by id get all address
    if args['name']: qry = qry.filter_by(address_name= args['name']) #filter by address name
    selected_address = qry.all()
    result_addr = []
    if selected_address:
        # loop for all selected address
        for address in selected_address:
            result_addr.append(marshal(address, ShippingAddress.customer_fields))

        return result_addr, 200, {'Content-Type': 'application/json'}

    return {'status': 'address not found'}, 404, {'Content-Type': 'application/json'}
class CustomerAddress(Resource):
    def options(self):
      return {}, 200

    @user_required
    def post(self):
        claims = get_jwt_claims()
        parser = reqparse.RequestParser()
        parser.add_argument('address_name', location='json', required=True)
        parser.add_argument('address', location='json', required=True)
        parser.add_argument('country', location='json', required=True)
        parser.add_argument('city', location='json', required=True)
        parser.add_argument('postal_code', location='json', required=True)
        parser.add_argument('phone_number', location='json', required=True)
        args = parser.parse_args()

        qry = ShippingAddress.query
        qry = qry.filter_by(address_cid= claims['id']) #filter by id 
        qry = qry.filter_by(address_name= args['address_name']) #filter by address name
        selected_address = qry.first()
        print(selected_address)
        if selected_address is None:
            # create new addr
            new_addr = ShippingAddress(
                address_name= args['address_name'],
                address_cid= claims['id'],
                address= args['address'],
                country= args['country'],
                city= args['city'],
                postal_code= args['postal_code'],
                phone_number= args['phone_number'])
            db.session.add(new_addr)
            db.session.commit()

            return marshal(new_addr, ShippingAddress.customer_fields), 200, {'Content-Type': 'application/json'}

        return {
            'status': 'address already exist',
            'details' : marshal(selected_address, ShippingAddress.customer_fields)},400, {'Content-Type': 'application/json'}

    @user_required
    def delete(self):
        claims = get_jwt_claims()
        parser = reqparse.RequestParser()
        parser.add_argument('address_name', location='json', required=True)
        args = parser.parse_args()

        qry = ShippingAddress.query
        qry = qry.filter_by(address_cid= claims['id']) #filter by id 
        qry = qry.filter_by(address_name= args['address_name']) #filter by address name
        selected_address = qry.first()
        print(selected_address)
        if selected_address:
            db.session.delete(selected_address)
            db.session.commit()
            print(selected_address)
            return {
                'status' : 'Shipping Address deleted',
                'details' : marshal(selected_address, ShippingAddress.customer_fields)
            }, 200, {'Content-Type': 'application/json'}

        return 'address not found', 404, {'Content-Type': 'application/json'}

    def options(self):
        return {}, 200

# CUSTOMER CREATE ORDER FROM BAG LIST
class CustomerOrder(Resource):
    # handshake
    def options(self):
        return {}, 200

    # use product id from bag to order
    # input claims and bag id
    # check stock
    # then create order,  add and commit
    @user_required
    def post(self):
        claims = get_jwt_claims()
        parser = reqparse.RequestParser()
        parser.add_argument('name', location='json', required=True)
        args = parser.parse_args()

        qry = ShippingAddress.query
        qry = qry.filter_by(address_cid= claims['id']) #filter by id 
        selected_addr = qry.filter_by(address_name= args['name']).first()#filter by address name
        if selected_addr == None:
            return {'status': 'order failed address required'}, 400, {'Content-Type': 'application/json'}
        selected_bag = MyBag.query.filter_by(customer_id=claims['id']).first()
        # 2 case
        # 1 order from bag
        if selected_bag:
            # create new order
            new_order = Order(
                order_cid=claims['id'],
                order_addrid=selected_addr.id,
                issue_date=datetime.now())
            db.session.add(new_order)
            db.session.commit()

            # loop for every product in bag create new details 
            selected_details = selected_bag.details.all()
            if selected_details:
                for detail in selected_details:
                    # createnew order details
                    new_order_details = OrderDetails(
                        ordetails_oid=claims['id'],
                        ordetails_pid=detail.product.id,
                        quantity=detail.amount)
                    db.session.add(new_order_details)
                    db.session.commit()

                    # delete details on bag
                    delete_detail = MyBagDetails.query.filter_by(id=detail.id).first()
                    db.session.delete(delete_detail)
                    db.session.commit()
                
                return 'order created', 200
        return 'bag not found', 404
            
        # 2 order from item direct cooming soon
        # get bag
        

    # get all order by self
    @user_required
    def get(self):
        claims = get_jwt_claims()
        qry = Order.query
        selected_order = qry.filter_by(order_cid=claims['id']).all()
        result_order = []
        if selected_order != []:
            for order in selected_order:
                marshal_order = marshal(order, Order.customer_fields)
                marshal_order['details'] = []
                details = OrderDetails.query.filter_by(ordetails_oid=order.id).all()
                if details != []:
                    # total = sum of all sell price in order
                    total = 0
                    print(details)    
                    for detail in details:
                        format_details = {}
                        format_details['product_name'] = detail.product.name
                        format_details['product_quantity'] = int(detail.quantity)
                        format_details['product_price'] = int(detail.product.sell_price)
                        format_details['sub_total'] = int(detail.product.sell_price) * int(detail.quantity)
                        total += format_details['sub_total']
                        marshal_order['details'].append(format_details)
                    marshal_order['total'] = total
                    return marshal_order, 200, {'Content-Type': 'application/json'}
        return {'status' : 'bad request'}, 400, {'Content-Type': 'application/json'}

# after create order page and confirm address go to payment page
class CustomerPayment(Resource):
    # handshake
    def options(self):
        return {}, 200
    # 
    @user_required
    def post(self):
        claims = get_jwt_claims()
        parser = reqparse.RequestParser()
        parser.add_argument('payment_oid', location='json', required=True)
        parser.add_argument('payment_type', location='json', choices=('ovo', 'dana', 'bank'), required=True)
        args = parser.parse_args()

        # get amount
        qry = OrderDetails.query
        selected_orderdetail = qry.filter_by(ordetails_oid= args['payment_oid']).all()
        # get total amount from payment oid
        calc_amount = 0
        for detail in selected_orderdetail:
            calc_amount += int(detail.product.sell_price) * int(detail.quantity)
        print(calc_amount)
        new_payment = Payment(
            payment_oid= args['payment_oid'],
            payment_type= args['payment_type'],
            issue_date= datetime.now(),
            amount= calc_amount,
            is_paid= False
        )
        return marshal(new_payment, Payment.admin_fields), 200, {'Content-Type': 'application/json'}

class CustomerResourceForPopular(Resource):
    def options(self):
        return {}, 200

    # get popular item
    def get(self):
        dum = db.session.query(MyBagDetails.product_id, db.func.count(MyBagDetails.id)).group_by(MyBagDetails.product_id).order_by(desc(db.func.count(MyBagDetails.id))).first()

        count_product = db.func.count(MyBagDetails.id)
        product_id = MyBagDetails.product_id
        qry = db.session.query(product_id, count_product).group_by(product_id).order_by(desc(count_product)).first()
        result_pid = qry[0]
        selected_product = Product.query.filter_by(id=result_pid).limit(5).all()
        print(selected_product)
        result_popular = []
        for select in selected_product:
            print(select)
            print(marshal(select, Product.cust_fields))
            popular_item = {
                'Popular Item' : f'Product ID {result_pid}',
                'details' : marshal(select, Product.cust_fields)
            }
            result_popular.append(popular_item)
        
        return result_popular, 200, {'Content-Type':'application/json'}

# CUSTOMER TEST CLAIMS
class CustomerTestJWT(Resource):
    # handshake
    def options(self):
        return {}, 200

    @jwt_required
    def post(self):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        claims = marshal(claims, Customer.jwt_claim_fields)
        identity = get_jwt_identity()
        return {'claims': claims, 'identity': identity}, 200



# CUSTOMER PATH /USER/....
api.add_resource(CustomerCreateTokenResource, '/login')
api.add_resource(RegisterCustomer, '/register')
api.add_resource(CustomerAddressCheckout, '/address')
api.add_resource(CustomerInfoSelf, '/me')
api.add_resource(CustomerAddress, '/me/address')
api.add_resource(CustomerEditSelf, '/edit')
api.add_resource(CustomerBag, '/mybag')
api.add_resource(CustomerGetProduct, '/product')
api.add_resource(CustomerOrder, '/order')
api.add_resource(CustomerPayment, '/payment')
api.add_resource(CustomerResourceForPopular, '/product/popular')


api.add_resource(CustomerTestJWT, '/jwt')
