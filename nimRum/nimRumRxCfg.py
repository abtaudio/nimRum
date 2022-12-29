#!/usr/bin/python3

import os
import yaml

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


class nimRumRxCfg:
    def __init__(self, configFile="./rxConfig.yaml"):

        try:
            cfgFile = open(configFile)
            self.cfg = yaml.load(cfgFile, Loader=Loader)
            cfgFile.close()
            self.usefulPath = os.path.dirname(os.path.abspath(configFile))
            print("Read: " + configFile)
        except:
            print("****************************************************************")
            print("Failed opening RX configuration file: " + configFile)
            print("  No worries. There will be one written when lib is closed down")
            print("  You just need to rename it to rxConfig.yaml")
            print("****************************************************************")
            self.cfg = {}
            self.cfg["nimRumRXConfig"] = {}
            self.usefulPath = os.getcwd()

        self._setDefault("nic", default="wlan0")
        self._setDefault("staticDelay_us", default=0)
        self._setDefault("outputChannelEnable", default=3)
        self._setDefault("logEnable", default=0)
        self._setDefault("logPath", default=self.usefulPath)

    def _setDefault(self, keyName, default=None):
        if not keyName in self.cfg["nimRumRXConfig"]:
            print("Using default value for: " + keyName + " = " + str(default))
            self.cfg["nimRumRXConfig"][keyName] = default

    def get(self, keyName):
        return self.cfg["nimRumRXConfig"][keyName]

    def alterDelay(self, diff):
        val = self.get("staticDelay_us") + diff
        self.cfg["nimRumRXConfig"]["staticDelay_us"] = val

    def dump(self):

        helpStr = """
#
# This file should have the following name: rxConfig.yaml
# Either store it in:
#   1. The same folder where you found this file (rxConfig.last)
#   2. $HOME/nimRum
#
# nic:
#   Select a NIC. This is where a broadcast message will be sent
#   to get in touch with TX. This NIC will then be used for transmission.
#   lo | eth0 | wlan0 | ...
#
# staticDelay_us: 
#   Add a static latency offset
#
# outputChannelEnable:
#   Binary coded enable for audio out
#   3 = 2'b11 = channel0 and channel1 is enabled
#   Most soundcards has 2 (stereo outputs), so 3 is probably a good value
#   In case of only using one channel to connect to a speaker,
#   then this parameter can help saving the unused amplifier output
#

"""

        fileName = os.path.join(self.usefulPath, "rxConfig.last")

        try:
            file = open(fileName, "w")
            file.write(helpStr)
            yaml.dump(self.cfg, file)
            file.close()
        except:
            print("Failed writing: " + fileName)
