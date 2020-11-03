import requests as r
import time
from Crypto.Hash import HMAC, SHA256
import json

class TuyaAPI:

    def __init__(self):
        self.clientID = None
        self.__accessKey = None
        self.__APIHeader = {'client_id': None, 'sign': None, 'sign_method': "HMAC-SHA256", 't': None}
        self.devices = {}

    def __init__(self, id: str, secret: str):
        """Initialize a connection with the Tuya API

        Args:
            id (str): Your Tuya developer account client id
            secret (str): Your Tuya developer account access secret
        """
        self.clientID = id
        self.__accessKey = secret
        self.devices = {}
        try:
            t = str(time.time() * 1000)[:13]
            signature = HMAC.new(str.encode(self.__accessKey), str.encode(self.clientID + t), digestmod=SHA256).hexdigest().upper()
            self.__APIHeader = {'client_id': self.clientID, 'sign': signature, 'sign_method': "HMAC-SHA256", 't': t}
            resp = r.get(url="https://openapi.tuyaus.com/v1.0/token?grant_type=1", headers=self.__APIHeader).json()
            self.tokenTimeLeft = resp['result']['expire_time']
            self.tokenGetTime = time.time()
            self.refreshToken = resp['result']['refresh_token']
            self.__APIHeader['access_token'] = resp['result']['access_token']
            self.refreshSignature()
        except Exception as e:
            raise

    def refreshSignature(self):
        """
        Refreshes the signature in the API head with a new time
        Needs to be done approximately every 10-20 minutes
        """
        t = str(time.time() * 1000)[:13]
        self.__APIHeader['sign'] = HMAC.new(str.encode(self.__accessKey), str.encode(self.clientID + self.__APIHeader['access_token'] + t), digestmod=SHA256).hexdigest().upper()
        self.__APIHeader['t'] = t
        self.signatureGetTime = time.time()

    def refreshAccessToken(self):
        """
        Refresh access token for API
        Must be done every 2 hours to maintain API access
        """
        try:
            t = str(time.time() * 1000)[:13]
            signature = HMAC.new(str.encode(self.__accessKey), str.encode(self.clientID + t), digestmod=SHA256).hexdigest().upper()
            self.__APIHeader = {'client_id': self.clientID, 'sign': signature, 'sign_method': "HMAC-SHA256", 't': t}
            refURL = "https://openapi.tuyaus.com/v1.0/token/" + self.refreshToken
            resp = r.get(url=refURL, headers=self.__APIHeader, params=None).json()
            self.tokenTimeLeft = resp['result']['expire_time']
            self.tokenGetTime = time.time()
            self.refreshToken = resp['result']['refresh_token']
            self.__APIHeader['access_token'] = resp['result']['access_token']
            refreshSignature()
        except Exception as e:
            raise

    def printConvertedTimeLeft(self):
        """Prints the amount of time left until access token must be refreshed"""
        hours = int(self.tokenTimeLeft / 3600)
        minutes = int((self.tokenTimeLeft / 60) - hours * 60)
        seconds = self.tokenTimeLeft % 60
        print(f"Time until key expiry: {hours} Hours, {minutes} Minutes, {seconds} Seconds")
    
    def addDevices(self, devices, identifier: str):
        """Adds devices to the device dictionary and gives them an easier identifier

        Args:
            devices (EasyTuya.devices): A single device object, from one of the devices in EasyTuya.devices, or a list of such objects with the same type.
            identifier (str): The identifier to give the added device(s)
        """
        if identifier not in self.devices.keys():
            self.devices[identifier] = devices
        else:
            if type(devices) is not list:
                self.devices[identifier].append(devices)
            else:
                self.devices[identifier] += devices
        self.__initStatus(identifier)
    
    def sendCommands(self, destIdentifier: str, commands: dict):
        """Send commands to all devices pointed to by destIdentifier

        Args:
            destIdentifier (str): The identifier corresponding to devices added with addDevices()
            commands (dict): The properly formatted commands to send the devices

        Raises:
            Exception: Raises an exception if destIdentifier is not a string
            Exception: Raises an exception if destIdentifier does not exist in devices dictionary
        """
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
                self.devices[destIdentifier].postCommand(self.__APIHeader, commands)
            else:
                for d in self.devices[destIdentifier]:
                    d.postCommand(self.__APIHeader, commands)
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

    def getStatus(self, destIdentifier: str):
        """Retrieves the statuses of all devices pointed to by destIdentifier
        returns 

        Args:
            destIdentifier (str): The identifier corresponding to devices added with addDevices()

        Raises:
            Exception: Raises an exception if destIdentifier is not a string
            Exception: Raises an exception if destIdentifier does not exist in devices dictionary

        Returns:
            dict: Device statuses in the form of {deviceObject: results[{}] }
        """
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
                resp = r.get(thisURL, headers=self.__APIHeader).json()
                return {self.devices[destIdentifier]: resp['result']}
            else:
                statusList = {}
                for d in self.devices[destIdentifier]:
                    thisURL = statusURL.replace('[id]', d.id)
                    resp = r.get(thisURL, headers=self.__APIHeader).json()
                    statusList[d] = resp['result']
                return statusList
        except Exception as e:
            raise