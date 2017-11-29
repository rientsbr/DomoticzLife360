"""
<plugin key="Life360" name="Life 360 Presence" author="febalci" version="1.0.4">
    <params>
        <param field="Username" label="Life360 Username" width="150px" required="true" default="username"/>
        <param field="Password" label="Life360 Password" width="150px" required="true" default="password"/>
        <param field="Mode2" label="Poll Period (min)" width="75px" required="true" default="2"/>
        <param field="Mode3" label="Google Maps API Key" width="300px" required="false"/>        
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

from life360 import life360
from googlemapsapi import googlemapsapi

import json

class BasePlugin:

    def __init__(self):
        self.authorization_token = "cFJFcXVnYWJSZXRyZTRFc3RldGhlcnVmcmVQdW1hbUV4dWNyRUh1YzptM2ZydXBSZXRSZXN3ZXJFQ2hBUHJFOTZxYWtFZHI0Vg=="
        self.deviceFirstName = []
        self.membercount = 0
        self.circles = ''
        self.id = ''
        self.pollPeriod = 0
        self.pollCount = 0
        self.googleapikey = ''
        return

    def onStart(self):
        Domoticz.Log("onStart called")

        if (Parameters["Mode6"] == "Debug"):
            Domoticz.Debugging(1)

        if ("Life360Presence" not in Images):
            Domoticz.Debug('Icons Created...')
            Domoticz.Image('Life360Presenceicon.zip').Create()
        iconPID = Images["Life360Presence"].ID

        api = life360(authorization_token=self.authorization_token, username=Parameters["Username"], password=Parameters["Password"])
        if api.authenticate():
            Domoticz.Debug("API Authenticated")
            #Grab some circles returns json
            self.circles =  api.get_circles()
            Domoticz.Debug("Circles:"+str(self.circles))        
            #grab id
            self.id = self.circles[0]['id']
            Domoticz.Debug("Circle 0 ID:"+str(self.id))
            #Let's get your circle!
            circle = api.get_circle(self.id)
            Domoticz.Debug("Family Circle:"+str(circle))
            self.membercount = int(circle['memberCount'])
            Domoticz.Debug('Member Count = '+str(self.membercount))
        else:
            Domoticz.Log("Error authenticating...")

        if (len(Devices) == 0):
            for member in range (self.membercount):
                self.deviceFirstName.append(circle['members'][member]['firstName'])
                Domoticz.Device(Name=self.deviceFirstName[member]+' Presence', Unit=(member*3)+1, TypeName="Switch", Image=iconPID, Used=1).Create()
                Domoticz.Device(Name=self.deviceFirstName[member]+' Location', Unit=(member*3)+2, TypeName="Text", Used=0).Create()
                Domoticz.Device(Name=self.deviceFirstName[member]+' Battery',Unit=(member*3)+3, TypeName="Percentage", Used=1).Create()
            Domoticz.Debug(str(self.deviceFirstName))
            with open(Parameters["HomeFolder"]+"deviceorder.txt","w") as f:
                json.dump(self.deviceFirstName,f)
        else:
            with open(Parameters["HomeFolder"]+"deviceorder.txt") as f: self.deviceFirstName = json.load(f)
            Domoticz.Debug(str(self.deviceFirstName))

        Domoticz.Debug("Devices created.")
        DumpConfigToLog()

        if (Parameters["Mode3"] == ""):
            self.googleapikey = 'Empty'
        else:
            self.googleapikey = Parameters["Mode3"]
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
            Domoticz.Log("Checking Circle...")
            api = life360(authorization_token=self.authorization_token, username=Parameters["Username"], password=Parameters["Password"])
            if api.authenticate():
                #Let's get your circle!
                circle = api.get_circle(self.id)
                Domoticz.Debug("Family Circle:"+str(circle))
            else:
                Domoticz.Log("Error authenticating...")

            for member in range (self.membercount):
                Domoticz.Debug(str(member)+'/'+str(self.membercount))
                foundDeviceIdx = self.deviceFirstName.index(circle['members'][member]['firstName'])
                Domoticz.Debug('Foundidx='+str(foundDeviceIdx)+','+circle['members'][member]['firstName'])
                if circle['members'][member]['location']['name'] == 'Home':
                    UpdateDevice((foundDeviceIdx*3)+1,1,'On')
                    Domoticz.Debug('Updated Device:'+str((foundDeviceIdx*3)+1)+','+circle['members'][member]['firstName'])
                else:
                    UpdateDevice((foundDeviceIdx*3)+1,0,'Off')
                    Domoticz.Debug('Updated Device:'+str((foundDeviceIdx*3)+1)+','+circle['members'][member]['firstName'])
                    
                if circle['members'][member]['location']['name'] == None:
                    if self.googleapikey != 'Empty':
                        a = googlemapsapi()
                        currentloc = a.getaddress(self.googleapikey,circle['members'][member]['location']['latitude'],circle['members'][member]['location']['longitude'])
                    else:
                        currentloc = 'None'
                else:
                    currentloc = circle['members'][member]['location']['name']
                UpdateDevice((foundDeviceIdx*3)+2,1,currentloc)
                Domoticz.Debug('Updated Device:'+str((foundDeviceIdx*3)+2)+','+circle['members'][member]['firstName'])
 
                UpdateDevice((foundDeviceIdx*3)+3,int(float(circle['members'][member]['location']['battery'])),circle['members'][member]['location']['battery'])
                Domoticz.Debug('Updated Device:'+str((foundDeviceIdx*3)+3)+','+circle['members'][member]['firstName'])
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

def UpdateDevice(Unit, nValue, sValue):
    # Make sure that the Domoticz device still exists (they can be deleted) before updating it 
    if (Unit in Devices):
        if (Devices[Unit].nValue != nValue) or (Devices[Unit].sValue != sValue):
            Devices[Unit].Update(nValue, str(sValue))
            Domoticz.Log("Update "+str(nValue)+":'"+str(sValue)+"' ("+Devices[Unit].Name+")")
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