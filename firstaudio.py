import argparse
import pyaudio
import wave
import time

audio = None
wavefile = None
_stream = None

class wav_recoder(object):
        def __init__(self, filename, CHANNELS=1, RATE=44100, CHUNK=10, device_num=None, sample_type=pyaudio.paInt32):
                self.filename = filename
                self.channels = CHANNELS
                self.rate = RATE
                self.num_frames = CHUNK
                self.devive_num =device_num
                self.sample_type = sample_type

                self.audio = pyaudio.PyAudio()
                self.wavefile = self._prepare_file()
                self._stream = None


        def start_recording(self):
                #Use a stream with a callback in non-blocking mode 
                self._stream = self.audio.open(format=pyaudio.paInt16,
                                                channels=self.channels,
                                                rate=self.rate,
                                                input=True,
                                                frames_per_buffer=self.num_frames,
                                                input_device_index=7,
                                                stream_callback=self._callback)
        
                self._stream.start_stream()

                print("start_recording() > Recording started")

        def _callback(self, in_data, frame_count, time_info, status):
                self.wavefile.writeframes(in_data)
                return in_data, pyaudio.paContinue

        def stop_recording(self):
                self._stream.stop_stream()
                print("stop_recording() > Recording stopped")


        def close(self):
                self._stream.close()
                self.audio.terminate()
                self.wavefile.close()
                print("close() > Stream closed, _pa terminated, wavefile closed")

        def _prepare_file(self):
                wavefile = wave.open(self.filename, 'wb')
                wavefile.setnchannels(self.channels)
                wavefile.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
                wavefile.setframerate(self.rate)

                return wavefile

#MAIN
_SAMPLE_TYPES = {'int16':pyaudio.paInt16, 'int32':pyaudio.paInt32}
if __name__ == "__main__":
        parser = argparse.ArgumentParser(description='Record a wav file.')
        parser.add_argument('-f', '--file', type=str, required=False, default='startstop_20.wav', help='File name')
        parser.add_argument('-c', '--chan', type=int, required=False, default=1, help='Number of audio channels')
        parser.add_argument('-r', '--rate', type=int, required=False, default=44100, help='Sample rate')
        parser.add_argument('-n', '--nframes', type=int, required=False, default=10, help='Number of frames per buffer')
        parser.add_argument('-d', '--device', type=int, required=False, default=-1, help='Device ID')
        parser.add_argument('-t', '--type', type=str, required=False, default='int32', help='Sample data type. Can be either int16 or int32')
        parser.add_argument('--time', type=int, required=False, default=20, help='Recording length')

        args = parser.parse_args()
        
        sample_type = pyaudio.paInt16
        try:
            sample_type = _SAMPLE_TYPES[args.type]
        except KeyError:
            print("Invalid sample type. Using signed 16-bit integers")

        device = args.device
        if device < 0:
            device = None

        recoder = wav_recoder(args.file, args.chan, args.rate, args.nframes, args.device, sample_type=sample_type)
        recoder.start_recording()
        time.sleep(args.time)
        recoder.stop_recording()
        recoder.close()
