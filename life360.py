#!/usr/bin/env python
import Domoticz
import urllib.request, urllib.parse
from urllib.error import URLError, HTTPError
import json

class life360:
    
    base_url = "https://api-cloudfront.life360.com/v3/"
    USER_AGENT = "com.life360.android.safetymapd"
    token_url = "oauth2/token.json"
    circles_url = "circles.json"
    circle_url = "circles/"

    def __init__(self, authorization_token=None, username=None, password=None):
        self.authorization_token = authorization_token
        self.username = username
        self.password = password

    def make_request(self, url, params=None, method='GET', authheader=None):
        headers = {
            'Accept': 'application/json',
            'user-agent': 'com.life360.android.safetymapd'
        }
        if authheader:
            headers.update({'Authorization': authheader, 'cache-control': "no-cache",})
        
        if method == 'GET':
            request = urllib.request.Request(url, headers=headers)
        elif method == 'POST':
            request = urllib.request.Request(url, data=(urllib.parse.urlencode(params)).encode('utf-8'), headers=headers)

        try:
            r = urllib.request.urlopen(request)
        except HTTPError as e:
            Domoticz.Log('Life360 HTTPError code: '+ str(e.code))
            jsonr = 'Error'
        except URLError as e:
            Domoticz.Log('Life360 URLError Reason: '+ str(e.reason))
            jsonr = 'Error'
        else:
            jsonr = json.loads(r.read().decode('utf-8'))

        return jsonr

    def authenticate(self):
        url = self.base_url + self.token_url
        params = {
            "grant_type":"password",
            'username': self.username,
            'password': self.password
        }
        r = self.make_request(url=url, params=params, method='POST', authheader="Basic " + self.authorization_token)
        if r!= 'Error':        
            self.access_token = r['access_token']
            Domoticz.Debug('Token Received: '+self.access_token)
            return True
        else:
                Domoticz.Log('No Token Received; Please Check Life360 Username and Password')
                Domoticz.Debug('You can Validate Your Credentials in www.life360.com')
                return False            

    def get_circle_id(self):
        url = self.base_url + self.circles_url
        authheader="bearer " + self.access_token
        r = self.make_request(url=url, method='GET', authheader=authheader)
        if r!='Error':
            return r['circles'][0]['id']
        else:
            return 'Error'

    def get_circle(self, circle_id):
        url = self.base_url + self.circle_url + circle_id
        authheader="bearer " + self.access_token
        r = self.make_request(url=url, method='GET', authheader=authheader)
        if r!='Error':
            return r
        else:
            return 'Error'

