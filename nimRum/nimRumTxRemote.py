#!/usr/bin/python3

# So many hours wasted on various internet tips.
# Ended up using this one: https://forums.raspberrypi.com/viewtopic.php?t=235256

# cat /etc/os-release -> bullseye
#
# sudo apt update
# sudo apt install lirc
#
# Edit /etc/lirc/lirc_options.conf as follows by changing these two lines:
# driver = default
# device = /dev/lirc0
#
# sudo nano /boot/config.txt
# dtoverlay=gpio-ir,gpio_pin=17
#
# pip3 install lirc
# sudo nano  /usr/lib/arm-linux-gnueabihf/python3.9/site-packages/lirc/paths.py
# Comment out
# #   try:
# #       os.unlink(os.path.join(HERE, '_client.so'))
# #   except PermissionError:
# #       pass
#
# sudo systemctl stop lircd.service
# sudo systemctl start lircd.service
# sudo systemctl status lircd.service
# sudo reboot

try:
    import lirc
except:
    pass


class nimRumTxRemote:
    def __init__(self):

        self.lircAvailable = False
        try:
            self.lircConn = lirc.LircdConnection(timeout=0.0001)
            self.lircConn.connect()
            self.lircAvailable = True
        except:
            print("nimRumTxRemote NOT enabled, reading " + __file__ + " migth help")

    def lircCheck(self):
        if not self.lircAvailable:
            return None

        try:
            keypress = self.lircConn.readline()
        except:
            return None

        if keypress != "" and keypress != None:

            data = keypress.split()
            # hexcode = data[0]
            repeat = data[1]
            command = data[2]
            remote = data[3]

            # ignore command repeats

            if remote == "LG_AKB72915207":
                if command == "KEY_VOLUMEUP":
                    self.volumeUp()

                if command == "KEY_VOLUMEDOWN":
                    self.volumeDown()

                if command == "KEY_MUTE":
                    if repeat != "00":
                        return None
                    self.volumeMuteToggle()

                if command == "KEY_RED":
                    if repeat != "00":
                        return None
                    self.latencyErrorToggle()

        return None
