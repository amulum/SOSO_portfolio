# # API RAJAONGKIR
# # 5adabb9084eaaa0a1bd1e165a7133333
# # Cek province return list province by can filter by contains name
# # Cek city return list city by can filter by contains name
# # cek postal code selected province & city
# # cek ongkir, origin already set
# # province city dan postal code akan di aplikasikan saat di form register address dan input address baru

# # import flask
# from flask import Blueprint, jsonify
# from flask_restful import Api, Resource, reqparse, marshal
# from blueprints import app, db, seller_required, admin_required
# from sqlalchemy import literal, desc, asc

# from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims
# from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_claims
# # import model
# from .model import Seller
# from ..items.model import *
# import http.client
# import requests

# bp_ongkir = Blueprint('ongkir', __name__)
# api = Api(bp_ongkir)


# class RajaOngkir(Resource):
#     # rajaongkir
#     ro_apikey = 'beec6b243c70c0c15332859c0d12a107'
#     ro_host = 'https://api.rajaongkir.com/starter'
#     @admin_required
#     def get(self):
#         parser = reqparse.RequestParser()
#         parser.add_argument('id', location='json', default=None)
#         parser.add_argument('input', location='json', help='city or province', choices=(
#             'city', 'province'), required=True)
#         parser.add_argument('province', location='json',
#                             help='input province id', default=None)
#         args = parser.parse_args()

#         rq = requests.get(self.ro_host + '/' + args['input'], params={
#                           'id': args['id'], 'province': args['province'], 'key': self.ro_apikey})

#         if args['input'] == 'province':
#             # test selected province id return only province name
#             if args['id']:
#                 return rq.json()['rajaongkir']['results']['province']
#             # return result province with id
#             lst_province_withid = rq.json()['rajaongkir']['results']
#             return lst_province_withid

#         elif args['input'] == 'city':
#             # return all city detail
#             lst_citydetail = rq.json()['rajaongkir']['results']
#             return lst_citydetail

#     @admin_required
#     def post(self):
#         parser = reqparse.RequestParser()
#         parser.add_argument('origin', location='json',
#                             help='id kabupaten/kota', required=True)
#         parser.add_argument('destination', location='json',
#                             help='id kabupaten/kota', required=True)
#         parser.add_argument('weight', location='json',
#                             help='input dalam kg', required=True)
#         parser.add_argument('courier', location='json', help='jne post tiki', choices=(
#             'jne', 'pos', 'tiki'), required=True)
#         args = parser.parse_args()

#         rq = requests.get(self.ro_host + '/cost', params={
#             'origin': args['origin'],
#             'destination': args['destination'],
#             'weight': int(args['weight'])*1000,
#             'courier': args['courier'],
#             'key': self.ro_apikey
#         })

#         res = rq.json()
#         res_format = {}
#         return res['rajaongkir']


# api.add_resource(RajaOngkir, '')
