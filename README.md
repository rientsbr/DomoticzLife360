# DomoticzLife360
### * If updating from earlier versions of 1.0.3 to latest 1.0.3, please delete the old plugin from Domoticz Hardware and readd the 1.0.3. Required to create the device order txt file in order to handle Issue #5.

This is a Domoticz Plugin for Life 360

You get 3 device types: At Home Presence, Location and Battery Percentage

![alt text](https://www.dropbox.com/s/8jqwuq0big73da3/Life360Devices.jpg?raw=1)

There are 2 assumptions:
1. This Plugin follows only all the members of the the first circle in your Life360 app.
2. In order to follow Presence, you have to name your location as 'Home' in your Life360 app.

Thanks to Harper Reed for Python implementation of Life 360 API: https://github.com/harperreed/life360-python

The icons are downloaded from "Free Vector Graphics by www.Vecteezy.com"

## Installation:
Create a new life360 "folder" under Domoticz plugins directory. Copy all the files here to the new life360 folder.
Restart Domoticz, under Hardware page, select "Life360 Presence" as a new hardware and fill in the required fields. "Google maps API key is not required, but if you want to get current address of a member, you should get a Google maps API key and copy-paste here, otherwise leave it empty.

## How to get a Google Maps API Key:
Go to https://developers.google.com/maps/documentation/javascript/get-api-key page. Press "Get A Key" Button and follow the directives.
