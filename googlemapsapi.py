#!/usr/bin/env python
import Domoticz
import urllib.request, urllib.parse
from urllib.error import URLError, HTTPError
import json

#18.09.2018
#Check distance status added

class googlemapsapi:
    rgeocodeaddr = "https://maps.googleapis.com/maps/api/geocode/json?latlng="
    trafficaddr = "https://maps.googleapis.com/maps/api/directions/json?origin=%s&destination=%s&transit_mode=driving&departure_time=now&key=%s"

    def __init__(self):
        return

    def make_request(self, type, url):
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
            if type == 0:
                jsonr = jsonj['results'][0]['formatted_address']
            elif type == 1:
                retstatus = jsonj["status"]
                if str(retstatus)=="OK":
                    jsonr = jsonj["routes"][0]["legs"][0]["duration_in_traffic"]["value"]
                    jsons = jsonj["routes"][0]["legs"][0]["start_address"]
                elif str(retstatus)=="ZERO_RESULTS":
                    jsonr = 0
                    jsons = ""
                Domoticz.Debug('Seconds:'+str(jsonr))
        return retstatus,jsonr,jsons

    def getaddress(self,apikey,lat,lon):
        url=self.rgeocodeaddr+str(lat)+','+str(lon)+'&key='+str(apikey)
        req = self.make_request(type=0,url=url)
        r = req
        if r!='Error':
            return r
        else:
            return 'Error'
    
    def getdistance(self,apikey,lat1,lon1,lat2,lon2):
        url = self.trafficaddr % (str(lat1)+','+str(lon1),str(lat2)+','+str(lon2),apikey)
        Domoticz.Debug('URL:'+url)
        stat, dist, address = self.make_request(type=1,url=url)
        return stat,dist,address
