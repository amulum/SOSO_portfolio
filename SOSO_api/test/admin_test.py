import json, hashlib, logging
from . import client, create_token, reset_db
from password_strength import PasswordPolicy
from flask_jwt_extended import jwt_required, get_jwt_claims
from blueprints import db, admin_required, user_required, seller_required

class TestAdminRegister():
    reset_db()
    # post client register
    def test_valid_register_admin(self, client):
        token = create_token('admin')
        data = {
            "username" : "bambangs",
            "password" : "jg46!32B"
        }
        res = client.post('/admin/register', json=data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)

        assert res.status_code == 200

    def test_invalid_register_admin_duplicate_admin(self, client):
        token = create_token('admin')
        data = {
            "username" : "admin",
            "password" : "jg46!32B"
        }
        res = client.post('/admin/register', json=data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)

        assert res.status_code == 500

    def test_invalid_register_admin(self, client):
        token = create_token('admin')
        data = {
            "username" : "yuyyum",
            "password" : "lalalla"
        }

        res = client.post('/admin/register', json=data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)

        assert res.status_code == 400

class AdminRootPath():
    reset_db()
    # get info admin by username
    def test_valid_alladmin_by_username(self, client):
        token = create_token('admin')
        data = {
            "username" : "admin"
        }
        res = client.get('/admin', json=data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)

        assert res.status_code == 200

    def test_invalid_alladmin_by_username(self, client):
        token = create_token('admin')
        data = {
            "username" : "lalallalla"
        }
        res = client.get('/admin', json=data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)

        assert res.status_code == 404

    def test_valid_get_alladmin(self, client):
        token = create_token('admin')
        data = {}
        res = client.get('/admin', json=data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)

        assert res.status_code == 200

    def test_delete_valid_admin(self, client):
        token = create_token('admin')
        data = {
            'username': 'admin',
        }
        res = client.delete('/admin', json=data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)

        assert res.status_code == 200

    def test_delete_invalid_admin(self, client):
        token = create_token('admin')
        data = {
            'username': 'saskeh',
        }
        res = client.delete('/admin', json=data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)

        assert res.status_code == 404

class TestAdminForSeller():

    # get seller
    def test_get_seller_success(self, client):
        token = create_token('admin')
        data = {
            'id': '1',
        }
        res = client.get('/admin/seller', json=data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)

        assert res.status_code == 200
    def test_get_seller_success(self, client):
        token = create_token('admin')
        data = {
            'username': 'brand2-VS',
        }
        res = client.get('/admin/seller', json=data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)

        assert res.status_code == 200
    def test_get_seller_success(self, client):
        token = create_token('admin')
        data = {
            'brand_name': 'emina',
        }
        res = client.get('/admin/seller', json=data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)

        assert res.status_code == 200
    def test_get_seller_failed(self, client):
        token = create_token('admin')
        data = {
            'username': 'lallala',
        }
        res = client.get('/admin/seller', json=data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)

        assert res.status_code == 404

    def test_get_allseller_success(self, client):
        token = create_token('admin')
        data = {
        }
        res = client.get('/admin/seller', json=data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)

        assert res.status_code == 200
    
    # delete seller
    def test_delete_seller_success(self, client):
        token = create_token('admin')
        data = {
            'id': '1',
        }
        res = client.delete('/admin/seller', json=data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_delete_seller_success(self, client):
        token = create_token('admin')
        data = {
            'username': 'brand2-VS',
        }
        res = client.delete('/admin/seller', json=data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_delete_seller_success(self, client):
        token = create_token('admin')
        data = {
            'brand_name': 'brand3',
        }
        res = client.delete('/admin/seller', json=data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_delete_seller_success(self, client):
        token = create_token('admin')
        data = {
            'brand_name': 'MAMAAMM',
        }
        res = client.delete('/admin/seller', json=data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 404

class TestAdminForCust():

    # get customer by id or username and all
    def test_get_seller_success(self, client):
        token = create_token('admin')
        data = {
            'id': '1',
        }
        res = client.get('/admin/user', json=data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)

        assert res.status_code == 200
    def test_get_seller_success(self, client):
        token = create_token('admin')
        data = {
            'username': 'kalila',
        }
        res = client.get('/admin/user', json=data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)

        assert res.status_code == 200

    def test_get_seller_failed(self, client):
        token = create_token('admin')
        data = {
            'username': 'lallala',
        }
        res = client.get('/admin/user', json=data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)

        assert res.status_code == 404

    def test_get_allseller_success(self, client):
        token = create_token('admin')
        data = {
        }
        res = client.get('/admin/seller', json=data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)

        assert res.status_code == 200
    
    # delete seller
    def test_delete_seller_success(self, client):
        token = create_token('admin')
        data = {
            'id': '1',
        }
        res = client.delete('/admin/user', json=data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_delete_seller_success(self, client):
        token = create_token('admin')
        data = {
            'username': 'cust2',
        }
        res = client.delete('/admin/user', json=data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_delete_seller_success(self, client):
        token = create_token('admin')
        data = {
            'username': 'MAMAAMM',
        }
        res = client.delete('/admin/user', json=data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 404
    
class AdminForProduct():
    def test_get_popular_item(self, client):
        token = create_token('admin')
        data = {
        }
        res = client.get('/admin/product', json=data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

