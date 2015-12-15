"""
Authors: Wouter Vrielink & Bram van den Akker
Date: 15-12-2015

FOQAPS example using a lowpass filter.

The code at (1) makes it possible to configure the frequency both
with the normal frequency or with a fraction of the nyquist frequency.
"""

from scipy import signal
from foqaps import FOQAPS

if __name__ == '__main__':
    # Build the FOQAPS object, setting up variables and the output stream
    foqaps = FOQAPS()

    # Configure filter
    order = 4
    freq_1 = 500
    freq_2 = 2000
    run_time = 1000
    frame_rate = 44100

    # (1) In case of a regular frequency, convert to the nyquist frequency.
    if type(freq_1) is int:
        freq_1 = freq_1 / (float(frame_rate) / 2)
    if type(freq_2) is int:
        freq_2 = freq_2 / (float(frame_rate) / 2)

    # Determine the Numerator and denomenator. 
    b, a = signal.butter(order, [freq_1, freq_2], btype = 'bandpass', analog=False)

    # Execture the filter in realtime
    foqaps.rt_lfilter(b, a, run_time)