#!/usr/bin/python3

import sys
import os

from nimRum import nimRumTx

soundFileName = None
if len(sys.argv) > 1:
    soundFileName = sys.argv[1]


configFile = "./txConfig.yaml"
if os.path.exists(configFile) == False:
    configFile = os.path.join(os.path.expanduser("~"), "nimRum/txConfig.yaml")

tx = nimRumTx.nimRumTx(configFile=configFile)
tx.runTx(fileName=soundFileName)
