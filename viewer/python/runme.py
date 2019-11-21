"""Read data from the selected folder

This script will load and display Clarius supported file types.

Note: code is tested on mac, for other operating systems you may need to
use backslash (\) instead of (/) for relative paths to work. 

Author: Reza Zahiri

"""

import numpy as np
from scipy.signal import hilbert
import matplotlib.pyplot as plt

# read rf data
def read_rf(filename):
    hdr_info = ('id', 'frames', 'lines', 'samples', 'samplesize')
    hdr, timestamps, data = {}, None, None
    with open(filename, 'rb') as raw_bytes:
        # read 4 bytes header 
        for info in hdr_info:
            hdr[info] = int.from_bytes(raw_bytes.read(4), byteorder='little')
        # read timestamps and data
        timestamps = np.zeros(hdr['frames'], dtype='int64')
        sz = hdr['lines'] * hdr['samples'] * hdr['samplesize']
        data = np.zeros((hdr['lines'], hdr['samples'], hdr['frames']), dtype='int16')
        for frame in range(hdr['frames']):
            # read 8 bytes of timestamp
            timestamps[frame] = int.from_bytes(raw_bytes.read(8), byteorder='little')
            # read each frame
            data[:, :, frame] = np.frombuffer(raw_bytes.read(sz), dtype='int16').reshape([hdr['lines'], hdr['samples']])
    print('Loaded {d[2]} raw frames of size, {d[0]} x {d[1]} (lines x samples)'.format(d=data.shape))
    return hdr, timestamps, data

# read iq data
def read_iq(filename):
    hdr_info = ('id', 'frames', 'lines', 'samples', 'samplesize')
    hdr, timestamps, data = {}, None, None
    with open(filename, 'rb') as raw_bytes:
        # read 4 bytes header 
        for info in hdr_info:
            hdr[info] = int.from_bytes(raw_bytes.read(4), byteorder='little')
        # read timestamps and data
        timestamps = np.zeros(hdr['frames'], dtype='int64')
        sz = hdr['lines'] * hdr['samples'] * hdr['samplesize']
        data = np.zeros((hdr['lines'], hdr['samples'] * 2, hdr['frames']), dtype='int16')
        for frame in range(hdr['frames']):
            # read 8 bytes of timestamp
            timestamps[frame] = int.from_bytes(raw_bytes.read(8), byteorder='little')
            # read each frame
            data[:, :, frame] = np.frombuffer(raw_bytes.read(sz), dtype='int16').reshape([hdr['lines'], hdr['samples']*2])
    print('Loaded {d[2]} raw frames of size, {d[0]} x {d[1]} (lines x samples)'.format(d=data.shape))
    return hdr, timestamps, data

# read env data
def read_env(filename):
    hdr_info = ('id', 'frames', 'lines', 'samples', 'samplesize')
    hdr, timestamps, data = {}, None, None
    with open(filename, 'rb') as raw_bytes:
        # read 4 bytes header 
        for info in hdr_info:
            hdr[info] = int.from_bytes(raw_bytes.read(4), byteorder='little')
        # read timestamps and data
        timestamps = np.zeros(hdr['frames'], dtype='int64')
        sz = hdr['lines'] * hdr['samples'] * hdr['samplesize']
        data = np.zeros((hdr['lines'], hdr['samples'], hdr['frames']), dtype='uint8')
        for frame in range(hdr['frames']):
            # read 8 bytes of timestamp
            timestamps[frame] = int.from_bytes(raw_bytes.read(8), byteorder='little')
            # read each frame
            data[:, :, frame] = np.frombuffer(raw_bytes.read(sz), dtype='uint8').reshape([hdr['lines'], hdr['samples']])
    print('Loaded {d[2]} raw frames of size, {d[0]} x {d[1]} (lines x samples)'.format(d=data.shape))
    return hdr, timestamps, data


if __name__ == '__main__':
    
    # read rf data
    path = "../data/wirephantom/"
    filename = "phantom_rf.raw"
    hdr, timestamps, data = read_rf(path + filename)
    
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
    hdr, timestamps, data = read_iq(path + filename)
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
    hdr, timestamps, data = read_env(path + filename)

    # display b data
    numframes = hdr['frames']
    for frame in range(numframes):
        plt.figure(figsize=(5,5))
        plt.imshow(np.transpose(data[:,:,frame]), cmap=plt.cm.gray, aspect='auto', vmin=0, vmax=255 )
        plt.title('envelope frame ' + str(frame))
        plt.show()   
    