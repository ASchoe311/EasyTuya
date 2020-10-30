# TuyaPy - Making IOT Control With Python Easy

TuyaPy is a module containing nearly all needed functionality for interacting with your Tuya powered IOT devices through Python. This is done using [Tuya's web API](https://developer.tuya.com/en/docs/iot/open-api/api-list/api?id=K989ru6gtvspg), meaning that for this module to work you will need a cloud developer account on Tuya's website. Full instructions for this and general setup can be found below. If you have not already, to use this you must also download the TuyaSmart app on your phone and add your compatible devices.

# Installation

    pip3 install TuyaPy
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

    from TuyaAPI.TuyaAPI import TuyaAPI
    from TuyaAPI.devices import Lights
    
    if __name__ == "__main__":
        api = TuyaAPI("your_client_id", "your_access_secret")
        l1 = Lights.Light("64304636a4cf12d76aad", "Light 1")
        l2 = Lights.Light("55008855483fdac28931", "Light 2")
        api.addDevices([l1, l2], "BRLIGHTS")
        while(True):
            toDo = input()
            if toDo == "on":
                api.sendGroupCommand("BRLIGHTS", Lights.onCommand())
            elif toDo == "off":
                api.sendGroupCommand("BRLIGHTS", Lights.offCommand())
            elif toDo == "white":
                api.sendGroupCommand("BRLIGHTS", Lights.whiteCommand())
            elif toDo == "rainbow":
                api.sendGroupCommand("BRLIGHTS", Lights.gorgCommand())
            elif toDo.split()[0] == "bright":
                print(toDo.split()[1])
                api.sendGroupCommand("BRLIGHTS", Lights.brightCommand(int(toDo.split()[1])))
            elif toDo == "onoff":
                if(api.devices['BRLIGHTS'][0].isOn == False):
                    api.sendGroupCommand("BRLIGHTS", Lights.onCommand())
                else:
                    api.sendGroupCommand("BRLIGHTS", Lights.offCommand())
               
# Other Notes
### Finding Device IDs
To find your device IDs, go to:
Tuya developer site -> Device Management -> Device List
Select your correct country from the drop down near the center of the page, then your devices should show up each with their name displayed above their device id, as shown in the following image.
![The device list page](https://i.imgur.com/EnUXKqL.png)
