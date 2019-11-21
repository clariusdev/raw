"""Read data from the selected folder

This script will load and display Clarius supported file types.

Note: code is tested on mac, for other operating systems you may need to
use backslash (\) instead of (/) for relative paths to work. 

Author: Reza Zahiri

"""

import numpy as np
from scipy.signal import hilbert
import matplotlib.pyplot as plt
import sys
sys.path.append("../../common/python")
import rdataread as rd

if __name__ == '__main__':
    
    # read rf data
    path = "../data/wirephantom/"
    filename = "phantom_rf.raw"
    hdr, timestamps, data = rd.read_rf(path + filename)
    
    # covnert to B 
    numframes = hdr['frames']
    bdata = np.zeros((hdr['lines'], hdr['samples'], hdr['frames']), dtype='float')
    for frame in range(numframes):
        bdata[:,:,frame] = 20 * np.log10( np.abs(1 + hilbert(data[:,:,frame])) )
    
    # display images
    for frame in range(numframes):
        plt.figure(figsize=(10,5))
        plt.subplot(1,2,1)
        plt.imshow(np.transpose(data[:,:,frame]), cmap=plt.cm.gray, aspect='auto', vmin=-1000, vmax=1000 )
        plt.title('RF frame ' + str(frame))
        plt.subplot(1,2,2)
        plt.imshow(np.transpose(bdata[:,:,frame]), cmap=plt.cm.gray, aspect='auto', vmin=15, vmax=70 )
        plt.title('sample B frame ' + str(frame))
        plt.show()    
    
    # read iq data
    path = "../data/wirephantom/"
    filename = "phantom_iq.raw"
    hdr, timestamps, data = rd.read_iq(path + filename)
    # separating i and q data
    idata = data[:,0::2,:]
    qdata = data[:,1::2,:]    
 
    # covnert IQ to B 
    numframes = hdr['frames']
    bdata = np.zeros((hdr['lines'], hdr['samples'], hdr['frames']), dtype='float')
    for frame in range(numframes):
        bdata[:,:,frame] = 10 * np.log10(1 + np.power(idata[:,:,frame], 2) + np.power( qdata[:,:,frame], 2)  )
    
    # display images
    for frame in range(numframes):
        plt.figure(figsize=(15,5))
        plt.subplot(1,3,1)
        plt.imshow(np.transpose(idata[:,:,frame]), cmap=plt.cm.gray, aspect='auto', vmin=-100, vmax=100 )
        plt.title('I frame ' + str(frame))
        plt.subplot(1,3,2)
        plt.imshow(np.transpose(qdata[:,:,frame]), cmap=plt.cm.gray, aspect='auto', vmin=-100, vmax=100 )
        plt.title('Q frame ' + str(frame))
        plt.subplot(1,3,3)
        plt.imshow(np.transpose(bdata[:,:,frame]), cmap=plt.cm.gray, aspect='auto', vmin=15, vmax=70 )
        plt.title('sample B frame ' + str(frame))
        plt.show()
    
    # read b/envelope data
    path = "../data/wirephantom/"
    filename = "phantom_env.raw"
    hdr, timestamps, data = rd.read_env(path + filename)

    # display b data
    numframes = hdr['frames']
    for frame in range(numframes):
        plt.figure(figsize=(5,5))
        plt.imshow(np.transpose(data[:,:,frame]), cmap=plt.cm.gray, aspect='auto', vmin=0, vmax=255 )
        plt.title('envelope frame ' + str(frame))
        plt.show()   
    