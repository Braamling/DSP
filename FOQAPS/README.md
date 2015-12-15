# FOQAPS
### Filters Over Quality Audio Processing Software
Python module that implements realtime audio filters. 

*Initialize the class as an object before use.*

#### Methods
##### *__init__*
Initialize stream variables and output stream. 

```
self: default
channels [default=1]: Amount of channels to use in audio
sample_size [default=1]: Size of each sample
frame_rate [default=44100]: The frame_rate to use for input and output
period_size [default=320]: periode size of each buffer. 
```
##### *create_input_stream*
Create an input stream and store it in the object.

##### *destroy_input_stream*
Detroy input stream to prevent memory issues.

##### *create_output_stream*
Create an output stream and store it in the object 

##### *execute_filter*
Execute the actual filter over the buffer.

```
self: default.
b: The numerator coefficient vector in a 1-D sequence.
a: The denominator coefficient vector in a 1-D sequence. 
    If a[0] is not 1, then both a and b are normalized by a[0].
buffer: The current buffer from the input stream (1d array)
pre_buffer: The previous buffer from the input stream (1d array)

return: 1d output with the length of a single buffer.
```

##### *rt_lfilter*
Realtime linear filter
Execute a filter over the audio captured with the microfone.
based on the scipy.signal.lfilter method,
but uses a timeframe instead of input stream. The input stream
will be generated with the realtime data. 

```
self: default
b: The numerator coefficient vector in a 1-D sequence.
a: The denominator coefficient vector in a 1-D sequence. 
    If a[0] is not 1, then both a and b are normalized by a[0].
run_time: Time to run filter in seconds
```

#### Using FOQAPS
Import the module class in python.

```python
from foqaps import FOQAPS
```

Initiate the python object.
```python
foqaps = FOQAPS()
```

Use any tool to create the numerator coefficient vector and 
the denominator coefficient vector. Example using scipy.signal.butter.
```python
# Determine the numerator and denominator. 
b, a = signal.butter(order, freq, btype = 'lowpass', analog=False)
```  

Start the realtime linear filter with the run time (in seconds), calculated numerator
and denominator
```python
foqaps.rt_lfilter(b, a, 60)
``` 

#### Examples
To demonstrate the use of the FOQAPS library, we provide you with a few 
extra examples. 

*lowpass.py*
Example use of the FOQAPS library using a lowpass filter.

*bandpass.py*
Example of the FOQAPS library using a bandpass filter.

#### Authors
Authors: Wouter Vrielink & Bram van den Akker
Date: 15-12-2015