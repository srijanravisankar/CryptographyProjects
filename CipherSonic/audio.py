import ggwave
import pyaudio

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
    p = pyaudio.PyAudio()

    stream = p.open(format=pyaudio.paFloat32, channels=1, rate=48000, input=True, frames_per_buffer=1024)

    print('Listening ... Press Ctrl+C to stop')
    instance = ggwave.init()

    ciphertext = None

    try:
        while True:
            data = stream.read(1024, exception_on_overflow=False)
            res = ggwave.decode(instance, data)
            if (not res is None):
                try:
                    ciphertext = res.decode("utf-8").strip()
                    print('Received text: ' + ciphertext)
                    break
                except:
                    pass
    except KeyboardInterrupt:
        pass

    ggwave.free(instance)

    stream.stop_stream()
    stream.close()

    p.terminate()

    return ciphertext