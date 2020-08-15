import numpy as np
import matplotlib.pyplot as plt

HEADER_LINES = 5
FILE_NAME = 'testing/1kHzcenter5ftT1.txt'
ampLeft = []
ampRight = []
time = []

# read from file, store values
with open(FILE_NAME, 'r') as f:
    for i in range(HEADER_LINES):
        next(f)
    for line in f:
        try:
            row = line.rstrip('\n')
            row = row.split('\t')
            time.append(float(row[0]))
            ampLeft.append(float(row[1]))
            ampRight.append(float(row[3]))
            # print(rw.split('\t'))
        except IndexError:
            pass

# from MATLAB code

# Physical Values
IN2M = 0.0254 # inches to meter conversion
c = 340.0 # m/s
d = 6*IN2M # m
fs = 48000 # Hz
ts = 1.0/fs
N = 10
maxTau = d/c
iStart = 0  # 0 instead of 1
sampWindow = int(maxTau/ts)
iStop = iStart + sampWindow # don't subtract 1, want 21 elements to match MATLAB code

# main loop
thetaMax = np.zeros(N)

while iStop < len(ampLeft):
    al = ampLeft[iStart:iStop]
    alhl = al
    ar = ampRight[iStart:iStop]
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

    theta = np.linspace(-90, 90, L)

    x = np.correlate(arhl, alhl, 'full')

    s = np.linspace(-L/2, L/2, L)

    iMax = x.argmax(axis=0)

    tauHat = s[iMax] * ts
    tauHat_ms = tauHat/(0.001)
    dist_inch = tauHat_ms * 0.001 * 340 * 39
    thetaHat = theta[iMax]
    thetaMax[0:N-1] = thetaMax[1:]
    thetaMax[N-1] = thetaHat
    thetaHat = np.mean(thetaMax)

    iStart = iStop
    iStop = iStart + sampWindow - 1
plt.plot(theta, x)
plt.show()