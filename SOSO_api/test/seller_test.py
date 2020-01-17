import json, hashlib, logging
from . import client, create_token, reset_db
from password_strength import PasswordPolicy
from flask_jwt_extended import jwt_required, get_jwt_claims
from blueprints import db, admin_required, user_required, seller_required

class TestRegisterSeller():
        def test_create_seller_valid(self,client):
            token = create_token('admin')
            data = {
                "username" : "maybelline-VS",
                "password" : "jg46!32B",
                "brand_name" : "maybelline",
                "email": "may@gmail.com"
            }
            res = client.post('/seller/register', json=data, headers={'Authorization': 'Bearer ' + token})
            res_json = json.loads(res.data)
            assert res.status_code == 200

        def test_create_seller_invalid(self,client):
            token = create_token('admin')
            data = {
                "username" : "senka-VS",
                "password" : "jg4",
                "brand_name" : "senka",
                "email": "sen@gmail.com"
            }
            res = client.post('/seller/register', json=data, headers={'Authorization': 'Bearer ' + token})
            res_json = json.loads(res.data)
            assert res.status_code == 400

class TestSellerSelf():

    def test_seller_get_self_valid(self,client):
        token = create_token('seller')
        data = {

        }
        res = client.get('/seller/me', json=data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
class TestSellerPostProduct():
    def test_seller_post_product(self,client):
        token = create_token('seller')
        data = {
            "department_id" : 1,
            "category_id": 1,
            "subcategory_id": 7,
            "name" : "toneup cream",
            "sub_name" : "shade beige",
            "price" : 36000,
            "discount" : 20
        }
        res = client.post('/seller/product', json=data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    # set stock after create product
    def test_seller_post_stock_add(self,client):
        token = create_token('seller')
        data = {
            "stock_pid" : 5,
            "qty_onupdate" : 10
        }
        res = client.post('/seller/product/stock', json=data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200
    def test_seller_post_stock_minus(self,client):
        token = create_token('seller')
        data = {
            "stock_pid" : 5,
            "qty_onupdate" : -1
        }
        res = client.post('/seller/product/stock', json=data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200
    def test_seller_get_stock_get_valid(self,client):
        token = create_token('seller')
        data = {
            "stock_pid" : 7,
        }
        res = client.get('/seller/product/stock', json=data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_seller_get_stock_get_invalid(self,client):
        token = create_token('seller')
        data = {
            "stock_pid" : 7,
        }
        res = client.get('/seller/product/stock', json=data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_seller_put_product(self,client):
        token = create_token('seller')
        data = {
            "id" : 11,
            "department_id" : 1,
            "category_id": 1,
            "subcategory_id": 7,
            "name" : "toneup cream",
            "sub_name" : "shade beige",
            "price" : 36000,
            "discount" : 20
        }
        res = client.put('/seller/product', json=data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200
    def test_seller_put_product_nodiscount(self,client):
        token = create_token('seller')
        data = {
            "id" : 11,
            "department_id" : 1,
            "category_id": 1,
            "subcategory_id": 7,
            "name" : "toneup cream",
            "sub_name" : "shade beige",
            "price" : 36000
        }
        res = client.put('/seller/product', json=data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_seller_put_product_invalid_id(self,client):
        token = create_token('seller')
        data = {
            "id" : 99,
            "department_id" : 1,
            "category_id": 1,
            "subcategory_id": 7,
            "name" : "toneup cream",
            "sub_name" : "shade beige",
            "price" : 36000
        }
        res = client.put('/seller/product', json=data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_seller_get_allproduct(self,client):
        token = create_token('seller')
        data = {

        }
        res = client.get('/seller/product', json=data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200
    def test_seller_get_product(self,client):
        token = create_token('seller')
        data = {
            "department_id" : 1,
            "name" : "toneup cream",
            "order_by" : "id",
            "page" : "1",
            "limit" : "10",
            "sort" : "asc"
        }
        res = client.get('/seller/product', json=data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200
    def test_seller_get_product(self,client):
        token = create_token('seller')
        data = {
            "department_id" : 1,
            "name" : "toneup cream",
            "order_by" : "id",
            "page" : "1",
            "limit" : "10",
            "sort" : "desc"
        }
        res = client.get('/seller/product', json=data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200
    def test_seller_get_product(self,client):
        token = create_token('seller')
        data = {
            "department_id" : 1,
            "name" : "toneup cream",
            "order_by" : "price",
            "page" : "1",
            "limit" : "10",
            "sort" : "desc"
        }
        res = client.get('/seller/product', json=data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200
    def test_seller_patch_product(self,client):
        token = create_token('seller')
        data = {
            "id" : 11,
            "name" : "toneup cream",
            "sub_name" : "shade beige",
            "price" : 36000,
            "discount" : 20
        }
        res = client.patch('/seller/product', json=data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_seller_delete_product_invalid(self,client):
        token = create_token('seller')
        data = {
            "id" : 99,
        }
        res = client.delete('/seller/product', json=data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_seller_delete_product_invalid(self,client):
        token = create_token('seller')
        data = {
            "id" : 99,
        }
        res = client.delete('/seller/product', json=data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 404

class TestJWT():
    def test_valid_get_jwt(self,client):
        token = create_token('seller')
        data = {
        }
        res = client.post('/seller/jwt', json=data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200
