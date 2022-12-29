#!/usr/bin/python3

import os

from nimRum import nimRumRx

configFile = "./rxConfig.yaml"
if os.path.exists(configFile) == False:
    configFile = os.path.join(os.path.expanduser("~"), "nimRum/rxConfig.yaml")

rx = nimRumRx.nimRumRx(configFile=configFile)
nimRumRx.setMyself(rx)  # Trick for callback function
rx.runRx()
