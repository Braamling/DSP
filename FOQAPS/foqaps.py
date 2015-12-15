"""
authors: Wouter Vrielink & Bram van den Akker
date: 15-12-2015

"Filters Over Quality Audio Processing Software"
Module that implements realtime audio filters. 

Initialize the class before use.

Method `rt_lfilter` is based on the scipy.signal.lfilter method,
but uses a timeframe instead of input stream. The input stream
will be generated with the realtime data.  
"""

import alsaaudio
import struct
import time

from scipy import signal
import numpy as np

class FOQAPS():
    def __init__(self):
        """ Initialize input and output streams """
        self.channels = 1
        sample_size = 1
        self.frame_size = self.channels * sample_size
        self.frame_rate = 44100
        byte_rate = self.frame_rate * self.frame_size
        self.period_size = 320

        self.create_output_stream()
        self.create_input_stream()

    def create_input_stream(self):
        """ Create an input stream and store it in the object.
        """

        # Create input object
        self.inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL)
        
        # Configure the input stream
        self.inp.setchannels(self.channels)
        self.inp.setrate(self.frame_rate)
        self.inp.setformat(alsaaudio.PCM_FORMAT_FLOAT_LE)#16 bit little endian
        self.inp.setperiodsize(self.period_size)

    def create_output_stream(self):
        """ Create an output stream and store it in the object """
        self.out = alsaaudio.PCM(alsaaudio.PCM_PLAYBACK, alsaaudio.PCM_NORMAL)
         
        # Configure the output stream
        self.out.setchannels(self.channels)
        self.out.setformat(alsaaudio.PCM_FORMAT_FLOAT_LE)
        self.out.setrate(self.frame_rate)
        self.out.setperiodsize(self.period_size)

         
    def execute_filter(self, b, a, buffer, pre_buffer):
        """ Order; the order of the filter (int). 
        Freq; scalar or length-2 sequence giving the critical frequencies.
        Data; N-dimensional input array.
        Filter_type: {'lowpass', 'highpass', 'bandpass', 'bandstop'}, optional.
        """
        timing = time.time()
        pre_buffer = np.concatenate([pre_buffer, buffer])

        # Execute the filter onto the buffer. 
        output = signal.lfilter(b, a, pre_buffer)

        # Only return the output based on the current buffer (drop pre_buffer)
        return output[len(output)/2:]


    def rt_lfilter(self, b, a, run_time):
        """ Realtime lfilter
        Execute a filter over the audio captured with the microfone.

        b: 
        a: 
        run_time: Time to run filter in seconds
        """

        start_time = time.time()

        # Used to determen the computational delay.
        comp_time = 0

        # Used to initate the first buffer filter without issues.
        prev_buffer = [0.0] * self.period_size

        # Preform computations while the run time has not been reached.
        while time.time() - start_time < run_time:

            # Empty everything in the buffer that was recorded during the 
            # Computations.
            buffer = ""
            length = 0
            while comp_time > self.period_size / float(self.frame_rate):
                l,date = self.inp.read()
                comp_time -= self.period_size / float(self.frame_rate)
                buffer = buffer + data
                length = length + l

            # Fetch the final buffer
            l, data = self.inp.read()

            # Get the start time of the computational process. 
            start_time = time.time()
            
            # Unpack the buffer
            floats = struct.unpack('f' * (length + l), buffer + data)

            # Subsample buffer to self.period_size
            floats = floats[0::len(floats)/self.period_size]

            # Execute the filter over buffer. 
            result = self.execute_filter(b, a, floats, prev_buffer)

            # Convert floats back to a struct for output.
            output = struct.pack('f' * l, *result)

            # Calculate the computation time filter. 
            comp_time = time.time() - start_time

            # Output audio
            self.out.write(output)

            # Keep the buffer to use as samples for the next buffer.
            prev_buffer = floats

