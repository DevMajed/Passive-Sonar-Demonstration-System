import sounddevice as sd
import numpy as np

# trying to test using earbuds microphone
# want to see contents of indata
# are the two channels the same?

def callback(indata, frames, time, status):
    # print("ADC time: ", time.inputBufferAdcTime)
    # print("current time: ", time.currentTime)
    # print("time difference: ", time.inputBufferAdcTime - time.currentTime)
    # Ldata = [indata[i][0] for i in range(len(indata))]
    # Rdata = [indata[j][1] for j in range(len(indata))]
    # print("L:")
    # print(Ldata)
    # print("R:")
    # print(Rdata)
    # print("Left channel matches right channel: ", np.array_equal(Ldata, Rdata))
    for i in range(len(indata)):
        Ldata = indata[i][0]
        Rdata = indata[i][1]
        if (Ldata != Rdata):
            print("Left and right channels are not equal!")
            print("Difference: ", Rdata - Ldata)
    print("####")

if __name__ == "__main__":
    device_info = sd.query_devices()

    stream = sd.InputStream(samplerate=44100, blocksize=0, device=32, channels=2, dtype=np.int16, latency="low", callback=callback)
    stream.start()
    stream.stop()