#!/usr/bin/python
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# cutoutslink.py
#
# Generates on-the-fly cutouts for ATLASmultiID.py
# Requires radio surface brightness, radio RMS map, and optical images
# 
# Cutouts are radio contours, preprojected (via interpolation) onto heatmap 
# optical images. 
#
# Author:
#   Jesse Swan 
#   University of Tasmania
#   Aug 2016
#
# 19th Aug - Fixed crashing when optical mosaic slice wasn't square, or size 
#            (0,0) due to being in a region where optical mosaic doesn't 
#            cover. Optical array is now positionally inserted into an array 
#            of zeros of the required shape. 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


from __future__ import division
from __future__ import print_function

import time

import astropy.wcs as wcs
from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
import reproject

# matplotlib.rcParams.update({'figure.autolayout': True})

verbose = False

# ------------------------------------------ #

if verbose:
    def verboseprint(*args):
        """
            usage: verboseprint('words', value, 'words', ...)
        """
        for arg in args:
            print(arg, end=' ')
        print()
else:  # a function that returns None
    def verboseprint(*args):
        return None


# http://preshing.com/20110924/timing-your-code-using-pythons-with-statement/
class Timer(object):    
    '''
        Times imbedded code execution
        Example usage for averaging over 10 runs:

        ts = []
        for i in range(10):
            with Timer() as t:
                <RUN CODE>
                ts.append(t.interval)
        print 'mean was', np.mean(ts)
    '''
    def __enter__(self):
        self.start = time.clock()
        return self

    def __exit__(self, *args):
        self.end = time.clock()
        self.interval = self.end - self.start


def rms(arr):
    '''
        find the RMS of input array
    '''
    from math import sqrt
    if len(arr.shape) > 1:
        arr = arr.flatten()
    return sqrt(old_div(np.nansum([x*x for x in arr]),len(arr)))


def arr_slice(arr, slicer, size):
    """
        Slices a 2d array to a square region specified by
        the slicer, and pads if necessary.

        Slicer should be defined as
               slicer = np.s_[xmin:xmax, ymin:ymax]

        Note:
        if array isn't square (xmax - xmin = ymax - ymin). If this occurs the returned array will be padded with zeroes
    """
    sliced = arr[slicer]
    if sliced.shape[0]!=sliced.shape[1]:
        # directly insert sliced data into an array of the intended size filled with 0.
        temp = np.zeros((size,size))
        temp[:sliced.shape[0], :sliced.shape[1]] = sliced
        sliced = temp
    return sliced


def cutouts(optical_image, radio_image, radio_rms, targetRA, targetDEC, osize = 200, rsize= 180, vmax=1.5, verbose=False):
    ''' does things '''

    from matplotlib.colors import PowerNorm#,LogNorm, SymLogNorm,

    if fits.getdata(radio_image)[0][0].shape != fits.getdata(radio_rms)[0][0].shape:
        raise Exception('Check that the radio image and radio rms files match')

    target = [targetRA, targetDEC]

    # Work out the integer pixel position of the target coordinates in optical
    omap_full = wcs.WCS(optical_image)
    opix = omap_full.wcs_world2pix([target], 1) # wcs conversions take list of lists
    opix = [int(x) for x in opix[0]] # ensure returned pixels are integer

    verboseprint('o_full shape', fits.getdata(optical_image).shape)
    verboseprint('optical pix center', opix)

    # Work out the integer pixel position of the target coordinates in radio
    rmap_full = wcs.WCS(radio_image).celestial
    rpix = rmap_full.wcs_world2pix([target],1)
    rpix = [int(x) for x in rpix[0]]

    verboseprint('r_full shape', fits.getdata(radio_image).shape)
    verboseprint('radio pix center', rpix)

    # Create slicer and slice the optical image, and optical WCS map
    half_osize = int(osize / 2.)
    oslicer = np.s_[opix[1] - half_osize:opix[1] + half_osize,
              opix[0] - half_osize:opix[0] + half_osize]  # (DEC:RA)

    ocut = arr_slice(fits.getdata(optical_image), oslicer, osize)
    omap = omap_full[oslicer]  # Note: wcs map can't be sliced by arr_slice, do it manually
    verboseprint('ocut shape', ocut.shape)

    # Create slicer and slice the radio image, radio rms, and radio WCS map
    half_rsize = int(rsize / 2.)
    rslicer = np.s_[rpix[1] - half_rsize:rpix[1] + half_rsize,
              rpix[0] - half_rsize:rpix[0] + half_rsize]  # (DEC:RA)

    rcut = arr_slice(fits.getdata(radio_image)[0][0], rslicer,
                     rsize)  # [0][0] because data is stored weird in fits file (shape (1,1,n,m))
    rmap = rmap_full[rslicer]
    verboseprint('rcut shape', rcut.shape)

    # Contours are to be in steps of (2^n)*(2.5*median(local_rms))
    contours = [2 ** x for x in range(17)]
    local_rms = 2.5 * np.nanmedian(
            fits.getdata(radio_rms)[0][0][rslicer])  # should have same shape and projecion as radio_image
    contours = [local_rms * x for x in contours]

    # project radio coordinates (rcut,rmap) onto optical projection omap
    # Fails unless you specifying the shape_out (to be the same as what you are projecting onto)
    # Since omap doesn't have a .shape, ocut.shape is used instead

    project_r, footprint = reproject.reproject_interp((rcut, rmap), omap, shape_out=ocut.shape)

    figure = plt.figure(figsize=(6.55, 5.2))
    axis = figure.add_subplot(111, projection=omap)
    # fig.subplots_adjust(left=0.25, right=.60)

    axtrans = axis.get_transform(
        'fk5')  # necessary for scattering data on later -- e.g ax.plot(data, transform=axtrans)

    #### CHANGE VMAX HERE TO SUIT YOUR DATA - (I just experimented) #####
    # plotting
    normalise = PowerNorm(gamma=.7)
    axis.imshow(ocut, origin='lower', cmap='gist_heat_r', norm=normalise, vmax=vmax)  # origin='lower' for .fits files
    axis.contour(np.arange(project_r.shape[0]), np.arange(project_r.shape[1]), project_r, levels=contours,
                 linewidths=1, smooth=16)

    axis.set_autoscale_on(False)
    axis.coords['RA'].set_axislabel('Right Ascension')
    axis.coords['DEC'].set_axislabel('Declination')

    return figure, axis, axtrans, omap


if __name__ == '__main__':
    ''' Test '''
 
    ## ELAIS test files for testing ##
    radio = 'data/ELAIS/ELAISmosaic_allch_8March2015.fits'
    noise = 'data/ELAIS/ELAISmosaic_allch_noise_8March2015.fits'
    swire = 'data/ELAIS/elais_mosaic.fits'
    optic = 'data/ELAIS/optical-r-mosaic.fits'
    target = [8.588891, -43.333966]
    # target = [8.740639, -43.919979]
    fig, ax, axtrans,omap = cutouts(swire, radio, noise, target[0], target[1], osize=200, rsize=110, verbose=True)
    sources, = ax.plot(target[0], target[1], 'k*', transform=axtrans)
    fig, ax, axtrans,omap = cutouts(optic, radio, noise, target[0], target[1], osize=400, rsize=210, vmax=40.5, verbose=True)
    sources, = ax.plot(target[0], target[1], 'k*', transform=axtrans)
    # sources.remove()

    plt.show()
