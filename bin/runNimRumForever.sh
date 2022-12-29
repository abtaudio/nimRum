#!/usr/bin/python3

import subprocess
import signal
import os
import sys
import sys

#### The idea is...
# In case of severe error (uncontrolled crash), then start a new process.
# Hopefully previous process will be cleaned up by the OS.
# Probably only useful if taking audio stream from some external source, like S/PDIF
# The idea is also to never really need this

#### This file can be triggered at boot by:
# sudo nano /etc/rc.local 
# Then add one of these to the end of that file:
# screen -d -m /usr/local/bin/runNimRumForever.sh /usr/local/bin/runNimRumTx.py
# screen -d -m /usr/local/bin/runNimRumForever.sh /usr/local/bin/runNimRumRx.py
#
# Depending on your installation these can come in handy:
# which ...
# pip show nimRum 
#
# Also, please put the tx|rxConfig.yaml-files in a folder named /root/nimRum/
#
# If you want to take a look at what is started in the background with screen, use:
# Connect to screen started by root:    sudo screen -r
# Leave screen:                         Ctrl-a + Ctrl-d
# Scroll inside screen:                 Ctrl-a + Esc

commandLine = sys.argv[1]

logLength = 10000
logFileName = "/var/log/runNimRumForever.log"

meStr = "**" + os.path.basename(__file__) + "**: "

logList = [None] * logLength
logCnt = 0
logWrap = 0
run = 1

def lclPrint(pStr):
    global meStr
    print(meStr + pStr)
    sys.stdout.flush()

def signal_handler(sig, frame):
    global run
    lclPrint ("Catched Ctrl-C")
    run = 0

signal.signal(signal.SIGINT, signal_handler)

def runCmd(cmd):
    global logList
    global logCnt
    global logLength
    global logWrap

    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while True:
        output = p.stdout.readline()
        if not output and p.poll() is not None:
            break
        if output:
            print (str(output.strip(), 'utf-8'))
            sys.stdout.flush()
            logList[logCnt] = output.strip()
            logCnt = logCnt + 1
            if logCnt >= logLength:
                logWrap = 1
                logCnt = 0

    rc = p.poll()
    return rc

def wrLog(logName):
    global logList
    global logCnt
    global logLength
    global logWrap

    f = open(logName, "w")
    if logWrap == 1:
        f.writelines("%s\n" % L for L in logList[logCnt:logLength])

    f.writelines("%s\n" % L for L in logList[0:logCnt])
    f.close()
    lclPrint ("Wrote: " + logName)


while run == 1:
    lclPrint ("***************************************************")
    lclPrint ("                    RESTART ")
    lclPrint ( "***************************************************")

    if os.path.exists(commandLine):
        runCmd(commandLine)
    else:
        lclPrint ("Could not find executable file")

    wrLog(logFileName)
