import pyaudio
import numpy as np
import time

CHUNK = 2**11   # 2048 frames per buffer
RATE = 44100

p=pyaudio.PyAudio()
stream=p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True,
              frames_per_buffer=CHUNK)

for i in range(int(10*44100/1024)): #go for a few seconds
    start = time.process_time()

    data = np.fromstring(stream.read(CHUNK),dtype=np.int16)
    print("update time = {0} ms".format((time.process_time() - start)*1000))  # end timer
    peak=np.average(np.abs(data))*2
    bars="#"*int(50*peak/2**16)
    print("%04d %05d %s"%(i,peak,bars))
    print("print time = {0} ms".format((time.process_time() - start)*1000))  # end timer

stream.stop_stream()
stream.close()
p.terminate()