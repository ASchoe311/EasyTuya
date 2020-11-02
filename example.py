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
