import alsaaudio
import struct
import time
from scipy import signal

class FOQAPS():

    """ Initialize input and output streams """
    def __init__(self):
        channels = 1
        sample_size = 1
        self.frame_size = channels * sample_size
        frame_rate = 44100
        byte_rate = frame_rate * self.frame_size
        self.period_size = 1024

        # Create output object
        self.out = alsaaudio.PCM(alsaaudio.PCM_PLAYBACK, alsaaudio.PCM_NORMAL)
         
        # Configure the output stream
        self.out.setchannels(channels)
        self.out.setformat(alsaaudio.PCM_FORMAT_FLOAT_LE)
        self.out.setrate(frame_rate)
        self.out.setperiodsize(self.period_size)

        # Create input object
        self.inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL)
        
        # Configure the input stream
        self.inp.setchannels(channels)
        self.inp.setrate(frame_rate)
        self.inp.setformat(alsaaudio.PCM_FORMAT_FLOAT_LE)#16 bit little endian
        self.inp.setperiodsize(self.period_size)
         
         
    def foqaps_butter(self, order, freq , data, filter_type = 'lowpass'):
        """ Order; the order of the filter (int). 
        Freq; scalar or length-2 sequence giving the critical frequencies.
        Data; N-dimensional input array.
        Filter_type: {'lowpass', 'highpass', 'bandpass', 'bandstop'}, optional.
        """
        a, b = signal.butter(order, freq, btype = filter_type, analog=False)
        return signal.lfilter(b, a, data)

    def playback_audio_realtime(self, end_time):
        run_time = 0
        while run_time < end_time:
            # Read the imput buffer
            l, data = self.inp.read()

            # Convert to an array of floats
            floats = struct.unpack('f' * self.period_size, data)


            result = self.foqaps_butter(5, .03, floats)
            #
            # HERE IS SPACE TO MANIPULATE AUDIO
            #

            # Convert floats back to a struct for output.
            test = struct.pack('f' * self.period_size, *result)

            # Output audio
            self.out.write(test)

            run_time += 1



if __name__ == '__main__':
    foqaps = FOQAPS()

    foqaps.playback_audio_realtime(1000000)
