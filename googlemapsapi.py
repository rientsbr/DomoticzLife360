#!/usr/bin/env python
import Domoticz
import urllib.request, urllib.parse
from urllib.error import URLError, HTTPError
import json

class googlemapsapi:
    rgeocodeaddr = "https://maps.googleapis.com/maps/api/geocode/json?latlng="

    def __init__(self):
        return

    def make_request(self, url):
        headers = {
            'Accept': 'application/json'
        }

        request = urllib.request.Request(url, headers=headers)
        try:
            r = urllib.request.urlopen(request)
        except HTTPError as e:
            Domoticz.Log('Life360 HTTPError Code: '+ str(e.code))
            jsonr='Error'
        except URLError as e:
            Domoticz.Log('Google API URLError Reason: '+ str(e.reason))
            jsonr='Error'
        else:
            jsonj = json.loads(r.read().decode('utf-8'))
            jsonr = jsonj['results'][0]['formatted_address']
        return jsonr

    def getaddress(self,apikey,lat,lon):
        url=self.rgeocodeaddr+str(lat)+','+str(lon)+'&key='+str(apikey)
        req = self.make_request(url=url)
        r = req
        if r!='Error':
            return r
        else:
            return 'Error'
