# Domoticz Life360


[![PyPI pyversions](https://img.shields.io/badge/python-3.6%20|%203.7%20|%203.8%203.9-blue.svg)]()
[![Plugin version](https://img.shields.io/badge/version-0.7.0-red.svg)](https://github.com/belzetrigger/domoticz-FritzPresence/branches/)

Primary a Presence Detector that works with your [Fritz!Box](https://en.avm.de/, 'Fritz!Box are quite famous router from avm'). And also lets you add easily other known hosts from your Box to Domoticz.


## Summary

This is a Domoticz Plugin to use information from the Life 360 app.
We will create 4 device types:
- Home Presence
- Battery
- Location
- Driving distance (in Minutes)

![alt text](https://www.dropbox.com/s/8jqwuq0big73da3/Life360Devices.jpg?raw=1)

This Plugin follows the members of the the **first circle** in your Life360 app.


Thanks to Harper Reed  and belzetrigger for Python implementation of Life 360.

The icons are downloaded from "Free Vector Graphics by www.Vecteezy.com"


## Installation and Setup
- a running Domoticz: 2020.2 or 2021.1 with Python 3.7
- clone project
    - go to `domoticz/plugins` directory
    - clone the project
        ```bash
        cd domoticz/plugins
        git clone https://github.com/rientsbr/dDomoticzLife360.git
        ```
- or just download, unzip and copy to `domoticz/plugins`
- no need on Raspbian for sys path adaption if using sudo for pip3
- restart Domoticz service
- Now go to **Setup**, **Hardware** in your Domoticz interface. There add
**Fritz!Presence Plugin**.
### Settings
<!-- prettier-ignore -->

## Usage
### Admin
this functions is not Used

## Bugs and ToDos


## Versions
| Version | Note                                                                                     |
| ------- | ---------------------------------------------------------------------------------------- |
| 0.7.0   | * change handling in case of MAC-List usage. Device names are fetched from Fritz!Box and updated on Heartbeat  <br>* Using domoticz special Parameter User/Password - so please reinsert.<br> * avoid overwriting custom images with default icons during start up<br> * better checking if inserted values are MAC-Addresses                                        |
| 0.6.4   | small stability fixes, a bit restructure and tested with new version of lib <br>for issue#2, avoid resetting images on startup also if MAC-List is used, so custom symbols will be kept   |
| 0.6.3   | button to add/remove know hosts from Fritz!Box to Domoticz and support for "Wake on LAN" |
| 0.6.2   | supports ';' separated list of MAC and names                                             |
| \>= 0.6 | works with new fritzconnection 1.2.1 and so without need of lxml but Python >= 3.6       |
| <= 0.5  | worked with fritzconnection 0.6.x and 0.8.x, needs lxml                                  |

## State
Under development but main function runs quite stabile.



## How to get a TomTom API Key:
Go to https://developer.tomtom.com/user/register page. Create a new User Account. Login to your account and from 'My Apps', press 'Add a new app' to add a new app and select at least 'Routing API' and 'Search API', you can select all APIs here if you want. Then from the 'Keys' page, copy the 'Consumer API Key' of your app to Life360 plugin setting page - 'TomTom API Key' field. Remember, you have 2.500 daily API calls limit fro free... When you are at 'Home', there are no API calls to TomTom.
