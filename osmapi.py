import Domoticz
import urllib.request, urllib.parse
from urllib.error import URLError, HTTPError
import json
import time

class osmapi:
    rgeocodeaddr = " https://nominatim.openstreetmap.org/reverse?format=json&lat=%s&lon=%s&zoom=18&addressdetails=0"
    trafficaddr = "http://router.project-osrm.org/route/v1/driving/%s;%s"

    def __init__(self):
        return

    def make_request(self, type, url):
        headers = {
            'Accept': 'application/json','User-Agent' : 'Domoticz/1.0'
        }
        Domoticz.Log('URL:'+url)
        time.sleep(1)
        request = urllib.request.Request(url, headers=headers)
        try:
            r = urllib.request.urlopen(request)
        except HTTPError as e:
            Domoticz.Log('OSMAPI HTTPError Code: '+ str(e.code))
            jsonr='Error'
        except URLError as e:
            Domoticz.Log('OSM Nominatim API URLError Reason: '+ str(e.reason))
            jsonr='Error'
        else:
            jsonj = json.loads(r.read().decode('utf-8'))
            if type == 0:
                jsonr = jsonj['display_name']
                retstatus = 'OK'
            elif type == 1:
                retstatus = jsonj["code"]
                if str(retstatus)=="Ok":
                    jsonr = jsonj["routes"][0]["duration"]
                elif str(retstatus)=="ZERO_RESULTS":
                    jsonr = 0
                Domoticz.Debug('Seconds:'+str(jsonr))
        return retstatus,jsonr

    def getaddress(self,lat,lon):
        url=self.rgeocodeaddr % (str(lat),str(lon))
        stat, req = self.make_request(type=0,url=url)
        Domoticz.Log('stat:'+str(stat))
        Domoticz.Log('req:'+str(req))

        r = req
        if r!='Error':
            return r
        else:
            return 'Error'

    def getdistance(self,lat1,lon1,lat2,lon2):
        url = self.trafficaddr % (str(lon1)+','+str(lat1),str(lon2)+','+str(lat2))
        Domoticz.Debug('URL:'+url)
        stat, dist = self.make_request(type=1,url=url)
        return stat,dist
