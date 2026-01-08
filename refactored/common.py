from gala.coordinates import reflex_correct, GD1Koposov10
from astropy.coordinates import SkyCoord
import matplotlib.pyplot as plt
from os.path import basename, exists
import re
import numpy as np


def table_to_string(table):
    s = np.array2string(table.as_array(), max_line_width=1000, separator=', ')
    s = re.sub('[\\[\\]()]', '', s)
    return s

def skycoords_to_string(skycoords):
    t = skycoords.to_string()
    s = ' '.join(t)
    return s.replace(' ', ', ')

def icrs_to_gd1 (coord) :
    transformed = coord.transform_to(GD1Koposov10)
    return reflex_correct(transformed)

def polygon (a, b):
    return np.append(a, b[::-1])

def make_rectangle(x_range, y_range):
    """Return the corners of a rectangle."""
    (x1,x2) = x_range
    (y1,y2) = y_range
    xs = [x1, x1, x2, x2, x1]
    ys = [y1, y2, y2, y1, y1]
    return xs, ys

def is_between(series, range):
    """Check whether values are between `low` and `high`."""
    (low,high) = range
    return (series > low) & (series < high)

def plot_proper_motion(table, decorator='ko', markersize=0.1, alpha=0.5) :
    """Plot propermotion in GD1 coordinates from given dataframe"""
    x = table['pm_phi1']
    y = table['pm_phi2']
    plt.plot(x, y, decorator, markersize=markersize, alpha=alpha)

        
    plt.xlabel('Proper motion phi1 (mas/yr GD1 frame)')
    plt.ylabel('Proper motion phi2 (mas/yr GD1 frame)');

    plt.xlim(-12, 8)
    plt.ylim(-10, 10);

    #plt.axis('equal');

    return plt

def plot_ra_dec(table, decorator='ko', markersize=0.1, alpha=0.5) :
    """Plot location in ra/dec coordinates from given dataframe"""
    x = table['ra']
    y = table['dec']
    plt.plot(x, y, decorator, markersize=markersize, alpha=alpha)


    plt.xlabel('RA (deg)')
    plt.ylabel('Dec (deg)');

    plt.axis('equal');

    return plt

def plot_gd1(table, decorator='ko', markersize=0.1, alpha=0.5, limits=None) :
    """Plot location in ra/dec coordinates from given dataframe"""
    x = table['phi1']
    y = table['phi2']
    plt.plot(x, y, decorator, markersize=markersize, alpha=alpha)



    plt.xlabel('phi1 GD-1 frame (deg)')
    plt.ylabel('phi2 GD-1 frame (deg)');

    plt.axis('equal');

    if limits:
        plt.xlim(limits[0])
        plt.ylim(limits[1])
    

    return plt

def plot_cmd(table, decorator='ko', markersize=0.1, alpha=0.5):
    y=table['g_mean_psf_mag']
    x=table['g_mean_psf_mag'] - table['i_mean_psf_mag']

    plt.plot(x,y, decorator, markersize=markersize, alpha=alpha)

    plt.xlim(0,3)
    plt.ylim(14,22)
    plt.gca().invert_yaxis()
    
    plt.ylabel('Magnitude $(g)$')
    plt.xlabel('Color $(g-i)$')

    return plt

def download(url):
    filename = basename(url)
    if not exists(filename):
        from urllib.request import urlretrieve
        local, _ = urlretrieve(url, filename)
        print('Downloaded ' + local)
