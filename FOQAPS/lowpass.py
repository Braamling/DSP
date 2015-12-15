
from scipy import signal
from foqaps import FOQAPS

if __name__ == '__main__':
    # Build the FOQAPS object. setting up variables and the output stream
    foqaps = FOQAPS()

    order = 4
    freq = .04

    # if type(freq) is int:
    #     freq = freq / (float(self.frame_rate) / 2)

    # Determine the Numerator and denomenator. 
    b, a = signal.butter(order, freq, btype = 'lowpass', analog=False)

    # Execture the filter in realtime
    foqaps.rt_lfilter(b, a, 1000)