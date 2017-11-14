"""
<plugin key="Life360" name="Life 360 Presence" author="febalci" version="1.0.0">
    <params>
        <param field="Username" label="Life360 Username" width="150px" required="true" default="username"/>
        <param field="Password" label="Life360 Password" width="150px" required="true" default="password"/>
        <param field="Mode2" label="Poll Period (sec)" width="75px" required="true" default="120"/>
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

class BasePlugin:
    authorization_token = "cFJFcXVnYWJSZXRyZTRFc3RldGhlcnVmcmVQdW1hbUV4dWNyRUh1YzptM2ZydXBSZXRSZXN3ZXJFQ2hBUHJFOTZxYWtFZHI0Vg=="

    def __init__(self):
        #self.var = 123
        return

    def onStart(self):
        global membercount
        global circles
        global id

        if (Parameters["Mode6"] == "Debug"):
            Domoticz.Debugging(1)
            
        Domoticz.Log("onStart called")
        api = life360(authorization_token=self.authorization_token, username=Parameters["Username"], password=Parameters["Password"])
        if api.authenticate():
            Domoticz.Debug("API Authenticated")
            #Grab some circles returns json
            circles =  api.get_circles()
            Domoticz.Debug("Circles:"+str(circles))        
            #grab id
            id = circles[0]['id']
            Domoticz.Debug("Circle 0 ID:"+str(id))
            #Let's get your circle!
            circle = api.get_circle(id)
            Domoticz.Debug("Family Circle:"+str(circle))
            membercount = int(circle['memberCount'])
            Domoticz.Debug('Member Count = '+str(membercount))
        else:
            Domoticz.Log("Error authenticating...")

        if (len(Devices) == 0):
            for member in range (1,membercount+1):
                Domoticz.Device(Name=circle['members'][member-1]['firstName']+' Presence', Unit=member, TypeName="Switch", Used=1).Create()
                Domoticz.Device(Name=circle['members'][member-1]['firstName']+' Location', Unit=member+membercount, TypeName="Text", Used=0).Create()
                Domoticz.Device(Name=circle['members'][member-1]['firstName']+' Battery',Unit=member+(2*membercount), TypeName="Percentage", Used=0).Create() 
        Domoticz.Debug("Devices created.")
        DumpConfigToLog()

        Domoticz.Heartbeat(int(Parameters["Mode2"]))

    def onStop(self):
        Domoticz.Log("onStop called")

    def onConnect(self, Connection, Status, Description):
        Domoticz.Log("onConnect called")

    def onMessage(self, Connection, Data, Status, Extra):
        Domoticz.Log("onMessage called")

    def onCommand(self, Unit, Command, Level, Hue):
        Domoticz.Log("onCommand called for Unit " + str(Unit) + ": Parameter '" + str(Command) + "', Level: " + str(Level))

    def onNotification(self, Name, Subject, Text, Status, Priority, Sound, ImageFile):
        Domoticz.Log("Notification: " + Name + "," + Subject + "," + Text + "," + Status + "," + str(Priority) + "," + Sound + "," + ImageFile)

    def onDisconnect(self, Connection):
        Domoticz.Log("onDisconnect called")

    def onHeartbeat(self):
        Domoticz.Log("onHeartbeat called")
        api = life360(authorization_token=self.authorization_token, username=Parameters["Username"], password=Parameters["Password"])
        if api.authenticate():
                #Let's get your circle!
            circle = api.get_circle(id)
            Domoticz.Debug("Family Circle:"+str(circle))
        else:
            Domoticz.Log("Error authenticating...")

        for member in range (1,membercount+1):
            if circle['members'][member-1]['location']['name'] == 'Home':
                UpdateDevice(member,1,'On')
            else:
                UpdateDevice(member,0,'Off')
            UpdateDevice(member+membercount,1,circle['members'][member-1]['location']['name'])
            UpdateDevice(member+(2*membercount),int(circle['members'][member-1]['location']['battery']),circle['members'][member-1]['location']['battery'])


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
