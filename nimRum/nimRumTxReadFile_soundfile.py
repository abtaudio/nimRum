#!/usr/bin/python

import soundfile as sf


class nimRumTxReadFile:
    def __init__(self):
        pass

    def open(self, fileName):
        self.buf, self.samplerate = sf.read(fileName, always_2d=True, dtype="int16")
        sampleBytes = 2

        info = sf.info(fileName)
        print(info)

        """
        print(info.name)
        print(info.samplerate)
        print(info.channels)
        print(info.frames)
        print(info.duration)
        print(info.format)
        print(info.subtype)
        print(info.endian)
        print(info.format_info)
        print(info.subtype_info)
        print(info.sections)
        print(info.extra_info)
        """

        self.bufPos = 0
        self.bufLen = info.frames
        self.numOfChannels = info.channels

        return self.samplerate, sampleBytes

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

            dataOut[ch][0:framesToRead] = self.buf[
                self.bufPos : self.bufPos + framesToRead
            ][ch]

            if framesLeft > 0:
                dataOut[ch][framesToRead : framesToRead + framesLeft] = self.buf[
                    0:framesLeft
                ][ch]

            ch = ch - 1

        self.bufPos = self.bufPos + frames
        self.bufPos = self.bufPos % self.bufLen

        return dataOut, self.numOfChannels
