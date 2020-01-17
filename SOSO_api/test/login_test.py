import json, hashlib, logging
from . import client, create_token, reset_db
from password_strength import PasswordPolicy
from flask_jwt_extended import jwt_required, get_jwt_claims
from blueprints import db, admin_required, user_required, seller_required

class TestLoginAll():
    reset_db()

    def test_login_admin_valid(self,client):
        data = {
            "username": "yuyyum",
            "password": "jg46!32B"
        }

        res = client.post('/admin/login', json = data)
        res_json = json.loads(res.data)

        assert res.status_code == 200
    
    
    def test_login_admin_invalid(self,client):
        data = {
            "username": "yuyyum",
            "password": "lalalala"
        }

        res = client.post('/admin/login', json = data)
        res_json = json.loads(res.data)

        assert res.status_code == 403
    
    def test_login_seller_valid(self, client):
        data = {
            "username": "emina-VS",
            "password": "jg46!32B"
        }

        res = client.post('/seller/login', json = data)
        res_json = json.loads(res.data)

        assert res.status_code == 200
    
    def test_login_seller_invalid(self, client):
        data = {
            "username": "emina-VS",
            "password": "lalalla"
        }
        token = create_token('admin')
        print('oke')
        res = client.post('/seller/login', json = data)
        res_json = json.loads(res.data)

        assert res.status_code == 403
    
    def test_login_seller_valid(self, client):
        data = {
            "username": "kalila",
            "password": "jg46!32B"
        }

        res = client.post('/user/login', json = data)
        res_json = json.loads(res.data)

        assert res.status_code == 200

    def test_login_seller_invalid(self, client):
        data = {
            "username": "kalila",
            "password": "lalalla"
        }

        res = client.post('/user/login', json = data)
        res_json = json.loads(res.data)

        assert res.status_code == 403
    