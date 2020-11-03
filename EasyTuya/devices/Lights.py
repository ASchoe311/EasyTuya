import requests as r
import json

"""Pre-formed HSV for red color"""
redHSV = {'h': 0, 's': 255, 'v': 255}
"""Pre-formed HSV for yellow color"""
yellowHSV = {'h': 60, 's': 255, 'v': 255}
"""Pre-formed HSV for green color"""
greenHSV = {'h': 120, 's': 255, 'v': 255}
"""Pre-formed HSV for sky blue color"""
skyHSV = {'h': 180, 's': 255, 'v': 255}
"""Pre-formed HSV for normal blue color"""
blueHSV = {'h': 240, 's': 255, 'v': 255}
"""Pre-formed HSV for puprle color"""
purpleHSV = {'h': 300, 's': 255, 'v': 255}
"""Pre-formed HSV for white color"""
whiteHSV = {'h': 0, 's': 0, 'v': 255}

"""Pre-formed HSV list of full color spectrum for use with scenes where colors change"""
rainbowHSV = [redHSV, yellowHSV, greenHSV, skyHSV, blueHSV, purpleHSV]

def workModeCommand(wMode = "white"):
    """Generates a command to set the work mode of lights
    
    Returns:
        dict: The formed command to set the work mode of lights

    Args:
        wMode (str, optional): A string corresponding to one of the working modes outlined in the Tuya API documentation. Defaults to "white".
    """
    return {'commands': [{'code': 'work_mode', 'value': wMode}]}

def colorCommand(colorHSV: dict):
    """Generates a command to set the color of lights
    
    Returns:
        dict: The formed command to set the color of lights

    Args:
        colorHSV (dict): The HSV representing desired color

    Raises:
        Exception: Raises exception if color is not in proper HSV format
    """
    if type(colorHSV) is not dict or 'h' not in colorHSV.keys() or 's' not in colorHSV.keys() or 'v' not in colorHSV.keys():
        raise Exception("Colors must be given as HSV in the form {'h': h, 's': s, 'v', v}")
    return {'commands': [{'code': 'colour_data', 'value': colorHSV}]}

def temperatureCommand(newTemperature: int):
    """Generates a command to set the temperature of lights
    
    Returns:
        dict: The formed command to set the color temperature of lights

    Args:
        newTemperature (int): Integer value between 25 and 255, inclusive, representing color temperature

    Raises:
        Exception: Raises exception if newTemperature is outside the range [25,255]
    """
    if newTemperature < 25 or newTemperature > 255:
        raise Exception("Values for temperature must be within the range [25,255], inclusive")
    return {'commands': [{'code': 'temp_value', 'value': newTemperature}]}
    
def brightnessCommand(newBright: int):
    """Generates a command to set the brightness of lights

    Returns:
        dict: The formed command to set the brightness of lights

    Args:
        newBright (int): Integer value between 25 and 255, inclusive, representing brightness

    Raises:
        Exception: Raises exception if newBright is outside the range [25,255]
    """
    if newBright < 25 or newBright > 255:
        raise Exception("Values for brightness must be within the range [25,255], inclusive")
    return {'commands': [{'code': 'bright_value', 'value': newBright}]}

def onCommand():
    """Generates a command to turn on lights
    
    Returns:
        dict: The formed command to turn on lights
    """
    return {'commands': [{'code': 'switch_led', 'value': True}]}

def offCommand():
    """Generates a command to turn off lights

    Returns:
        dict: The formed command to turn off lights
    """
    return {'commands': [{'code': 'switch_led', 'value': False}]}

def sceneCommand(sceneNum = 4, bright = 255, freq = 191, hsvList = rainbowHSV):
    """Generates a command to set the scene mode of lights
    
    Returns:
        dict: The formed command to set the scene

    Args:
        sceneNum (int, optional): The scene number corresponding to desired effects, between 1 and 4. 
                                  See Tuya API documentation for more information on what each scene number means.
                                  Defaults to 4.
        bright (int, optional): Brightness of the lights during the scene. Defaults to 255 (maximum).
        freq (int, optional): Frequency of light changes from scene. Can be between 25 and 255, inclusive. Defaults to 191.
        hsvList (list, optional): List of HSVs representing colors for the scene. Defaults to rainbowHSV.

    """
    cmdCode = "flash_scene_" + str(sceneNum)
    return {'commands': [{
                "code": cmdCode,
                "value": {
                    "bright": bright,
                    "frequency": freq,
                    "hsv": hsvList,
                    "temperature": 0
                }
            }]}


class Light:

    def __init__(self, deviceID: str, deviceName: str):
        """Initialize a new light type device

        Args:
            deviceID (str): The ID of the device, found through the Tuya cloud development interface
            deviceName (str): The custom name you would like to give the light
        """
        self.id = deviceID
        self.name = deviceName
        self.isOn = None
        self.workMode = None
        self.brightness = 0

    def toggleOnOff(self):
        """Generates the right on/off command based on current vals
        Returns:
            dict: Either the command to turn on or to turn off lights 
        """
        if self.isOn:
            return offCommand()
        else:
            return onCommand()

    def postCommand(self, headerData: dict, command: dict):
        """Sends a post request to Tuya API for this device affecting it with the given command

        Args:
            headerData (dict): The data needed for the header to be sent to Tuya API
            command (dict): The command to affect the device with

        Raises:
            Exception: Raises an exception on a failed call to Tuya API
        """
        try:
            thisEnd = "https://openapi.tuyaus.com/v1.0/devices/[id]/commands".replace("[id]", self.id)
            resp = r.post(url=thisEnd, headers=headerData, data=json.dumps(command))
            if resp.json()['success'] == False:
                problem = "ERROR: Command failed, server response => " + json.dumps(resp.json())
                raise Exception(problem)
        except Exception as e:
            raise
        else:
            #print(f"Ran command successfully:\n{command} on device named {self.name}")
            if command['commands'][0]['code'] == "switch_led":
                self.isOn = not self.isOn
            elif command['commands'][0]['code'] == "work_mode" or command['commands'][0]['code'].find("scene") != -1:
                self.workMode = command['commands'][0]['value']
            elif command['commands'][0]['code'] == "bright_value":
                self.brightness = command['commands'][0]['value']

    def setStatusInfo(self, statusInfo: list):
        """Sets the status related variables of this device to the retrieved information from Tuya API. Only used for initializing a device

        Args:
            statusInfo (list): The list contained in the json response to a device status request at the dictionary key 'result'
        """
        self.isOn = statusInfo[0]['value']
        self.workMode = statusInfo[1]['value']
        self.brightness = statusInfo[2]['value']

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name
        