import json, hashlib, logging
from . import client, create_token, reset_db
from password_strength import PasswordPolicy
from flask_jwt_extended import jwt_required, get_jwt_claims
from blueprints import db, admin_required, user_required, seller_required

class TestCustomer():
    reset_db
    # post register cust
    def test_valid_post_customer(self, client):
        token = create_token('user')
        data = {
            "username" : "bambi",
            "password" : "jg46!32B",
            "first_name" : "first",
            "last_name" : "last",
            "email" : "lalla@gmail.com"
        }
        
        res = client.post('/user/register', json=data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200
    def test_invalid_post_customer(self, client):
        token = create_token('user')
        data = {
            "username" : "bambs",
            "password" : "a!3",
            "first_name" : "first",
            "last_name" : "last",
            "email" : "lalla@gmail.com"
        }
        
        res = client.post('/user/register', json=data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 400

class TestEditSelef():
    reset_db
    # method put required all
    def test_valid_put_method(self, client):
        token = create_token('user')
        data = {
            "first_name" : "test123",
            "last_name" : "cobalagi",
            "password" : "asdfasdf",
            "email" : "edited@gmail.com"
        }
        
        res = client.put('/user/edit', json=data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200
    def test_invalid_put_method(self, client):
        token = create_token('user')
        data = {
            "first_name" : "test123",
            "last_name" : "cobalagi",
            "password" : "as",
            "email" : "edited@gmail.com"
        }
        
        res = client.put('/user/edit', json=data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 400
    
    # patch method only can edit 1 element
    def test_valid_patch_method(self, client):
        token = create_token('user')
        data = {
            "first_name" : "test123",
            "last_name" : "cobalagi",
            "password" : "as",
            "email" : "edited@gmail.com"
        }
        
        res = client.patch('/user/edit', json=data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200
    def test_valid_patch_method(self, client):
        token = create_token('user')
        data = {
            "first_name" : "test123",
            "last_name" : "cobalagi",
            "password" : "aasdfafs",
            "email" : "asdfadsf@gmail.com"
        }
        
        res = client.patch('/user/edit', json=data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

class TestCustomerSelf():
    reset_db()
    def test_valid_get_info_self(self, client):
        token = create_token('user')
        data = {
        }
        
        res = client.get('/user/me', json=data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

class TestGetProduct():
    reset_db()
    def test_valid_user_get_product_all(self, client):
        token = create_token('user')
        data = {
            "page" : 1,
            "limit" : 1,
            "order_by" : "id",
            "sort" : "asc",
            "name" : "bb cream"
        }
        res = client.get('/user/product', json=data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200
        
    def test_valid_user_get_product_all(self, client):
        token = create_token('user')
        data = {
            "page" : 1,
            "limit" : 1,
            "order_by" : "id",
            "sort" : "desc",
            "name" : "bb cream"
        }
        res = client.get('/user/product', json=data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_valid_user_get_product_all(self, client):
        token = create_token('user')
        data = {
            "page" : 1,
            "limit" : 1,
            "order_by" : "price",
            "sort" : "desc",
            "name" : "bb cream"
        }
        res = client.get('/user/product', json=data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_valid_get_info_self(self, client):
        token = create_token('user')
        data = {
            "page" : 1,
            "limit" : 1,
            "order_by" : "id",
            "sort" : "desc",
            "name" : "lalallalla"
        }
        res = client.get('/user/product', json=data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 404

class TestCustomerBag():
    reset_db()
    def test_valid_get_bag(self, client):
        token = create_token('user')
        data = {
        }
        res = client.get('/user/mybag', json=data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200
    # post product
    def test_validpost_bag(self, client):
        token = create_token('user')
        data = {
            "product_id" : 10,
            "amount" : 2
        }
        res = client.post('/user/mybag', json=data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200
    def test_validpost_bag(self, client):
        token = create_token('user')
        data = {
            "product_id" : 10,
            "amount" : -1
        }
        res = client.post('/user/mybag', json=data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_valid_patch_bag(self, client):
        token = create_token('user')
        data = {
            "product_id" : 10,
            "amount" : 4
        }
        res = client.patch('/user/mybag', json=data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_valid_patch_bag(self, client):
        token = create_token('user')
        data = {
            "product_id" : 99,
            "amount" : 4
        }
        res = client.patch('/user/mybag', json=data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_valid_delete_bag(self, client):
        token = create_token('user')
        data = {
            "product_id" : 10
        }
        res = client.delete('/user/mybag', json=data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

class TestCustomerAddress():
    reset_db()
    # post address
    def test_valid_input_address_bag(self, client):
        token = create_token('user')
        data = {
            "address_name" : "kantor",
            "address" : "jalan kantor no 45",
            "country" : "indonesia",
            "city" : "jembs",
            "postal_code" : "68133",
            "phone_number" : "0812312323"
        }
        res = client.post('/user/me/address', json=data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200
    def test_valid_input_address2_bag(self, client):
        token = create_token('user')
        data = {
            "address_name" : "taman",
            "address" : "jalan rumah no 45",
            "country" : "indonesia",
            "city" : "blablabla",
            "postal_code" : "68133",
            "phone_number" : "0812312323"
        }
        res = client.post('/user/me/address', json=data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_get_valid_address_bag(self, client):
        token = create_token('user')
        data = {
            "address_name" : "kampus"
        }
        res = client.get('/user/me/address', json=data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_get_valid_address2_bag(self, client):
        token = create_token('user')
        data = {

        }
        res = client.get('/user/me/address', json=data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_delete_addr(self, client):
        token = create_token('user')
        data = {
            "address_name" : "kampus"
        }
        res = client.get('/user/me/address', json=data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_delete_addr(self, client):
        token = create_token('user')
        data = {
            "address_name" : "lalalla"
        }
        res = client.get('/user/me/address', json=data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 404
    
    def test_add_order(self,client):
        token = create_token('user')
        data = {
            "address_name" : "rumah"
        }
        res = client.post('/user/order', json=data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_payment(self,client):
        token = create_token('user')
        data = {
            'payment_oid' : 2,
            'payment_type' : 'ovo'
        }
        res = client.post('/user/payment', json=data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

class TestJWT():
    def test_valid_get_jwt(self,client):
        token = create_token('user')
        data = {
        }
        res = client.post('/user/jwt', json=data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200