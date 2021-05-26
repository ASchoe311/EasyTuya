class Camera:

    def __init__(self, deviceID: str, deviceName: str, base_url: str = "https://openapi.tuyaus.com"):
        """Initialize a new light type device

        Args:
            deviceID (str): The ID of the device, found through the Tuya cloud development interface
            deviceName (str): The custom name you would like to give the light
            base_url (str, optional): The Tuya API base URL. Choose the right one for your location. The default is 'https://openapi.tuyaus.com'
        """
        self.id = deviceID
        self.name = deviceName
        self.base_url = base_url.rstrip("/")  # use the url without trailing slashes
        self.ipc_workmode = 1
        self.deviceVolume = 5
        self.floodlightBrightness = 50
        self.wirelessBatteryLock = True
        self.siren = True
        self.zoomStop = False
        self.cryDetection = True
        self.soundDetection = True
        self.recording = False
        self.motionRecording = True
        self.statusLight = True
        self.timeMark = True
        self.moTrack = False
        

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
            thisEnd = self.base_url + "/v1.0/devices/[id]/commands".replace("[id]", self.id)
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
        