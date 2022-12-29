#!/usr/bin/python3

import os
import sys
import yaml

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

from nimRum import nimRumTxRemote


class nimRumTxCfg(nimRumTxRemote.nimRumTxRemote):
    def __init__(
        self,
        volumeCallback,
        latencyCallback,
        configFile="./txConfig.yaml",
        cliIdErrorInsertion=2,
    ):
        nimRumTxRemote.nimRumTxRemote.__init__(self)

        self.volumeCallback = volumeCallback
        self.latencyCallback = latencyCallback
        self.configFile = configFile
        self.cliIdErrorInsertion = cliIdErrorInsertion

        try:
            cfgFile = open(configFile)
            self.cfg = yaml.load(cfgFile, Loader=Loader)["nimRumTXConfig"]
            cfgFile.close()
            print("Read: " + configFile)
        except:
            print("Failed opening TX configuration file: " + configFile)
            whereAmI = os.path.dirname(os.path.abspath(__file__))
            print(" You can find an example here: " + whereAmI + "/txConfig.yaml")
            quit()

        self.volume = self._getTxVal("mainVolume", default=10)
        self.latency = self._getTxVal("latency_us", default=100000)
        self.logEnable = self._getTxVal("logEnable", default=0)
        self.logPath = self._getTxVal(
            "logPath", default=os.path.dirname(os.path.abspath(configFile))
        )

        self.clientData = self._getTxVal("clients", default=[])

        self.numOfCli = len(self.clientData)
        self.cliIds = list(range(0, self.numOfCli))

        self.cliNames = self._getCliVals("name", default="Missing")
        self.cliLocation = self._getCliVals("location")
        self.cliVolume = self._getCliVals("volume", default=100)
        self.cliLatencyOffset = self._getCliVals("offset_us", default=0)

        self.multiChannelMap = self._getCliVals("multiChannel", default=[])
        self.stereoChannelMap = self._getCliVals("stereoChannel", default=[])

        self.latencyError = 0
        self.muteEnable = 0

        self.printCfg()
        sys.stdout.flush()

    def _getTxVal(self, keyName, default=None):
        res = default
        if keyName in self.cfg:
            res = self.cfg[keyName]
        else:
            print("Using default value for: " + keyName + " = " + str(default))

        return res

    def _getCliVals(self, keyName, default=None):
        res = []
        for d in self.clientData:
            if keyName in d:
                res.append(d[keyName])
            else:
                print(
                    "Using default value for client number "
                    + d
                    + " : "
                    + keyName
                    + " = "
                    + str(default)
                )
                res.append(default)
        return res

    def _printList(self, name, L):
        print("".join("{0:<15}".format(str(k)) for k in [name] + L))

    def printCfg(self):
        print("#### txConfig:")
        self._printList("Index:", self.cliIds)
        self._printList("Name:", self.cliNames)
        self._printList("Location:", self.cliLocation)
        self._printList("Volume:", self.cliVolume)
        self._printList("Offset:", self.cliLatencyOffset)
        self._printList("Stereo mode:", self.stereoChannelMap)
        self._printList("Multi mode:", self.multiChannelMap)
        print("####")

    def volumeUp(self):
        if self.muteEnable == 0:
            self.volume = self.volume + 1
            if self.volume > 100:
                self.volume = 100
        else:
            self.volume = self.muteEnable
            self.muteEnable = 0

        self.volumeCallback()

    def volumeDown(self):
        if self.muteEnable == 0:
            self.volume = self.volume - 1
            if self.volume < 0:
                self.volume = 0
        else:
            self.volume = self.muteEnable
            self.muteEnable = 0

        self.volumeCallback()

    def volumeMuteToggle(self):
        # Stores last volume setting in muteEnable
        if self.muteEnable == 0:
            self.muteEnable = self.volume
            self.volume = 0
        else:
            self.volume = self.muteEnable
            self.muteEnable = 0

        self.volumeCallback()

    def latencyErrorToggle(self):
        if self.latencyError == 0:
            self.latencyError = 100
        elif self.latencyError == 100:
            self.latencyError = 500
        elif self.latencyError == 500:
            self.latencyError = 1000
        elif self.latencyError == 1000:
            self.latencyError = 2000
        elif self.latencyError == 2000:
            self.latencyError = 0

        print(
            "#### "
            + self.cliNames(self.cliIdErrorInsertion)
            + ", error insertion: "
            + str(self.latencyError)
        )
        self.latencyCallback(cliId=self.cliIdErrorInsertion, error=self.latencyError)

    def getVolume(self, cliId):
        volMain = self.volume / 100.0
        volCli = self.cliVolume[cliId] / 100.0
        vol = int(round(100 * (volMain * volCli)))
        return vol

    def getLatency(self, cliId):
        lat = self.latency + self.cliLatencyOffset[cliId]
        return lat
