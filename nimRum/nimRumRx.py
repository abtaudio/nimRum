#!/usr/bin/python3

import os

from nimRum import libNimRumRx_py as rxLib

from nimRum import nimRumPyCommon
from nimRum import nimRumRxCfg
from nimRum import nimRumPyLed
from nimRum import nonBlockingConsole

global mySelf


# Trick for callback function
def setMyself(din):
    global mySelf
    mySelf = din


# Trick for callback function
def callbackWrapper(newState):
    global mySelf
    # print("Address of mySelf = ", id(mySelf), "  ", mySelf)
    return nimRumRx.callBack(mySelf, newState)


class nimRumRx(nimRumPyCommon.nimRumPyCommon):
    def __init__(self, configFile="./rxConfig.yaml"):
        nimRumPyCommon.nimRumPyCommon.__init__(self, meName=os.path.basename(__file__))

        self.cfg = nimRumRxCfg.nimRumRxCfg(configFile=configFile)
        self.led = nimRumPyLed.nimRumPyLed()
        self.kthread = nonBlockingConsole.NonBlockingConsole()

        # Used by TX for identification (channel mapping)
        self.myName = self.getMyUniqueName()
        self.myId = self.getMyUniqueId()

        self.bcastAddr, self.useLocalClock = self.getBCAddr(self.cfg.get("nic"))
        self.state = -10

        # Trick for callback function
        self.setDelay = rxLib.c_libNimRumRxSetStaticDelay

    def callBack(self, newState):
        # state: Tells how accurate the synch is.
        # -2: Not even getting packets
        # -1: Collecting data
        #  0, 1: The higher the better
        # +2: Now you can measure =)

        keyRead = self.kthread.get_data()
        if keyRead:
            if keyRead == "+":
                self.cfg.alterDelay(+100)
            if keyRead == "-":
                self.cfg.alterDelay(-100)
            self.setDelay(self.cfg.get("staticDelay_us"))

        if self.state != newState:
            self.state = newState
            self.lclPrint("State updated to: " + str(self.state))
            if self.state == -2:
                self.led.red()
            if self.state == -1:
                self.led.green()
            if self.state == 0:
                self.led.blue()
            if self.state == 1:
                self.led.white()
            if self.state == 2:
                self.led.off()

        if self.run == 0:
            return 0
        else:
            return 1

    def runRx(self):
        while self.run == 1:
            rxLib.c_libNimRumRxInit(
                self.bcastAddr,
                self.myId,
                self.myName,
                callbackWrapper,
                self.useLocalClock,
                self.cfg.get("outputChannelEnable"),
            )

            rxLib.c_libNimRumRxSetStaticDelay(self.cfg.get("staticDelay_us"))
            rxLib.c_libNimRumRxSetLogs(self.cfg.get("logEnable"))
            rxLib.c_libNimRumRxSetLogsPath(self.cfg.get("logPath"))

            res = rxLib.c_libNimRumRxStart()
            self.lclPrint("c_libNimRumRxStart returned " + str(res))
            rxLib.c_libNimRumRxClose()

            self.led.off()

        self.cfg.dump()


###########################################################
#### MAIN ####
###########################################################
if __name__ == "__main__":

    r = nimRumRx(configFile="./rxConfig.yaml")
    r.runRx()
