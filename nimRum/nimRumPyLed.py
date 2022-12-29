#!/usr/bin/python3

try:
    from gpiozero import LED
except:
    pass


class nimRumPyLed:
    def __init__(self, Rpin=12, Gpin=13, Bpin=26):

        self.ledAvailable = False
        try:
            self.ledR = LED(Rpin)
            self.ledG = LED(Gpin)
            self.ledB = LED(Bpin)
            self.ledAvailable = True
        except:
            print("nimRumPyLed NOT enabled")

        self.off()

    def off(self):
        if self.ledAvailable:
            self.ledR.off()
            self.ledG.off()
            self.ledB.off()

    def red(self):
        if self.ledAvailable:
            self.ledR.on()
            self.ledG.off()
            self.ledB.off()

    def green(self):
        if self.ledAvailable:
            self.ledR.off()
            self.ledG.on()
            self.ledB.off()

    def blue(self):
        if self.ledAvailable:
            self.ledR.off()
            self.ledG.off()
            self.ledB.on()

    def white(self):
        if self.ledAvailable:
            self.ledR.on()
            self.ledG.on()
            self.ledB.on()
