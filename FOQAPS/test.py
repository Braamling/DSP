import alsaaudio, sys
import time
 
channels = 1
sample_size = 1
frame_size = channels * sample_size
frame_rate = 44100
byte_rate = frame_rate * frame_size
 
#******************************************************************
#******************************************************************
#               OUTPUT                                       *
#period size controls internal number of frames per period
period_size = 160
 
out = alsaaudio.PCM(alsaaudio.PCM_PLAYBACK, alsaaudio.PCM_NORMAL)
 
out.setchannels(channels)
out.setformat(alsaaudio.PCM_FORMAT_S16_LE)
out.setrate(frame_rate)
out.setperiodsize(period_size)
 
#******************************************************************
#******************************************************************
#                       INPUT                                   *
 
inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL)
 
inp.setchannels(channels)
inp.setrate(frame_rate)
inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)#16 bit little endian
inp.setperiodsize(period_size)
 
#******************************************************************
 
def main():
       
        while True:
                l, data = inp.read()#l seems to always be 940
                if l:
                        #time.sleep(.1)
                        out.write(data)
       
                time.sleep(.001)
        return
       
if __name__ == '__main__':
        main()
