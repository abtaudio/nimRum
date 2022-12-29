#!/usr/bin/python3

import sys
import os

from nimRum import libNimRumTx_py as txLib
from nimRum import libNimRumAlsaCapture_py as capLib

from nimRum import nimRumPyCommon
from nimRum import nimRumTxReadFile_wavio
from nimRum import nimRumTxCfg
from nimRum import nimRumPyLed


class nimRumTx(nimRumPyCommon.nimRumPyCommon):
    def __init__(self, configFile="./txConfig.yaml"):
        nimRumPyCommon.nimRumPyCommon.__init__(self, meName=os.path.basename(__file__))

        self.cfg = nimRumTxCfg.nimRumTxCfg(
            self.volumeSet, self.latencySet, configFile=configFile
        )
        self.led = nimRumPyLed.nimRumPyLed()
        self.file = nimRumTxReadFile_wavio.nimRumTxReadFile()

    def volumeSet(self):
        for cliId in self.cfg.cliIds:
            txLib.c_libNimRumTxSetVolume(cliId, self.cfg.getVolume(cliId))

    def latencySet(self, cliId=None, error=0):
        if cliId == None:  # Set for all clients
            for cliId in self.cfg.cliIds:
                txLib.c_libNimRumTxSetLatency(cliId, self.cfg.getLatency(cliId) + error)
        else:  # Set for specific client
            txLib.c_libNimRumTxSetLatency(cliId, self.cfg.getLatency(cliId) + error)

    def assignChannels(self, activeChannels):
        for cliId in self.cfg.cliIds:
            chLst = [0]

            if activeChannels > 2:
                chLst = self.cfg.multiChannelMap[cliId]
            elif activeChannels == 2:
                chLst = self.cfg.stereoChannelMap[cliId]
            else:
                pass

            txLib.c_libNimRumTxSetChannel(cliId, chLst)

    def runTx(self, fileName=None):
        # INIT SOURCE TO PLAY
        bytePerSample = 2  # This is what libNimRumAlsaCapture supports
        sampleRate = 48000  # This is what libNimRumAlsaCapture supports

        if fileName == None:
            # INIT SPDIF INPUT
            frameStretchEnable = 1
            if capLib.c_libNimRumAlsaCapture_init(frameStretchEnable) != 0:
                self.lclPrint("CAPT init failed")
                quit()

        else:
            # OPEN INPUT FILE
            (sampleRate, bytePerSample) = self.file.open(fileName)

        # INIT TX
        if txLib.c_libNimRumTxInit(self.getMyUniqueId(), self.cfg.cliNames) != 0:
            self.lclPrint("TX Init failed")
            quit()

        (res, framesPerInterval) = txLib.c_libNimRumTxConfigure(
            bytePerSample, sampleRate
        )
        if res != 0:
            self.lclPrint("TX Cfg failed")
            quit()

        txLib.c_libNimRumTxLogs(self.cfg.logEnable)
        txLib.c_libNimRumTxSetLogsPath(self.cfg.logPath)

        self.latencySet()
        self.volumeSet()

        ###########################################################
        # LOOP FOREVER (Until Ctrl-C, or severe error)
        ###########################################################
        activeChannels = -1  # -1 to force initial configureation
        activeChannelsNew = 0
        dataValid = 0

        # INIT ARRAY FOR DATA TRANSFER
        maxChannels = 8
        dataOut = []
        while maxChannels > 0:
            dataOut.append(bytearray(4 * 2400))
            maxChannels = maxChannels - 1

        while self.run == 1:

            if fileName == None:
                # GET DATA - FROM SPDIF
                (
                    res,
                    samplesQueued,
                    activeChannelsNew,
                    layout,
                    frameTimeActual,
                    dataValid,
                ) = capLib.c_libNimRumAlsaCapture_getData(dataOut, framesPerInterval)

            else:
                # GET DATA - FROM FILE
                dataArr, activeChannelsNew = self.file.read(framesPerInterval)
                txLib.c_libNimRumTxListToBuf(dataArr, dataOut)

            # Ctrl LED, if any
            if (dataValid < 0) or (self.cfg.latencyError != 0):
                self.led.red()
            else:
                self.led.green()

            # UPDATE CHANNEL MAPPING IF NEEDED
            if activeChannels != activeChannelsNew:
                activeChannels = activeChannelsNew
                self.assignChannels(activeChannels)

            # SEND DATA
            # totFrameTime_ns = int(round(frameTimeActual * numOfFrames))
            totFrameTime_ns = 0
            txLib.c_libNimRumTxProcess(dataOut, framesPerInterval, totFrameTime_ns)

            # CHECK REMOTE
            self.cfg.lircCheck()

        ###########################################################
        # CLEAN UP
        ###########################################################
        self.led.off()
        capLib.c_libNimRumAlsaCapture_close()
        txLib.c_libNimRumTxClose()

        self.lclPrint("TX Done")


###########################################################
#### MAIN ####
###########################################################
if __name__ == "__main__":

    fileName = None
    if len(sys.argv) > 1:
        fileName = sys.argv[1]

    t = nimRumTx(configFile="./txConfig.yaml")
    t.runTx(fileName=fileName)
