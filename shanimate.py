# -*- coding: utf-8 -*-
"""
Created on Sun Jun 17 12:09:30 2018

This script generates spherical harmonic animations as gifs.

Spherical degree (l) and azimuthal order (m) required as inputs.

@author: keatonb
"""

#import stuff
from __future__ import division, print_function
import sys
import argparse
import scipy.special as sp
import numpy as np
import cartopy.crs as ccrs
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import animation


def main(args):
    #ensure valid input
    assert np.abs(args.m) <= args.ell
    assert np.abs(args.inc) <= 180
    outfile = args.outfile 
    if outfile is None:
        outfile = 'l{0}m{1}.gif'.format(args.ell,args.m)
    
    plotcrs = ccrs.Orthographic(0, 90-args.inc)

    #compute spherical harmonic
    lon = np.linspace(0,2*np.pi,args.nlon)-np.pi
    lat = np.linspace(-np.pi/2,np.pi/2,args.nlat)
    colat = lat+np.pi/2
    d = np.zeros((len(lon),len(colat)),dtype = np.complex64)
    for j, yy in enumerate(colat):
        for i, xx in enumerate(lon):
            d[i,j] = sp.sph_harm(args.m,args.ell,xx,yy)
    
    # set up figure
    fig = plt.figure(figsize=(args.size,args.size),tight_layout = {'pad': 0})
    ax = plt.subplot(projection=plotcrs)
    drm = np.transpose(np.real(d))
    vlim = np.max(np.abs(drm))
    ax.pcolormesh(lon*180/np.pi,lat*180/np.pi,drm,
                transform=ccrs.PlateCarree(),cmap='seismic',vmin=-vlim,
                vmax=vlim)
    ax.relim()
    ax.autoscale_view()
    
    #Prepare to animate
    
    #No initialization needed
    def init():
        return 
    
    #animation function to call
    def animate(i):
        drm = np.transpose(np.real(d*np.exp(-1.j*(2.*np.pi*float(i) / 
                                                  np.float(args.nframes)))))
        sys.stdout.write("\rFrame {0} of {1}".format(i+1,args.nframes))
        sys.stdout.flush()
        drm[np.abs(drm) < 1.e-6] = 0.
        ax.clear()
        ax.pcolormesh(lon*180/np.pi,lat*180/np.pi,drm,
             transform=ccrs.PlateCarree(),cmap='seismic',vmin=-vlim,vmax=vlim)
        ax.relim()
        ax.autoscale_view()
        return
    
    interval = args.duration / np.float(args.nframes)
  
    anim = animation.FuncAnimation(fig, animate, init_func=init, 
                                   frames=args.nframes, interval=interval, 
                                   blit=False)
    anim.save(outfile, dpi=args.dpi, fps = 1./interval, writer='imagemagick')
    print('\nWrote '+outfile)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            description = 'Generate animated gif of spherical harmonic.')
    parser.add_argument('ell', type=int, help='spherical degree')
    parser.add_argument('m', type=int, help='azimuthal order')
    parser.add_argument('-o','--outfile', type=str, 
                        help='output gif filename')
    parser.add_argument('-i','--inc', type=float, default=60, 
                        help='inclination (degrees from pole)')
    parser.add_argument('-s','--size', type=float, default=1, 
                        help='image size (inches)')
    parser.add_argument('-n','--nframes', type=int, default=32, 
                        help='number of frames in animation')
    parser.add_argument('-d','--duration', type=float, default=2, 
                        help='animation duration (seconds)')
    parser.add_argument('--nlon', type=int, default=200, 
                        help='number of longitude samples')
    parser.add_argument('--nlat', type=int, default=500, 
                        help='number of latitude samples')
    parser.add_argument('--dpi', type=float, default=300, 
                        help='dots per inch')
    args = parser.parse_args()
    
    main(args)
