import numpy as np

class Localization():
    """
    Class containing localization function
    """

    def __init__(self, sampleRate):
        IN2M = 0.0254 # inches to meter conversion
        self.c = 340.0 # m/s
        self.d = 6*IN2M # m
        self.fs = 48000 # Hz
        self.ts = 1.0/self.fs
        self.N = 10
        self.maxTau = self.d/self.c
        self.iStart = 0  # 0 instead of 1
        self.sampWindow = int(self.maxTau/self.ts)
        self.iStop = self.iStart + self.sampWindow # don't subtract 1, want 21 elements to match MATLAB code
        self.x = [0 for i in range(41)]
        self.theta = np.linspace(-90, 90, 41)

    def runLocalization(self, left, right):
        thetaMax = np.zeros(self.N)
        iStart = self.iStart
        iStop = self.iStop

        while iStop < len(left):
            al = left[self.iStart:self.iStop]
            alhl = al
            ar = right[self.iStart:self.iStop]
            arhl = ar

            for i in range(len(arhl)):
                # left
                if alhl[i] >= 0:
                    alhl[i] = 1
                else:
                    alhl[i] = -1
                # right
                if arhl[i] >= 0:
                    arhl[i] = 1
                else:
                    arhl[i] = -1

            L = len(al) + len(ar) - 1

            # these are plotted
            self.theta = np.radians(np.linspace(-90, 90, L))
            # for i in range(len(self.theta)):
            #     if self.theta[i] < 0:
            #         self.theta[i] = 360.0 + self.theta[i]
            self.x = np.correlate(arhl, alhl, 'full')
            

            s = np.linspace(-L/2, L/2, L)

            iMax = self.x.argmax(axis=0)

            tauHat = s[iMax] * self.ts
            tauHat_ms = tauHat/(0.001)
            dist_inch = tauHat_ms * 0.001 * 340 * 39
            thetaHat = self.theta[iMax]
            thetaMax[0:self.N-1] = thetaMax[1:]
            thetaMax[self.N-1] = thetaHat
            self.thetaHat = np.degrees(np.mean(thetaMax))

            # print(self.theta)

            iStart = iStop
            iStop = iStart + self.sampWindow - 1
            # print(thetaHat)