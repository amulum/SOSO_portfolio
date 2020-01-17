import pytest, json, logging, hashlib
from flask import Flask, request
from datetime import datetime
from blueprints import app, db
from app import cache
from blueprints.admin.model import *
from blueprints.bag.model import *
from blueprints.customer.model import *
from blueprints.items.model import *
from blueprints.seller.model import *



def call_client(request):
    client = app.test_client()
    return client

def reset_db():
    db.drop_all()
    db.create_all()

    # create admin
    admin_1 = Admin('yuyyum','a194fd6dd42d742b3fbca069e451dc7f')
    admin_3 = Admin('admin', hashlib.md5("admin".encode()).hexdigest())
    db.session.add(admin_1)
    db.session.add(admin_3)
    db.session.commit()

    # create seller
    seller_1 = Seller('brand1', 'brand1-VS',hashlib.md5("passwordaja".encode()).hexdigest(),'emailaja')
    seller_2 = Seller('brand2', 'brand2-VS',hashlib.md5("passwordaja".encode()).hexdigest(),'emailaja')
    seller_3 = Seller('brand3', 'brand3-VS',hashlib.md5("passwordaja".encode()).hexdigest(),'emailaja')
    seller_4 = Seller('brand4', 'brand4-VS',hashlib.md5("passwordaja".encode()).hexdigest(),'emailaja')
    seller_5 = Seller('emina', 'emina-VS',"a194fd6dd42d742b3fbca069e451dc7f",'emina@gmail.com')
    db.session.add(seller_1)
    db.session.add(seller_2)
    db.session.add(seller_3)
    db.session.add(seller_4)
    db.session.add(seller_5)
    db.session.commit()
    
    # create customer
    customer_1 = Customer('cust1',hashlib.md5("passwordaja".encode()).hexdigest(),'first', 'last','later' )
    customer_2 = Customer('cust2',hashlib.md5("passwordaja".encode()).hexdigest(),'first', 'last','later' )
    customer_3 = Customer('cust3',hashlib.md5("passwordaja".encode()).hexdigest(),'first', 'last','later' )
    customer_4 = Customer('cust4',hashlib.md5("passwordaja".encode()).hexdigest(),'first', 'last','later' )
    customer_5 = Customer('kalila','a194fd6dd42d742b3fbca069e451dc7f','kalila@gmail.com', 'last','later' )
    customer_6 = Customer('yuyyum','a194fd6dd42d742b3fbca069e451dc7f','yuyyum@gmail.com', 'last','later' )
    db.session.add(customer_1)
    db.session.add(customer_2)
    db.session.add(customer_3)
    db.session.add(customer_4)
    db.session.add(customer_5)
    db.session.add(customer_6)
    db.session.commit()
    
    # create department
    department_1 = Department('Makeup')
    department_2 = Department('Skincare')
    department_3 = Department('Haircare')
    department_4 = Department('Bath & Body')
    db.session.add(department_1)
    db.session.add(department_2)
    db.session.add(department_3)
    db.session.add(department_4)
    db.session.commit()

    # create category
    category_1 = Category(1, 'Face')
    category_2 = Category(1, 'Lips')
    category_3 = Category(2, 'Cleanser')
    category_4 = Category(2, 'Moisturizer')
    category_5 = Category(3, 'Shampoo')
    category_6 = Category(3, 'Hair Treatment')
    category_7 = Category(4, 'Cleanser')
    category_8 = Category(4, 'Moisturizer')
    db.session.add(category_1)
    db.session.add(category_2)
    db.session.add(category_3)
    db.session.add(category_4)
    db.session.add(category_5)
    db.session.add(category_6)
    db.session.add(category_7)
    db.session.add(category_8)
    db.session.commit()

    # create sub-category
    sub_1 = Subcategory(1,1, 'Foundation')
    sub_2 = Subcategory(1,1, 'Primer')
    sub_3 = Subcategory(1,1, 'Concealer')
    sub_4 = Subcategory(1,1, 'Bronzer')
    sub_5 = Subcategory(1,1, 'Loose Powder')
    sub_6 = Subcategory(1,1, 'BB & CC Cream')
    sub_7 = Subcategory(1,2, 'Lipstick')
    sub_8 = Subcategory(1,2, 'Lip Gloss')
    sub_9 = Subcategory(1,2, 'Lip Primer')
    sub_10 = Subcategory(1,2, 'Lip Balm')
    sub_11 = Subcategory(2,1, 'Cleanser')
    sub_12 = Subcategory(2,1, 'Cleansing Oil')
    sub_13 = Subcategory(2,1, 'Toner')
    sub_14 = Subcategory(2,1, 'Makeup Remover')
    sub_15 = Subcategory(2,2, 'Moisturizer')
    sub_16 = Subcategory(2,2, 'Face Oil')
    sub_17 = Subcategory(3,1, 'Shampoo')
    sub_18 = Subcategory(3,1, 'Dry Shampoo')
    sub_19 = Subcategory(3,1, 'Conditioner')
    sub_20 = Subcategory(3,2, 'Hair Mask')
    sub_21 = Subcategory(3,2, 'Hair Serum')
    sub_22 = Subcategory(3,2, 'Hair Oil')
    sub_23 = Subcategory(3,2, 'Hair Ampule')
    sub_24 = Subcategory(4,1, 'Body Wash & Gel')
    sub_25 = Subcategory(4,1, 'Body Scrub & Exfo')
    sub_26 = Subcategory(4,2, 'Body Lotion & Oil')
    sub_27 = Subcategory(4,2, 'Hand & Foot Cream')
    db.session.add(sub_1)
    db.session.add(sub_2)
    db.session.add(sub_3)
    db.session.add(sub_4)
    db.session.add(sub_5)
    db.session.add(sub_6)
    db.session.add(sub_7)
    db.session.add(sub_8)
    db.session.add(sub_9)
    db.session.add(sub_10)
    db.session.add(sub_11)
    db.session.add(sub_12)
    db.session.add(sub_13)
    db.session.add(sub_14)
    db.session.add(sub_15)
    db.session.add(sub_16)
    db.session.add(sub_17)
    db.session.add(sub_18)
    db.session.add(sub_19)
    db.session.add(sub_20)
    db.session.add(sub_21)
    db.session.add(sub_22)
    db.session.add(sub_23)
    db.session.add(sub_24)
    db.session.add(sub_25)
    db.session.add(sub_26)
    db.session.add(sub_27)
    db.session.commit()

    # create product
    item_1 = Product(1,1,1, 'Fit Me! Matte Foundation', 'Fit Me! Matte Foundation', 149000, 40, 89400, 1)
    item_2 = Product(1,1,1, 'Radiance Foundation', 'Radiance Foundation', 149000, 0, 149000, 1)
    item_3 = Product(1,1,1, 'Stay matte not Flat', 'Stay matte not Flat', 160000, 30, 112000, 1)
    item_4 = Product(4,1,24, 'Baby Daily Lotion', 'Shower Gel Lavender', 160000, 0, 160000, 1)
    item_5 = Product(4,1,24, 'Experience Body Foam', 'Baby Bath & Wash', 52000, 50, 26000, 3)
    item_6 = Product(1,1,6, 'BB Cream Beauty Bliss Natural', 'Natural Shade', 26000, 10, 23400, 5)
    item_7 = Product(1,1,6, 'BB Cream Beauty Bliss Light', 'Light Shade', 26000, 10, 23400, 5)
    item_8 = Product(1,1,6, 'BB Cream Beauty Bliss Caramel', 'Caramel Shade', 26000, 10, 23400, 5)
    item_9 = Product(2,1,1, 'Ms Pimple Moist Gel', 'Moist Gel', 50000, 40, 30000, 5)
    item_10 = Product(2,1,3, 'Ms Pimple Face Tonic', 'Face Tonic', 50000, 40, 30000, 5)
    db.session.add(item_1)
    db.session.add(item_2)
    db.session.add(item_3)
    db.session.add(item_4)
    db.session.add(item_5)
    db.session.add(item_6)
    db.session.add(item_7)
    db.session.add(item_8)
    db.session.add(item_9)
    db.session.add(item_10)
    db.session.commit()

    # create customer bag
    bag_1 = MyBag(6)
    bag_2 = MyBag(3)
    bag_3 = MyBag(2)
    bag_4 = MyBag(5)
    bag_5 = MyBag(6)
    db.session.add(bag_1)
    db.session.add(bag_2)
    db.session.add(bag_3)
    db.session.add(bag_4)
    db.session.add(bag_5)
    db.session.commit()

    # create bagdetails
    bagdetails_1 = MyBagDetails(1,6,1)
    bagdetails_2 = MyBagDetails(1,7,2)
    bagdetails_3 = MyBagDetails(2,6,1)
    bagdetails_4 = MyBagDetails(2,7,2)
    bagdetails_5 = MyBagDetails(2,8,3)
    bagdetails_6 = MyBagDetails(3,6,1)
    bagdetails_7 = MyBagDetails(3,7,2)
    bagdetails_8 = MyBagDetails(3,8,3)
    bagdetails_9 = MyBagDetails(4,6,1)
    bagdetails_10 = MyBagDetails(4,7,2)
    bagdetails_11 = MyBagDetails(4,8,2)
    bagdetails_12 = MyBagDetails(4,9,6)
    db.session.add(bagdetails_1)
    db.session.add(bagdetails_2)
    db.session.add(bagdetails_3)
    db.session.add(bagdetails_4)
    db.session.add(bagdetails_5)
    db.session.add(bagdetails_6)
    db.session.add(bagdetails_7)
    db.session.add(bagdetails_8)
    db.session.add(bagdetails_9)
    db.session.add(bagdetails_10)
    db.session.add(bagdetails_11)
    db.session.add(bagdetails_12)
    db.session.commit()

    # Shipping Address
    shipping_1 = ShippingAddress('rumah', 6, 'jalan mawar', 'indonesia','jembs', '68123', '08123123')
    shipping_2 = ShippingAddress('kampus', 6, 'jalan kampus', 'indonesia','jembs', '68123', '08123123')
    db.session.add(shipping_1)
    db.session.add(shipping_2)
    db.session.commit()

    # order
    order_1 = Order(6,1,datetime.now())
    ordetail_1 = OrderDetails(1,6,1)
    db.session.add(order_1)
    db.session.add(ordetail_1)
    db.session.commit()

    #stock
    stock_1 = Stock(1,0,10,datetime.now(),10)
    stock_2 = Stock(2,0,10,datetime.now(),10)
    stock_3 = Stock(3,0,10,datetime.now(),10)
    stock_4 = Stock(4,0,10,datetime.now(),10)
    stock_5 = Stock(5,0,10,datetime.now(),10)
    stock_6 = Stock(6,0,10,datetime.now(),10)
    stock_7 = Stock(7,0,10,datetime.now(),10)
    stock_8 = Stock(8,0,10,datetime.now(),10)
    stock_9 = Stock(9,0,10,datetime.now(),10)
    db.session.add(stock_1)
    db.session.add(stock_2)
    db.session.add(stock_3)
    db.session.add(stock_4)
    db.session.add(stock_5)
    db.session.add(stock_6)
    db.session.add(stock_7)
    db.session.add(stock_8)
    db.session.add(stock_9)
    db.session.commit()

@pytest.fixture
def client(request):
    return call_client(request)

# create token for 3 different type user
def create_token(person):
    if person =='admin':
        cachename = "test-admin-token"
        data = {
            'username': 'yuyyum',
            'password': 'jg46!32B'
        }

    elif person == 'seller':
        cachename = "test-seller-token"
        data = {
            'username': 'brand3-VS',
            'password': 'passwordaja'
        }

    else:
        cachename = "test-user-token"
        data = {
            'username': 'yuyyum',
            'password': 'jg46!32B'
        }

    token = cache.get(cachename)

    if token is None:
        # Do Request
        req = call_client(request)
        if person =='admin': res = req.post('/admin/login', json = data, content_type='application/json')
        elif person =='seller': res = req.post('/seller/login', json = data, content_type='application/json')
        else: res = req.post('/user/login', json = data, content_type='application/json')

        # Store Response
        res_json = json.loads(res.data)

        logging.warning('RESULT : %s', res_json)

        # Assertion
        assert res.status_code == 200

        # Save token into cache
        cache.set(cachename, res_json['token'], timeout = 60)

        # Return, because it is useful for other test
        return res_json['token']
    return token