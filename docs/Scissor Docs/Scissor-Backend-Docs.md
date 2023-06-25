---
stoplight-id: mdmgrs51gj786
tags: [flask, capstone]
---

## Scissor-Backend-Docs
_______________________

The scissor backend project is a capstone project from AltSchool (Backend track) using the Python framework flask and API(Restx).
When the project view was made, I had to do my architecting with the project. So basically I did a fullstack project here(VueJs and Python).

### Implementation :
___________________

1. URL Shortening
2. Custom URLs
3. QR Code Generation
4. Analytics
5. Link History

### - Code review 👍
________________

```python

#from the first part where we have the url shortening. Below is the code with a simple integration.

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
            'Authorization': 'Bearer {}'.format(your_token),
            'Content-type': 'application/json'
        }
        response = requests.post('https://api-ssl.bitly.com/v4/shorten', json=body, headers=headers)
        response_dict = json.loads(response.content.decode('utf-8'))
        if response:
            shorts_link = response_dict['link']
            set_link = LinkModel(link=link, short_link=shorts_link)
            set_link.save()
        
            return response.json(), HTTPStatus.OK
            
#from what you can see, I added a limiter to make a request to that api four(4) per day since i'm running on free tier
```

```python

# want to check out qrLink?
# Now, this is the thing. This code works but won't provide the base64 image; string you need due to running on free tier, but reading the code and json body you will know this is right ...

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
```

### -Endpoints
______________

- Login : /api/auth/login (POST)
- SignUp : /api/auth/signup (POST)
- Refresh : /api/auth/refresh (GET)
- Get User : /api/auth/getme (GET)
- Shorten Link : /api/link/shortenlink (POST)
- qrCode : /api/link/qrlink (Frontend UI does this also without backend due to free tier) (POST)
- Get all Links : /api/link/all_link (GET)