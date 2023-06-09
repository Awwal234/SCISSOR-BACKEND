# **SCISSOR-BACKEND DOCUMENTATION**


<b style="font-size:17px;">
This project is built as a Capstone Project from AltSchool Africa.<br/>
The project is built using flask-restx API. Scissor allows users to shorten URLs by pasting a long URL into the platform and a shorter URL is automatically generated.
</b>

<br/><br/><br/>
## Implementation :

1) URL Shortening
2) Custom URLs
3) QR Code Generation
4) Analytics
5) Link History

<br/><br/>
## **Project Guide**
____________________

## *Installation* :

```python
# after cloning the repo you can then install all requirements.txt file to run

pip install -r requirements.txt

# the above command will help you install all the packages installed through my env and help you get to work.
```

## - *Code review* &#128077;
#
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

This backend API has a UI to test on.<br/>
*Lol* something like a frontend (yeah.) built with VueJs. [Frontend Link](https://momocut.vercel.app).
 **NB**: mobile view only

## **Bitly**