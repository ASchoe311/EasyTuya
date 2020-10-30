import requests as r
import time
from Crypto.Hash import HMAC, SHA256
import json

class TuyaAPI:

    def __init__(self):
        self.clientID = None
        self.accessKey = None
        self.APIHeader = {'client_id': None, 'sign': None, 'sign_method': "HMAC-SHA256", 't': None}
        self.devices = {}

    # Initialize an API connection with Tuya by passing your client ID and access secret as strings
    def __init__(self, id, secret):
        self.clientID = id
        self.accessKey = secret
        self.devices = {}
        try:
            t = str(time.time() * 1000)[:13]
            signature = HMAC.new(str.encode(self.accessKey), str.encode(self.clientID + t), digestmod=SHA256).hexdigest().upper()
            self.APIHeader = {'client_id': self.clientID, 'sign': signature, 'sign_method': "HMAC-SHA256", 't': t}
            resp = r.get(url="https://openapi.tuyaus.com/v1.0/token?grant_type=1", headers=self.APIHeader).json()
            self.tokenTimeLeft = resp['result']['expire_time']
            self.printConvertedTimeLeft(self.tokenTimeLeft)
            self.refreshToken = resp['result']['refresh_token']
            self.APIHeader['access_token'] = resp['result']['access_token']
            t = str(time.time() * 1000)[:13]
            self.APIHeader['sign'] = HMAC.new(str.encode(self.accessKey), str.encode(self.clientID + self.APIHeader['access_token'] + t), digestmod=SHA256).hexdigest().upper()
            self.APIHeader['t'] = t
        except Exception as e:
            raise

    # Refresh access token for API, must be done at least every 2 hours
    def refreshAccessToken(self):
        try:
            t = str(time.time() * 1000)[:13]
            signature = HMAC.new(str.encode(self.accessKey), str.encode(self.clientID + t), digestmod=SHA256).hexdigest().upper()
            self.APIHeader = {'client_id': self.clientID, 'sign': signature, 'sign_method': "HMAC-SHA256", 't': t}
            refURL = "https://openapi.tuyaus.com/v1.0/token/" + self.refreshToken
            resp = r.get(url=refURL, headers=self.APIHeader, params=None).json()
            self.tokenTimeLeft = resp['result']['expire_time']
            self.printConvertedTimeLeft(self.tokenTimeLeft)
            self.refreshToken = resp['result']['refresh_token']
            self.APIHeader['access_token'] = resp['result']['access_token']
            t = str(time.time() * 1000)[:13]
            self.APIHeader['sign'] = HMAC.new(str.encode(self.accessKey), str.encode(self.clientID + self.APIHeader['access_token'] + t), digestmod=SHA256).hexdigest().upper()
            self.APIHeader['t'] = t
        except Exception as e:
            print(resp, e)
            #raise

    def printConvertedTimeLeft(self, seconds):
	    hours = int(seconds / 3600)
	    minutes = int((seconds / 60) - hours * 60)
	    seconds = seconds % 60
	    print(f"Time until key expiry: {hours} Hours, {minutes} Minutes, {seconds} Seconds")
    
    def addDevice(self, device, deviceGroup):
        if deviceGroup not in self.devices.keys():
            self.devices[deviceGroup] = [device]
        else:
            self.devices[deviceGroup].append(device)

    def addDevices(self, devices, deviceGroup):
        if type(devices) is not list:
            raise Exception("ERROR: Type of \"devices\" argument must be \"list\"")
        elif deviceGroup not in self.devices.keys():
            self.devices[deviceGroup] = devices
        else:
            self.devices[deviceGroup] = self.devices[deviceGroup] + devices

    def sendGroupCommand(self, destGroup, commands):
        if type(destGroup) is not str:
            raise Exception("ERROR: destination group must be passed as string")
        elif destGroup not in self.devices.keys():
            raise Exception("ERROR: destination group must correspond to a group added with addDevice() or addDevices()")
        else:
            try:
                for d in self.devices[destGroup]:
                    d.postCommand(self.APIHeader, commands)
            except Exception as e:
                if str(e).find("ERROR: Command failed") != -1:
                    self.refreshAccessToken()
                    self.sendGroupCommand(destGroup, commands)
                else: raise

    def sendIndivCommand(self, destDevice, commands):
        try:
            destDevice.postCommand(self.APIHeader, commands)
        except Exception as e:
            if str(e).find("ERROR: Command failed") != -1:
                self.refreshAccessToken()
                self.sendIndivCommand(destDevice, commands)
            else: raise