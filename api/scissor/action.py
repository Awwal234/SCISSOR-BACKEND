from flask_restx import Namespace, Resource, fields
import requests
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask import request
from http import HTTPStatus
from flask_caching import Cache
import json
from ..models.link import LinkModel
from flask_jwt_extended import jwt_required

#Caching sysytem
from flask import Flask
app = Flask(__name__)
app.config['CACHE_TYPE'] = 'simple'
app.config['CACHE_DEFAULT_TIME'] = 300

cache = Cache(app)
#End Caching system
#Rate Limiting to Create Short Links
limiter = Limiter(get_remote_address, app=app, default_limits=["200 per day", "50 per hour"])

#End CodeSpace for Rate Limiting

action_namespace = Namespace('action', description='Namespace for all scissor actions')
link_model = action_namespace.model('Link',{
    'link': fields.String(required=True, description='link space for link actions')
})
alllink_model = action_namespace.model('AllLinks', {
    'id': fields.Integer(),
    'link': fields.String(required=True, description='link'),
    'short_link': fields.String(required=True, description='short link'),
    'created_at': fields.DateTime()
})

token = '046a5a46fa5509bb74507bea2f497bbbe30e3a7b'

@action_namespace.route('/shortenlink')
class ShortenLink(Resource):
    @action_namespace.expect(link_model)
    @limiter.limit('4 per day')
    @jwt_required()
    def post(self):
        '''
            Shorten link
        '''
        data = request.get_json()
        link = data.get('link')
        body = {
            "long_url": link,
            "domain": "bit.ly",
        }
        headers = {
            'Authorization': 'Bearer {}'.format(token),
            'Content-type': 'application/json'
        }
        response = requests.post('https://api-ssl.bitly.com/v4/shorten', json=body, headers=headers)
        response_dict = json.loads(response.content.decode('utf-8'))
        if response:
            shorts_link = response_dict['link']
            set_link = LinkModel(link=link, short_link=shorts_link)
            set_link.save()
        
            return response.json(), HTTPStatus.OK
        

# creating a QRCODE link request.
@action_namespace.route('/qrlink')
class QRLink(Resource):
    @action_namespace.expect(link_model)
    @jwt_required()
    def post(self):
        '''
            Create QRCode Link using domain and hashed link
        '''
        data = request.get_json()
        link = data.get('link')
        url = 'https://api-ssl.bitly.com/v4/bitlinks/{}/qr'.format(link)
        body = {
              "color": "1133ff",
              "exclude_bitly_logo": True,
              "logo_image_guid": "I123456789",
              "image_format": "png",
              "is_hidden": True
        }
        headers = {
            'Authorization': 'Bearer {}'.format(token),
            'Content-type': 'application/json'
        }
        response = requests.post(url, json=body, headers=headers)
        response_dict = response.content.decode('utf-8').strip('()')
        
        return response_dict, HTTPStatus.CREATED
        
# create a bitlink or custom link
@action_namespace.route('/bitlink')
class BitLink(Resource):
    @action_namespace.expect(link_model)
    @jwt_required()
    def post(self):
        '''
            create a bitlink
        '''
        data = request.get_json()
        link = data.get('link')
        url = 'https://api-ssl.bitly.com/v4/bitlinks'
        body = {
              "long_url": link,
              "domain": "bit.ly",
              "title": "Custom Link",
              "tags": [
                "bitly",
                "api"
              ],
              "deeplinks": [
                {
                  "app_id": "com.bitly.app",
                  "app_uri_path": "/store?id=123456",
                  "install_url": "https://play.google.com/store/apps/details?id=com.bitly.app&hl=en_US",
                  "install_type": "promote_install"
                }
              ]
        }
        headers = {
            'Authorization': 'Bearer {}'.format(token),
            'Content-type': 'application/json'
        }
        response = requests.post(url, json=body, headers=headers)
        return response.json(), HTTPStatus.CREATED
        
#List out all link
@action_namespace.route('/all_link')
class GetAllLinks(Resource):
    @cache.cached()
    @action_namespace.marshal_with(alllink_model)
    @jwt_required()
    def get(self):
        '''
            Display all Link
        '''
        links = LinkModel.query.all()
        return links, HTTPStatus.OK