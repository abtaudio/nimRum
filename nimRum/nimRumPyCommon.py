#!/usr/bin/python3

import sys
import signal
import socket
import re
import socket
import os

import netifaces as ni


class nimRumPyCommon:
    def __init__(self, meName=os.path.basename(__file__)):

        self.meStr = "**" + meName + "**: "

        self.run = 1
        signal.signal(signal.SIGINT, self.signal_handler)

        try:
            self.myName = socket.gethostname()
        except:
            self.myName = "Unknown1"

        try:
            self.myId = int(re.findall(r"\d+", self.myName)[0])
        except:
            self.myId = 666

    def lclPrint(self, pStr):
        print(self.meStr + pStr)
        sys.stdout.flush()

    def signal_handler(self, sig, frame):
        self.lclPrint("Catched Ctrl-C, stopping")
        self.run = 0

    def getMyUniqueName(self):
        return self.myName

    def getMyUniqueId(self):
        return self.myId

    def getBCAddr(self, nicName):
        try:
            useLocalClock = 0
            bcastAddr = ni.ifaddresses(nicName)[ni.AF_INET][0]["broadcast"]
            if nicName == "lo":
                useLocalClock = 1
        except:
            self.lclPrint("'nic' must be one of the following:")
            self.lclPrint(str(ni.interfaces()))
            quit()

        self.lclPrint("BCAddr:" + str(bcastAddr))
        return bcastAddr, useLocalClock
