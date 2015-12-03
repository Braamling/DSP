import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy.io import wavfile # get the api

fs, data = wavfile.read('track01_ijsvogel.wav')

length = data.shape[0] / fs

times = 10
fft_fs = fs / 10

print fft_fs
print fs

a = data.T[0]
for i in range(length * times):
    print fft_fs*(i+1)
    # two channel track, get the first channel


    # 8-bit track, b is now normalized on [-1,1)
    #b=[(x/2**8.)*2-1 for x in a] 
    
    c = fft(a[i*fft_fs:fft_fs*(i+1)]) # calculate fourier transform (complex numbers list)
    d = len(c)/2  # you only need half of the fft list (real signal symmetry)
    X[i,:] = np.log(np.abs(z[:nfft/2]))
    plt.plot(abs(c[:(d-1)]),'r') 
    plt.show()
    
from pylab import *
specgram(b)
