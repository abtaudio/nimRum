
# nimRum (Nimble Rumble)

## What is this
This is an implementation of the **www.abtaudio.tech** solution. **Free for private use and evaluation purposes.**  

This implementation is limited to:  
    * **Raspberry Pi 2,3,4 / Raspbian GNU/Linux 11 (bullseye)**  
    * Max 8 clients/speakers (Enough for 7.1 or 5.2)  
    * Max 2 audio channels per client (1 audio channel per client is the normal case)  
    * No audio repair in case of packet loss  
    * Single local network


## What does it
A program/library to transmit wireless audio over WiFi/Ethernet.

The receiving speakers will play the audio in synch, just as if you connected them with wires, ..without mixing up + and -.

In other words, this solution is good enough for putting **multiple wireless speakers** in the same room, and let them **play toghether**, either for music, or as surround speakers.

This maybe sounds obvious, but this is NOT what most wireless speakers does today.

## What you need
* A couple of **Raspberry Pis 2|3|4** with
    * **Raspbian GNU/Linux 11 (bullseye)**

* All connected through a local network, where one of the Raspberries being the AP  
    * 5GHz WiFi has the perfect balance between range and radio interference for this purpose  
    * Ethernet cables works as well  

* The one configured as AP should be the transmitter  
    * As sound source, either use a local file or the Line-In|S/PDIF input from a soundcard.  
    * If transmitter has IR-sensor/LIRC, then volume/mute can be controlled from a remote.  

* The ones configured as receivers should have a soundcard with either line-out or direct speaker output  
    * The built in line-out on RPI is very noisy  
    * The transmitter can also be a receiver at the same time as long as the HW supports it  

* Recomended soundcards?
    * HifiBerry & IQAudio works fine, with or without built in amplifier
    * ...probably many others as well.

* Just a kind remark  
    If using line-in on a Bluetooth speaker, be aware that these probably adds something like 20-60ms delay.  
    This is ok for nimRum, you just need to adjust for it.  
    ...the problem is that I've noticed that this delay is not always constant.  

# Getting started
## The TX part:
1. pip3 install nimRum
2. runNimRumTx.py *aFileWithSound.wav* (This will play this file repeatedly, forever)

First time you will get a message telling you to create a txConfig.yaml file.
It will also tell where you find an example, with instructions, to copy. Most important to add are the *hostnames* of the RX devices and map correct audio channels to them.

## The RX part
1. pip3 install nimRum
2. runNimRumTx.py

First time it will use default settings. When you close (Ctrl-C) the program, it will store an example *rxConfig.last* file for you. Rename it to *rxConfig.yaml* to alter the default settings if needed.

Note: It will use the first 'hw:' sound device it finds. Please disable the others.  
    Hint:  
    # dtparam=audio=on  
    dtoverlay=vc4-kms-v3d -> dtoverlay=vc4-kms-v3d,noaudio
## Support
You will need some background knowledge to set this up. I am not saying it is hard, it is actually far from it. But you probably need some previous experience.

Please look in the provided python files, I've tried to make them readable.
'*which runNimRumTx.py*' will tell you where your installation is located.

# Getting further
## Streaming from Line-In|S/PDIF input
Start *runNimRumTx.py* without providing any input sound file.
It will then look for the first 'hw:' input sound device it finds.

## Start at boot
*runNimRumForever.sh* can be used to start automatically at boot. The file is located next to *runNimRumTx.py* and *runNimRumRx.py*. Instructions are found inside.
## In case you want to install nimRum to a virtuelenv
pip3 install virtualenv virtualenvwrapper

nano .bashrc
#Virtualenvwrapper settings:  
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3  
export WORKON_HOME=$HOME/.virtualenvs  
export VIRTUALENVWRAPPER_VIRTUALENV=~/.local/bin/virtualenv  
source ~/.local/bin/virtualenvwrapper.sh  
export VIRTUALENVWRAPPER_ENV_BIN_DIR=bin  

Login/Logout OR source ~/.bashrc

mkvirtualenv testPyNimRum

workon testPyNimRum

deactivate

# Getting involved
I myself do not have the possibility to give unlimited support to whatever question. If anyone like this to the level they would like to help others to install, improve the scripts, improve documentation, moderate some chat/forum, or in any other way get involved, then this is in line with what I want.  
BR,  
www.abtaudio.tech

## TODO

* Find all remaining bugs, specially those from my latest refactoring =)

* Replace libNimRumAlsaCapture_py.so  
    This is a library used to capture samples from an audio input and provide raw sample data for transmission. This has nothing to do with what AbtAudio focus on.  
    FFMPEG is a great tool, but using latest version instead of Bullseye default version would be better. Updating version becomes much easier if this is written directly in Python.

    The function it does can be explained with this (will spam your terminal forever):  
    >ffmpeg -f alsa -i hw -f wav - | ffmpeg -i - -y -f wav -  

    Try this if you want to understand what it does (will not spam your terminal forever):  
    >ffmpeg -t 20 -f alsa  -i hw -f wav - | ffmpeg   -i - -y t2.wav  

    In addition to just grab the samples, it is good to have low/known latency, not to mess up lip-synch.  
    It should also enable compensation for clock drift. Either by resample the incoming stream to local clock, or provide the exact rate to libNimRumTx_py.so  
    It should automatically detect if PCM or Encoded data, in best of worlds, without adding HW specific code.  
    ...maybe *import asyncio* is a good start?  

* Support any format for input files. Currently *nimRumTxReadFile_wavio.py* is used, which only supports .wav-format. *nimRumTxReadFile_soundfile.py* needs to be fixed.

* Add possibility to mix audio channels  
    Like rigth/left front to LFE channels (in case of small front speakers)  
    Merge left and rigth to a mono channel

* ...

## Working in development mode for pypi
git clone https://github.com/abtaudio/nimRum  
cd evaluate  
rm -rf dist  
pip3 install -e .  
python3 setup.py sdist  
twine upload dist/*  
