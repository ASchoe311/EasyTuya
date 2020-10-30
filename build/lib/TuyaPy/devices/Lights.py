import requests as r
import json

redHSV = {'h': 0, 's': 255, 'v': 255}
yellowHSV = {'h': 60, 's': 255, 'v': 255}
greenHSV = {'h': 120, 's': 255, 'v': 255}
skyHSV = {'h': 180, 's': 255, 'v': 255}
blueHSV = {'h': 240, 's': 255, 'v': 255}
purpleHSV = {'h': 300, 's': 255, 'v': 255}
whiteHSV = {'h': 0, 's': 0, 'v': 255}

rainbowHSV = [redHSV, yellowHSV, greenHSV, skyHSV, blueHSV, purpleHSV]

def colorCommand(color = "white"):
    return {'commands': [{'code': 'work_mode', 'value': color}]}
    
def brightCommand(newBright):
    return {'commands': [{'code': 'bright_value', 'value': newBright}]}

def onCommand():
    return {'commands': [{'code': 'switch_led', 'value': True}]}

def offCommand():
    return {'commands': [{'code': 'switch_led', 'value': False}]}

def gorgCommand(bright = 255, freq = 191, hsvList = rainbowHSV):
    return {'commands': [{
                "code": "flash_scene_4",
                "value": {
                    "bright": bright,
                    "frequency": freq,
                    "hsv": hsvList,
                    "temperature": 0
                }
            }]}


class Light:

    def __init__(self, deviceID = None, deviceName = None):
        self.id = deviceID
        self.name = deviceName
        self.isOn = None
        self.workMode = None
        self.brightness = 0

    def toggleOnOff(self):
        if self.isOn:
            return offCommand()
        else:
            return onCommand()

    def postCommand(self, headerData, command):
        try:
            thisEnd = "https://openapi.tuyaus.com/v1.0/devices/[id]/commands".replace("[id]", self.id)
            resp = r.post(url=thisEnd, headers=headerData, data=json.dumps(command))
            if resp.json()['success'] == False:
                problem = "ERROR: Command failed, server response => " + json.dumps(resp.json())
                raise Exception(problem)
        except Exception as e:
            raise
        else:
            print(f"Ran command successfully:\n{command} on device named {self.name}")
            if command['commands'][0]['code'] == "switch_led":
                self.isOn = not self.isOn
            elif command['commands'][0]['code'] == "work_mode" or command['commands'][0]['code'].find("scene") != -1:
                self.workMode = command['commands'][0]['value']
            elif command['commands'][0]['code'] == "bright_value":
                self.brightness = command['commands'][0]['value']

        