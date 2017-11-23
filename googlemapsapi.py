#!/usr/bin/env python
import urllib.request, urllib.parse
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
        r = urllib.request.urlopen(request)

        jsonr = json.loads(r.read().decode('utf-8'))
        return jsonr

    def getaddress(self,apikey,lat,lon):
        url=self.rgeocodeaddr+str(lat)+','+str(lon)+'&key='+str(apikey)
        req = self.make_request(url=url)
        r = req['results'][0]['formatted_address']
        return r
