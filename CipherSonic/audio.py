import ggwave
import pyaudio
import threading

# global GGWave instance
ggwave_instance = None
lock = threading.Lock()

# enocde the message to sound waves
def encode_sound(ciphertext):
    p = pyaudio.PyAudio()

    waveform = ggwave.encode(ciphertext, protocolId = 1, volume = 20)

    print(f"Transmitting text '{ciphertext}' ...")
    stream = p.open(format=pyaudio.paFloat32, channels=1, rate=48000, output=True, frames_per_buffer=4096)
    stream.write(waveform, len(waveform)//4)
    stream.stop_stream()
    stream.close()

    p.terminate()

# decode the sound waves to message
def decode_sound():
    global ggwave_instance

    # ensure only one GGWave instance is created
    with lock:
        if ggwave_instance is None:
            ggwave_instance = ggwave.init()

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32, channels=1, rate=48000, input=True, frames_per_buffer=1024)

    ciphertext = None

    try:
        while True:
            data = stream.read(1024, exception_on_overflow=False)
            res = ggwave.decode(ggwave_instance, data)
            if res:
                try:
                    ciphertext = res.decode("utf-8").strip()
                    print('🎵 Received text:', ciphertext)
                    break
                except Exception as e:
                    print(f"❌ Decoding error: {e}")
    except KeyboardInterrupt:
        pass
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

    return ciphertext

# function to free GGWave instance when done
def free_ggwave():
    global ggwave_instance
    with lock:
        if ggwave_instance is not None:
            ggwave.free(ggwave_instance)
            ggwave_instance = None
