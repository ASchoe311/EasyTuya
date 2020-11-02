# EasyTuya - Making IOT Control With Python Easy

EasyTuya is a module containing nearly all needed functionality for interacting with your Tuya powered IOT devices through Python. This is done using [Tuya's web API](https://developer.tuya.com/en/docs/iot/open-api/api-list/api?id=K989ru6gtvspg), meaning that for this module to work you will need a cloud developer account on Tuya's website. Full instructions for this and general setup can be found below. If you have not already, to use this you must also download the TuyaSmart app on your phone and add your compatible devices.

# Installation

    pip3 install EasyTuya
### Requirements

 - [pycryptodome](https://pypi.org/project/pycryptodome/)

# Tuya Account Setup - IMPORTANT!!

 - [Make a developer account on Tuya's site](https://iot.tuya.com/)
 -  Once signed in click on "Cloud Development" (or go to https://iot.tuya.com/cloud/)
 - Create a project
 - Click on your new project, you should see a screen similar to this![The project page](https://i.imgur.com/Z7YqYPn.jpg)
 - Note your client ID and access secret
 - Go to "Link Devices" under device management, then select the tab titled "Link devices by App Account"
 - Follow instructions on the site to add your Tuya app account and connected devices
 - Click "API Group" in the left sidebar, then click "Apply" on the groups: "Authorization Management", "Device Management", and "Device Control"
 - Open other API group as needed by your usage 
# Usage Example
### A simple program to control a group of lights through command line input
	from EasyTuya import TuyaAPI
	from EasyTuya.devices import Lights
	
	if __name__ == "__main__":
	    api = TuyaAPI("your_client_id", "your_access_secret")
	    l1 = Lights.Light("your_device_id_1", "Light 1")
	    l2 = Lights.Light("your_device_id_2", "Light 2")
	    api.addDevices([l1, l2], "LIGHTS")
	    while(True):
	        toDo = input()
	        if toDo == "on":
	            api.sendCommands("LIGHTS", Lights.onCommand())
	        elif toDo == "off":
	            api.sendCommands("LIGHTS", Lights.offCommand())
	        elif toDo == "white":
	            api.sendCommands("LIGHTS", Lights.workModeCommand("white"))
	        elif toDo == "color":
	            api.sendCommands("LIGHTS", Lights.workModeCommand("colour"))
	        elif toDo == "red":
	            api.sendCommands("LIGHTS", Lights.colorCommand(Lights.redHSV))
	        elif toDo == "blue":
	            api.sendCommands("LIGHTS", Lights.colorCommand(Lights.blueHSV))
	        elif toDo == "rainbow":
	            api.sendCommands("LIGHTS", Lights.sceneCommand(4))
	        elif toDo.split()[0] == "bright":
	            api.sendCommands("LIGHTS", Lights.brightnessCommand(int(toDo.split()[1])))
	        elif toDo == "onoff":
	            api.sendCommands("LIGHTS", api.devices['LIGHTS'][0].toggleOnOff())
	        elif toDo == "status":
	            print(api.getStatus("LIGHTS"))

               
# Other Notes
### Finding Device IDs
To find your device IDs, go to:
Tuya developer site -> Device Management -> Device List
Select your correct country from the drop down near the center of the page, then your devices should show up each with their name displayed above their device id, as shown in the following image.
![The device list page](https://i.imgur.com/EnUXKqL.png)
