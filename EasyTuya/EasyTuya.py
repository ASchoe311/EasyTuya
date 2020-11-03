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
            self.tokenGetTime = time.time()
            #self.printConvertedTimeLeft(self.tokenTimeLeft)
            self.refreshToken = resp['result']['refresh_token']
            self.APIHeader['access_token'] = resp['result']['access_token']
            self.refreshSignature()
        except Exception as e:
            raise

    # Refreshes the signature in the API head with a new time
    # Needs to be done approximately every 10-20 minutes
    def refreshSignature(self):
        t = str(time.time() * 1000)[:13]
        self.APIHeader['sign'] = HMAC.new(str.encode(self.accessKey), str.encode(self.clientID + self.APIHeader['access_token'] + t), digestmod=SHA256).hexdigest().upper()
        self.APIHeader['t'] = t
        self.signatureGetTime = time.time()

    # Refresh access token for API, must be done every 2 hours to maintain API access
    def refreshAccessToken(self):
        try:
            t = str(time.time() * 1000)[:13]
            signature = HMAC.new(str.encode(self.accessKey), str.encode(self.clientID + t), digestmod=SHA256).hexdigest().upper()
            self.APIHeader = {'client_id': self.clientID, 'sign': signature, 'sign_method': "HMAC-SHA256", 't': t}
            refURL = "https://openapi.tuyaus.com/v1.0/token/" + self.refreshToken
            resp = r.get(url=refURL, headers=self.APIHeader, params=None).json()
            self.tokenTimeLeft = resp['result']['expire_time']
            self.tokenGetTime = time.time()
            #self.printConvertedTimeLeft(self.tokenTimeLeft)
            self.refreshToken = resp['result']['refresh_token']
            self.APIHeader['access_token'] = resp['result']['access_token']
            refreshSignature()
        except Exception as e:
            raise

    # Prints the amount of time left until access token must be refreshed
    def printConvertedTimeLeft(self):
	    hours = int(self.tokenTimeLeft / 3600)
	    minutes = int((self.tokenTimeLeft / 60) - hours * 60)
	    seconds = self.tokenTimeLeft % 60
	    print(f"Time until key expiry: {hours} Hours, {minutes} Minutes, {seconds} Seconds")
    
    # Takes in either a single device or a list of devices
    # Devices are objects defined in EasyTuya.devices such as Lights
    def addDevices(self, devices, identifier):
        if identifier not in self.devices.keys():
            self.devices[identifier] = devices
        else:
            if type(devices) is not list:
                self.devices[identifier].append(devices)
            else:
                self.devices[identifier] += devices
        self.__initStatus(identifier)
    
    def sendCommands(self, destIdentifier, commands):
        if time.time() - self.tokenGetTime >= self.tokenTimeLeft:
            self.refreshAccessToken()
        elif time.time() - self.signatureGetTime >= 600:
            self.refreshSignature()
        if type(destIdentifier) is not str:
            raise Exception("ERROR: Command destination identifier must be passed as string")
        if destIdentifier not in self.devices.keys():
            raise Exception("ERROR: Command destination identifier must correspond to a device or group of devices added with addDevice() or addDeviceGroup()")
        try:
            if type(self.devices[destIdentifier]) != list:
                self.devices[destIdentifier].postCommand(self.APIHeader, commands)
            else:
                for d in self.devices[destIdentifier]:
                    d.postCommand(self.APIHeader, commands)
        except Exception as e:
            raise

    def __initStatus(self, destID):
        try:
            statuses = self.getStatus(destID)
        except Exception as e:
            raise Exception("Something went wrong while initializing your devices")
        else:
            for d in statuses.keys():
                d.setStatusInfo(statuses[d])

    def getStatus(self, destIdentifier):
        if time.time() - self.tokenGetTime >= self.tokenTimeLeft:
            self.refreshAccessToken()
        elif time.time() - self.signatureGetTime >= 600:
            self.refreshSignature()
        if type(destIdentifier) is not str:
            raise Exception("ERROR: Status destination identifier must be passed as string")
        if destIdentifier not in self.devices.keys():
            raise Exception("ERROR: Status destination identifier must correspond to a device or group of devices added with addDevice() or addDeviceGroup()")
        try:
            statusURL = "https://openapi.tuyaus.com/v1.0/devices/[id]/status"
            if type(self.devices[destIdentifier]) != list:
                thisURL = statusURL.replace('[id]', self.devices[destIdentifier].id)
                resp = r.get(thisURL, headers=self.APIHeader).json()
                return {self.devices[destIdentifier]: resp['result']}
            else:
                statusList = {}
                for d in self.devices[destIdentifier]:
                    thisURL = statusURL.replace('[id]', d.id)
                    resp = r.get(thisURL, headers=self.APIHeader).json()
                    statusList[d] = resp['result']
                return statusList
        except Exception as e:
            raise