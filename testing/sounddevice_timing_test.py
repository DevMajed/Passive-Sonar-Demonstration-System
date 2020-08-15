import sounddevice as sd
import numpy as np

currentTimeList = [0, 0]

def callback(indata, frames, time, status):
    print("1    ADC time: ", time.inputBufferAdcTime)
    print("1    current time: ", time.currentTime)
    print("1    time difference: ", time.inputBufferAdcTime - time.currentTime)
    currentTimeList[0] = time.currentTime
    print("1    device time difference: ", currentTimeList[0] - currentTimeList[1])
    print(indata[0][0])
    print("###############")

def callback2(indata, frames, time, status):
    print("2    ADC time: ", time.inputBufferAdcTime)
    print("2    current time: ", time.currentTime)
    print("2    time difference: ", time.inputBufferAdcTime - time.currentTime)
    currentTimeList[1] = time.currentTime
    print("2    device time difference: ", currentTimeList[1] - currentTimeList[0])
    print(indata[0][1])
    print("###############")


if __name__ == "__main__":
    device_info = sd.query_devices()

    stream = sd.InputStream(samplerate=44100, blocksize=2048, device=8, channels=2, dtype=np.int16, latency="low", callback=callback)
    stream2 = sd.InputStream(samplerate=44100, blocksize=2048, device=14, dtype=np.int16, latency="low", callback=callback2)
    stream.start()
    stream2.start()
    stream.stop()
    stream2.stop()