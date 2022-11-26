"""
<plugin key="Life360" name="Life 360 Presence" author="rmbrandsma" version="1.0.0">
    <params>
        <param field="Username" label="Life360 Email Address" width="150px" required="true" default="username"/>
        <param field="Password" label="Life360 Password" width="150px" required="true" default="password"/>
        <param field="Mode1" label="Naam Thuis" width="150px"/>
        <param field="Mode2" label="Poll Period (min)" width="75px" required="true" default="2"/>
        <param field="Mode4" label="Choose Map provider" width="300px">
            <options>
                <option label="TomTom Maps" value="TM"/>
                <option label="Open Streetmap" value="OSM" default="true" />
            </options>
        </param>
        <param field="Mode3" label="TomTom API Key" width="300px" required="false"/>
        <param field="Mode6" label="Debug" width="75px">
            <options>
                <option label="True" value="Debug"/>
                <option label="False" value="Normal"  default="true" />
            </options>
        </param>
    </params>
</plugin>
"""
import Domoticz
import datetime
import time

from math import radians, cos, sin, asin, sqrt
from life360 import life360
from tomtomapi import tomtomapi
from osmapi import osmapi

import json

class BasePlugin:

    def __init__(self):
        self.authorization_token = "cFJFcXVnYWJSZXRyZTRFc3RldGhlcnVmcmVQdW1hbUV4dWNyRUh1YzptM2ZydXBSZXRSZXN3ZXJFQ2hBUHJFOTZxYWtFZHI0Vg=="
        self.deviceFirstName = []
        self.membercount = 0
        self.id = ''
        self.pollPeriod = 0
        self.pollCount = 0
        self.tomtomapikey = ''
        self.myHomelat = 0
        self.myHomelon = 0
        self.circleFirstName = ''
        self.circleBattery = 0
        self.circleLatitude = 0
        self.circleLongitude = 0
        self.circlLocationName = ''
        self.selectedMap = ''
        self.locationNames = []
        return

    def onStart(self):
        Domoticz.Log("onStart called")
        if (Parameters["Mode6"] == "Debug"):
            Domoticz.Debugging(1)

        if ("Life360Presence" not in Images):
            Domoticz.Debug('Icons Created...')
            Domoticz.Image('Life360Presenceicon.zip').Create()
        iconPID = Images["Life360Presence"].ID

        # Get the location from the Settings
        if not "Location" in Settings:
            Domoticz.Log("Location not set in Preferences")
            return False

        # The location is stored in a string in the Settings
        loc = Settings["Location"].split(";")
        self.myHomelat = float(loc[0])
        self.myHomelon = float(loc[1])
        Domoticz.Debug("Coordinates from Domoticz: " + str(self.myHomelat) + ";" + str(self.myHomelon))

        if self.myHomelat == None or self.myHomelon == None:
            Domoticz.Log("Unable to parse coordinates")
            return False

        api = life360(authorization_token=self.authorization_token, username=Parameters["Username"], password=Parameters["Password"])
        if api.authenticate():
            Domoticz.Debug("API Authenticated")

            #Grab id
            self.id = api.get_circle_id()
            Domoticz.Debug("Circle 0 ID:"+str(self.id))
            #Let's get your circle!
            circle = api.get_circle(self.id)
            Domoticz.Debug("Family Circle:"+str(circle))
            self.membercount = int(circle['memberCount'])
            Domoticz.Debug('Member Count = '+str(self.membercount))

            if (len(Devices) == 0):
                for member in range (self.membercount):
                    self.deviceFirstName.append(circle['members'][member]['firstName'])
                    Domoticz.Device(Name=self.deviceFirstName[member]+' Presence', Unit=(member*4)+1, TypeName="Switch", Image=iconPID, Used=1).Create()
                    Domoticz.Device(Name=self.deviceFirstName[member]+' Location', Unit=(member*4)+2, TypeName="Text", Used=1).Create()
                    Domoticz.Device(Name=self.deviceFirstName[member]+' Battery',Unit=(member*4)+3, TypeName="Percentage", Used=1).Create()
                    Domoticz.Device(Name=self.deviceFirstName[member]+' Distance',Unit=(member*4)+4, TypeName="Custom", Options={"Custom": "1;mins"}, Used=1).Create()
                Domoticz.Debug(str(self.deviceFirstName))
                with open(Parameters["HomeFolder"]+"deviceorder.txt","w") as f:
                    json.dump(self.deviceFirstName,f)
            else:
                with open(Parameters["HomeFolder"]+"deviceorder.txt") as f: self.deviceFirstName = json.load(f)
                Domoticz.Debug(str(self.deviceFirstName))

            Domoticz.Debug("Devices created.")
            DumpConfigToLog()
        else:
            Domoticz.Log('Error Authenticating Life360 or Connection Problem...')
            Domoticz.Log('Please Use Correct Credentials and Restart The Plugin!')

        self.Home = Parameters["Mode1"]

        if (Parameters["Mode4"] == "OSM"):
            self.selectedMap = "OSM"
        else:
            self.selectedMap = "TM"

        if (Parameters["Mode3"] == ""):
            self.tomtomapikey = 'Empty'
        else:
            self.tomtomapikey = Parameters["Mode3"]

        try:
            with open(Parameters["HomeFolder"]+"locations.txt") as f:
                for line in f:
                    self.locationNames.append(line.rstrip('\n').split(','))
        except:
            Domoticz.Log('No locations.txt file found')

        self.pollPeriod = 6 * int(Parameters["Mode2"])
        self.pollCount = self.pollPeriod - 1
        Domoticz.Heartbeat(10)

    def onStop(self):
        Domoticz.Log("onStop called")

    def onConnect(self, Connection, Status, Description):
        Domoticz.Log("onConnect called")

    def onMessage(self, Connection, Data, Status, Extra):
        Domoticz.Log("onMessage called")

    def onCommand(self, Unit, Command, Level, Hue):
        Domoticz.Log("onCommand called for Unit " + str(Unit) + ": Parameter '" + str(Command) + "', Level: " + str(Level))
        Command = Command.strip()
        action, sep, params = Command.partition(' ')
        action = action.capitalize()
        params = params.capitalize()

        if Command=='Off':
            UpdateDevice(Unit,0,'Off')
        elif Command=='On':
            UpdateDevice(Unit,1,'On')

    def onNotification(self, Name, Subject, Text, Status, Priority, Sound, ImageFile):
        Domoticz.Log("Notification: " + Name + "," + Subject + "," + Text + "," + Status + "," + str(Priority) + "," + Sound + "," + ImageFile)

    def onDisconnect(self, Connection):
        Domoticz.Log("onDisconnect called")

    def onHeartbeat(self):
        Domoticz.Debug("onHeartBeat called:"+str(self.pollCount)+"/"+str(self.pollPeriod))
        if self.pollCount >= self.pollPeriod:
            Domoticz.Log("Checking Life360 Circle...")
            api = life360(authorization_token=self.authorization_token, username=Parameters["Username"], password=Parameters["Password"])
            if api.authenticate():
                #self.id = api.get_circle_id()  //Removed v2.0.0
                #Let's get your circle!
                circle = api.get_circle(self.id)

                Domoticz.Debug("Family Circle:"+str(circle))
                for member in range (self.membercount):
                    Domoticz.Debug(str(member)+'/'+str(self.membercount))
                    #Assign Variables
                    self.circleFirstName = circle['members'][member]['firstName']
                    self.circleBattery = circle['members'][member]['location']['battery']
                    self.circleLatitude = circle['members'][member]['location']['latitude']
                    self.circleLongitude = circle['members'][member]['location']['longitude']
                    self.circlLocationName = circle['members'][member]['location']['name']

                    foundDeviceIdx = self.deviceFirstName.index(self.circleFirstName)
                    Domoticz.Debug('Foundidx='+str(foundDeviceIdx)+','+self.circleFirstName)
                    if self.circlLocationName == self.Home:
                        UpdateDevice((foundDeviceIdx*4)+1,1,'On')
                        Domoticz.Debug('Updated Device:'+str((foundDeviceIdx*4)+1)+','+self.circleFirstName)
                    else:
                        UpdateDevice((foundDeviceIdx*4)+1,0,'Off')
                        Domoticz.Debug('Updated Device:'+str((foundDeviceIdx*4)+1)+','+self.circleFirstName)

                    if self.selectedMap == "TM":
                        a = tomtomapi()
                    elif self.selectedMap == "OSM":
                        a = osmapi()

                    if self.circlLocationName == None:
                        currentloc = None
                        if self.selectedMap == "TM":
                            if self.tomtomapikey != 'Empty':
                                currentstat, currentmin = a.getdistance(self.tomtomapikey,self.circleLatitude,self.circleLongitude,self.myHomelat,self.myHomelon)
                                for line in self.locationNames[1:]:
                                    aa= haversine(float(self.circleLatitude),float(self.circleLongitude),float(line[1]),float(line[2]))
                                    if int(aa)<=int(line[3]):
                                        currentloc=line[0]
                                if currentloc==None:
                                    currentstat2, currentloc = a.getaddress(self.tomtomapikey,self.circleLatitude,self.circleLongitude)
                            else:
                                currentloc = 'TomTom API Key not set!'
                                currentmin = 0

                        elif self.selectedMap == "OSM":
                            currentstat, currentloc = a.getaddress(self.circleLatitude,self.circleLongitude)
                            currentmin = 0
                            for line in self.locationNames[1:]:
                                aa= haversine(float(self.circleLatitude),float(self.circleLongitude),float(line[1]),float(line[2]))
                                if int(aa)<=int(line[3]):
                                    currentloc=line[0]

                            # Get distance
                            # currentstat, currentmin = a.getdistance(self.circleLatitude,self.circleLongitude,self.myHomelat,self.myHomelon)

                    else:
                        currentloc = self.circlLocationName
                        if self.circlLocationName == self.Home:
                            currentmin = 0
                        else: #Location known on Life360, but other than 'Home'
                            if self.selectedMap == "TM":
                                if self.tomtomapikey != 'Empty':
                                    currentstat, currentmin = a.getdistance(self.tomtomapikey,self.circleLatitude,self.circleLongitude,self.myHomelat,self.myHomelon)
                                else:
                                    currentloc = 'TomTom API Key not set!'
                                    currentmin = 0
                            elif self.selectedMap == "OSM":
                                currentmin = 0


                    UpdateDevice((foundDeviceIdx*4)+2,1,currentloc)
                    Domoticz.Debug('Updated Device:'+str((foundDeviceIdx*4)+2)+','+self.circleFirstName)

                    UpdateDevice((foundDeviceIdx*4)+3,int(float(self.circleBattery)),str(int(float(self.circleBattery))))
                    Domoticz.Debug('Updated Device:'+str((foundDeviceIdx*4)+3)+','+self.circleFirstName)
                    try:
                        currentmin = str(int(currentmin//60))
                    except:
                        currentmin = "Error"

                    UpdateDevice((foundDeviceIdx*4)+4,0,currentmin)
                    Domoticz.Debug('Updated Device:'+str((foundDeviceIdx*4)+4)+','+self.circleFirstName)

                    if self.selectedMap == "OSM": # In respect of OSM's usage policy of 1 call per second
                        time.sleep(1)
            else:
                Domoticz.Log("Error Authenticating Life360 or Connection Problem...")
                Domoticz.Log('Please Use Correct Credentials and Restart The Plugin!!!')

            self.pollCount = 0 #Reset Pollcount
        else:
            self.pollCount = self.pollCount + 1


global _plugin
_plugin = BasePlugin()

def onStart():
    global _plugin
    _plugin.onStart()

def onStop():
    global _plugin
    _plugin.onStop()

def onConnect(Connection, Status, Description):
    global _plugin
    _plugin.onConnect(Connection, Status, Description)

def onMessage(Connection, Data, Status, Extra):
    global _plugin
    _plugin.onMessage(Connection, Data, Status, Extra)

def onCommand(Unit, Command, Level, Hue):
    global _plugin
    _plugin.onCommand(Unit, Command, Level, Hue)

def onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile):
    global _plugin
    _plugin.onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile)

def onDisconnect(Connection):
    global _plugin
    _plugin.onDisconnect(Connection)

def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()

def haversine(lat1, lon1, lat2, lon2):

    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r * 1000

def UpdateDevice(Unit, nValue, sValue):
    # Make sure that the Domoticz device still exists (they can be deleted) before updating it
    if (Unit in Devices):
        if (Devices[Unit].nValue != nValue) or (Devices[Unit].sValue != sValue):
            Devices[Unit].Update(nValue=nValue, sValue=str(sValue))
            Domoticz.Debug("Update "+str(nValue)+":'"+str(sValue)+"' ("+Devices[Unit].Name+")")
    return


    # Generic helper functions
def DumpConfigToLog():
    for x in Parameters:
        if Parameters[x] != "":
            Domoticz.Debug( "'" + x + "':'" + str(Parameters[x]) + "'")
    Domoticz.Debug("Device count: " + str(len(Devices)))
    for x in Devices:
        Domoticz.Debug("Device:           " + str(x) + " - " + str(Devices[x]))
        Domoticz.Debug("Device ID:       '" + str(Devices[x].ID) + "'")
        Domoticz.Debug("Device Name:     '" + Devices[x].Name + "'")
        Domoticz.Debug("Device nValue:    " + str(Devices[x].nValue))
        Domoticz.Debug("Device sValue:   '" + Devices[x].sValue + "'")
        Domoticz.Debug("Device LastLevel: " + str(Devices[x].LastLevel))
    return
