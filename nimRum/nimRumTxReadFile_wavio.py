#!/usr/bin/python

import wavio


class nimRumTxReadFile:
    def __init__(self):
        pass

    def open(self, fileName):
        wav = wavio.read(fileName)

        sampleBytes = wav.sampwidth

        [self.bufLen, self.numOfChannels] = wav.data.shape
        if self.numOfChannels == None:
            self.numOfChannels = 1

        self.buf = wav.data.T

        print(
            "Read: [ Channels:{0}, SampleSize:{1} bytes, Rate:{2}Hz, Frames:{3}, Duration:{4} seconds ]".format(
                self.numOfChannels,
                sampleBytes,
                wav.rate,
                self.bufLen,
                self.bufLen / wav.rate,
            )
        )

        self.bufPos = 0

        return wav.rate, sampleBytes

    def read(self, frames):

        bufRemaning = self.bufLen - self.bufPos
        framesToRead = frames
        framesLeft = 0
        if bufRemaning < framesToRead:
            framesToRead = bufRemaning
            framesLeft = frames - framesToRead

        dataOut = [None] * self.numOfChannels
        ch = self.numOfChannels - 1
        while ch >= 0:
            dataOut[ch] = [0] * frames

            dataOut[ch][0:framesToRead] = self.buf[ch][
                self.bufPos : self.bufPos + framesToRead
            ]

            if framesLeft > 0:
                dataOut[ch][framesToRead : framesToRead + framesLeft] = self.buf[ch][
                    0:framesLeft
                ]

            ch = ch - 1

        self.bufPos = self.bufPos + frames
        self.bufPos = self.bufPos % self.bufLen

        return dataOut, self.numOfChannels
