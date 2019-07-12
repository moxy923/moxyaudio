#First PyAudio thing.
import pyaudio
import wave
import time

audio = None
wavefile = None
_stream = None

def start_recording(filename, CHANNELS = 1, RATE = 44100, CHUNK = 1024):
    global audio
    global wavefile
    global _stream

    audio = pyaudio.PyAudio()

    wavefile = _prepare_file(filename, 'wb' )
    print wavefile

    #Use a stream with a callback in non-blocking mode 
    _stream = audio.open( format = pyaudio.paInt32,
            channels = CHANNELS,
            rate = RATE,
            input = True,
            frames_per_buffer = CHUNK,
            stream_callback = get_callback())
    
    _stream.start_stream()

    print "start_recording() > Recording started"

def get_callback():
    global wavefile

    def callback(in_data, frame_count, time_info, status):
        wavefile.writeframes(in_data)
        return in_data, pyaudio.paContinue
    return callback

def stop_recording():
    global _stream

    _stream.stop_stream()
    print "stop_recording() > Recording stopped"


def close():

    global audi
    global wavefile
    global _stream

    _stream.close()
    audio.terminate()
    wavefile.close()
    print "close() > Stream closed, _pa terminated, wavefile closed"

def _prepare_file(fname, mode = 'wb' , CHANNELS = 1, RATE = 44100):
    global audio
    global wavefile

    wavefile = wave.open(fname, mode)
    wavefile.setnchannels(CHANNELS)
    wavefile.setsampwidth(audio.get_sample_size(pyaudio.paInt32))
    wavefile.setframerate(RATE)

    return wavefile

#MAIN

start_recording('startstop_20.wav', 1, 44100, 1024)
time.sleep(20)
stop_recording()
close()
