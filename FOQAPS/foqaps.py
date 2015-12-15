"""
Authors: Wouter Vrielink & Bram van den Akker
Date: 15-12-2015

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
import gc

from scipy import signal
import numpy as np

class FOQAPS():
    def __init__(self, channels=1, sample_size=1, frame_rate=44100, period_size=320):
        """ Initialize stream variables and output stream. 
        channels [default=1] Amount of channels to use in audio
        sample_size [default=1] Size of each sample
        frame_rate [default=44100] The frame_rate to use for input and output
        period_size [default=320] periode size of each buffer. """
        self.channels = channels
        self.frame_size = self.channels * sample_size
        self.frame_rate = frame_rate
        self.period_size = period_size

        self.create_output_stream()

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

    def destroy_input_stream(self):
        """ Detroy input stream to prevent memory issues. """

        # Destroy the stream
        del self.inp

        # Garbage collect
        gc.collect()

    def create_output_stream(self):
        """ Create an output stream and store it in the object """
        self.out = alsaaudio.PCM(alsaaudio.PCM_PLAYBACK, alsaaudio.PCM_NORMAL)
         
        # Configure the output stream
        self.out.setchannels(self.channels)
        self.out.setformat(alsaaudio.PCM_FORMAT_FLOAT_LE)
        self.out.setrate(self.frame_rate)
        self.out.setperiodsize(self.period_size)

    def execute_filter(self, b, a, buffer, pre_buffer):
        """ Execute the actual filter over the buffer.
        b: The numerator coefficient vector in a 1-D sequence.
        a: The denominator coefficient vector in a 1-D sequence. 
            If a[0] is not 1, then both a and b are normalized by a[0].
        buffer: The current buffer from the input stream (1d array)
        pre_buffer: The previous buffer from the input stream (1d array)

        return 1d output with the length of a single buffer.
        """
        timing = time.time()
        pre_buffer = np.concatenate([pre_buffer, buffer])

        # Execute the filter onto the buffer. 
        output = signal.lfilter(b, a, pre_buffer)

        # Only return the output based on the current buffer (drop pre_buffer)
        return output[len(output)/2:]

    def rt_lfilter(self, b, a, run_time):
        """ Realtime linear filter
        Execute a filter over the audio captured with the microfone.

        b: The numerator coefficient vector in a 1-D sequence.
        a: The denominator coefficient vector in a 1-D sequence. 
            If a[0] is not 1, then both a and b are normalized by a[0].
        run_time: Time to run filter in seconds
        """
        # Store the start time of the filter to determine duration.
        start_time = time.time()

        # Set up an input stream, stored in object, to be removed after
        # the filter is completed.
        self.create_input_stream()

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

        self.destroy_input_stream()