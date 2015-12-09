import matplotlib.pyplot as plt
import scipy.io.wavfile
import numpy as np
import os
import operator


from scipy import signal
from scipy.ndimage.filters import maximum_filter
from scipy.ndimage.morphology import generate_binary_structure, binary_erosion

class Shazam():
    database = {}
    debug = True

    # http://stackoverflow.com/questions/3684484/peak-detection-in-a-2d-array
    def detect_peaks(self, image):
        """
        Takes an image and detect the peaks using the local maximum filter.
        Returns a boolean mask of the peaks (i.e. 1 when
        the pixel's value is the neighborhood maximum, 0 otherwise)
        """

        # define an 8-connected neighborhood
        neighborhood = generate_binary_structure(2,2)
        neighborhood = np.full((20,3), True)

        #apply the local maximum filter; all pixel of maximal value 
        #in their neighborhood are set to 1
        local_max = maximum_filter(image, footprint=neighborhood)==image
        #local_max is a mask that contains the peaks we are 
        #looking for, but also the background.
        #In order to isolate the peaks we must remove the background from the mask.

        #we create the mask of the background
        background = (image==0)
        #a little technicality: we must erode the background in order to 
        #successfully subtract it form local_max, otherwise a line will 
        #appear along the background border (artifact of the local maximum filter)
        eroded_background = binary_erosion(background, structure=neighborhood, border_value=1)

        #we obtain the final mask, containing only peaks, 
        #by removing the background from the local_max mask
        detected_peaks = local_max - eroded_background
        return detected_peaks.astype(int)

    def create_footprint(self, filename):
        self.print_debug("Creating footprint for: " + filename)

        sr,x = scipy.io.wavfile.read(filename)
        x = x.T[0]
        ## Parameters: 10ms step, 30ms window
        nstep = int(sr * 0.01)
        nwin  = int(sr * 0.03)
        nfft = nwin

        window = np.hamming(nwin)

        ## will take windows x[n1:n2].  generate
        ## and loop over n2 such that all frames
        ## fit within the waveform
        nn = range(nwin, len(x), nstep)

        X = np.zeros( (len(nn), nfft/2) )

        for i,n in enumerate(nn):
            xseg = x[n-nwin:n]
            z = np.fft.fft(window * xseg, nfft)
            X[i,:] = np.log(np.abs(z[:nfft/2]))

        
        # Retrieve peaks 
        peaks = self.detect_peaks(X.T)


        plt.imshow(X.T, interpolation='nearest',
                   origin='lower',
                   aspect='auto')

        # plt.show()


        plt.imshow(peaks, interpolation='nearest',
                   origin='lower',
                   aspect='auto')

        self.print_debug("Footprint created for: " + filename)

        return peaks

    # def corrilate(self, sample):
    #     b[data_length/2:data_length/2+data_length] = a # This works for data_length being even

    #     # Do an array flipped convolution, which is a correlation.
    #     c = signal.fftconvolve(b, a[::-1], mode='valid') 

    #     # Use numpy.correlate for comparison
    #     d = numpy.correlate(a, a, mode='same')

    #     # c will be exactly the same as d, except for the last sample (which 
    #     # completes the symmetry)
    #     numpy.allclose(c[:-1], d) # Should be True

    def find_match(self, filename):
        self.print_debug("Starting match for: " + filename)
        
        # Create a footprint of the track
        footprint = self.create_footprint(filename)

        results = {}
        # Compare all database entries with the footprint
        for name, entry in self.database.iteritems():
            # Get the highest values with the best match
            results[name] = np.amax(signal.fftconvolve(footprint, entry, 'same'))

        return max(results.iteritems(), key=operator.itemgetter(1))[0]

    def build_database(self, dir):
        """ Create a database from a files in a directory """
        self.print_debug("Initializing database")
        
        files = os.listdir(dir)

        for i, filename in enumerate(files):
            self.print_debug("Initialized " + str(i + 1) + "/" + str(len(files)) + " samples.")
            self.database[filename] = self.create_footprint(dir + filename)

        self.print_debug("Database Initialized")

    def print_debug(self, text):
        if self.debug:
            print("[DEBUG] - " + text)


if __name__ == '__main__':
    db_folder = "Birds/database/"
    sample_folder = "Birds/samples/"
    sample_file = "alcedo_atthis_ijsvogel.wav"

    shazam = Shazam()
    shazam.build_database(db_folder)
    match_file = shazam.find_match(sample_folder + sample_file)

    print("We have matched " + sample_file + " to " + match_file)
