# A simple program to control a group of lights through command line input
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
            api.sendGroupCommand("LIGHTS", Lights.onCommand())
        elif toDo == "off":
            api.sendGroupCommand("LIGHTS", Lights.offCommand())
        elif toDo == "white":
            api.sendGroupCommand("LIGHTS", Lights.colorCommand("white"))
        elif toDo == "rainbow":
            api.sendGroupCommand("LIGHTS", Lights.gorgCommand(255, 191))
        elif toDo.split()[0] == "bright":
				# Expecting input to be in the form of "bright [val]"
				# where val is in the range 25 <= val <= 255
            api.sendGroupCommand("LIGHTS", Lights.brightCommand(int(toDo.split()[1])))
        elif toDo == "onoff":
            api.sendGroupCommand("LIGHTS", api.devices['LIGHTS'][0].toggleOnOff())
        elif toDo == "refresh":
            api.refreshAccessToken()
