import sounddevice #pip install sounddevice

#sounddevice.default.device = "aggregate device"
#sounddevice.default.channels = 2

for i in range(30): #30 updates in 1 second
    rec = sounddevice.rec(44100/30)
    sounddevice.wait()
    print(rec.shape)