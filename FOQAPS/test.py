import alsaaudio, sys, audioop
import time
 
class FOQAPS():

    """ Initialize input and output streams """
    def __init__(self):
        channels = 1
        sample_size = 1
        frame_size = channels * sample_size
        frame_rate = 44100
        byte_rate = frame_rate * frame_size
        period_size = 160

        # Create output object
        self.out = alsaaudio.PCM(alsaaudio.PCM_PLAYBACK, alsaaudio.PCM_NORMAL)
         
        # Configure the output stream
        self.out.setchannels(channels)
        self.out.setformat(alsaaudio.PCM_FORMAT_FLOAT_LE)
        self.out.setrate(frame_rate)
        self.out.setperiodsize(period_size)

        # Create input object
        self.inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL)
        
        # Configure the input stream
        self.inp.setchannels(channels)
        self.inp.setrate(frame_rate)
        self.inp.setformat(alsaaudio.PCM_FORMAT_FLOAT_LE)#16 bit little endian
        self.inp.setperiodsize(period_size)
         
         
    def foqaps_butter(self, order, freq , data, filter_type = 'lowpass'):
    """ Order; the order of the filter (int). 
        Freq; scalar or length-2 sequence giving the critical frequencies.
        Data; N-dimensional input array.
        Filter_type: {‘lowpass’, ‘highpass’, ‘bandpass’, ‘bandstop’}, optional.
    """
        a, b = scipy.signal.butter(order, freq, btype = filter_type)
        return scipy.signal.filtfilt(b, a, data)

    def playback_audio_realtime(self, end_time):
        run_time = 0
        while run_time < end_time:
            l, data = self.inp.read()#l seems to always be 940
            self.out.write(data)
            time.sleep(.001)

            run_time += 1


if __name__ == '__main__':
    foqaps = FOQAPS()
    foqaps.playback_audio_realtime(1000000)
