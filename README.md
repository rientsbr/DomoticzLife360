# DomoticzLife360
### *** Please Note that due to the new pricing scheme of Google Maps API, this plugin has some memory and error issues. Have to find another service provider for traffic data...
### * If updating from earlier versions of 1.1.0, please delete all Life360 devices from Domoticz-Settings-Devices. Restarting the plugin with the new 1.1.0 will recreate the devices. Required to create new device and remove battery device to incorporate request issue #6 Distance in minutes. 

This is a Domoticz Plugin for Life 360

You get 4 device types: At Home Presence, Battery, Location and Driving Distance in Minutes

![alt text](https://www.dropbox.com/s/8jqwuq0big73da3/Life360Devices.jpg?raw=1)

There are 2 assumptions:
1. This Plugin follows only all the members of the the first circle in your Life360 app.
2. In order to follow Presence, you have to name your location as 'Home' in your Life360 app.

Thanks to Harper Reed for Python implementation of Life 360 API: https://github.com/harperreed/life360-python

The icons are downloaded from "Free Vector Graphics by www.Vecteezy.com"

## Installation:
Create a new Life360 "folder" under Domoticz plugins directory. Copy all the files here to the new Life360 folder.
Restart Domoticz, under Hardware page, select "Life360 Presence" as a new hardware and fill in the required fields. "Google maps API key is not required, but if you want to get current address of a member and driving distance, you should get a Google maps API key and copy-paste here, otherwise leave it empty.

## How to get a Google Maps API Key:
Go to https://developers.google.com/maps/documentation/javascript/get-api-key page. Press "Get A Key" Button and follow the directives.
