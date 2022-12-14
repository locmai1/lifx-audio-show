import time
import numpy as np
import pyaudio
import config
import led

p = pyaudio.PyAudio()

# Fetch user's choice of microphone input for visualization
print('\nAudio Devices:')
for i in range(p.get_device_count()):
    device = p.get_device_info_by_index(i)
    if (device['hostApi'] == 0):
        print("    %s : %d" % (device['name'], device['index']))
input_device = int(input('\nInput Device: '))
print('')

frames_per_buffer = int(config.MIC_RATE / config.FPS)
stream = p.open(format=pyaudio.paInt16,
                input_device_index=input_device,
                channels=1,
                rate=config.MIC_RATE,
                input=True,
                frames_per_buffer=frames_per_buffer)
overflows = 0
prev_ovf_time = time.time()

def start_stream(callback):
    # p = pyaudio.PyAudio()

    # print('\nAudio Devices:')
    # for i in range(p.get_device_count()):
    #     device = p.get_device_info_by_index(i)
    #     if (device['hostApi'] == 0):
    #         print("    %s : %d" % (device['name'], device['index']))
    # input_device = int(input('Which to use: '))
    # print('')

    # frames_per_buffer = int(config.MIC_RATE / config.FPS)
    # stream = p.open(format=pyaudio.paInt16,
    #                 input_device_index=input_device,
    #                 channels=1,
    #                 rate=config.MIC_RATE,
    #                 input=True,
    #                 frames_per_buffer=frames_per_buffer)
    # overflows = 0
    # prev_ovf_time = time.time()

    try:
        while True:
            try:
                y = np.fromstring(stream.read(frames_per_buffer, exception_on_overflow=False), dtype=np.int16)
                y = y.astype(np.float32)
                stream.read(stream.get_read_available(), exception_on_overflow=False)
                callback(y)
            except IOError:
                overflows += 1
                if time.time() > prev_ovf_time + 1:
                    prev_ovf_time = time.time()
                    print('Audio buffer has overflowed {} times'.format(overflows))
    except KeyboardInterrupt:
        # stream.stop_stream()
        # stream.close()
        # p.terminate()
        # led.off()
        stop_stream()

def stop_stream():
    stream.stop_stream()
    stream.close()
    p.terminate()
    led.off()
