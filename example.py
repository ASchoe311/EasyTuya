from TuyaAPI.TuyaAPI import TuyaAPI
from TuyaAPI.devices import Lights

if __name__ == "__main__":
    api = TuyaAPI("9ea9sk54a0k2978837d6", "d6034d97286c4b049ee16874a5a2d92d")
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
        elif toDo == "refresh":
            api.refreshAccessToken()
