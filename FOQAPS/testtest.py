import numpy as np
from numpy.random import randn
from numpy.fft import rfft
from scipy import signal
import matplotlib.pyplot as plt

b, a = signal.butter(4, 0.03, analog=False)

# Show that frequency response is the same
impulse = np.zeros(1000)
impulse[100] = 1
imp_ff = signal.filtfilt(b, a, impulse)
imp_lf = signal.lfilter(b, a, impulse)
plt.subplot(2, 2, 1)
plt.semilogx(20*np.log10(np.abs(rfft(imp_lf))))
plt.ylim(-100, 20)

plt.subplot(2, 2, 2)
plt.semilogx(20*np.log10(np.abs(rfft(imp_ff))))
plt.ylim(-100, 20)

sig = np.cumsum(randn(800))  # Brownian noise
sig_ff = signal.filtfilt(b, a, sig)
sig_lf = signal.lfilter(b, a, sig)
plt.subplot(2, 1, 2)
plt.plot(sig, color='silver', label='Original')
plt.plot(sig_ff, color='#3465a4', label='filtfilt')
plt.plot(sig_lf, color='#cc0000', label='lfilter')
plt.legend()

plt.show()
