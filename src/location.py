from __future__ import annotations
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# earth semi- and major axis. se main.ipynb
a = 6378137.0
b = 6356752.314245


def geocentric_radius(phi: float) -> float:
    """
    Returns geocentric radius given geodetic latitude.

    Parameters:
    -----
    phi: float. geodetic latitude

    Returns:
    -----
    radius: float. Geocentric radius
    """
    numer = (a**2 * np.cos(phi))**2 + (b**2 * np.sin(phi))**2
    denom = (a*np.cos(phi))**2 + (b * np.sin(phi))**2
    radius = np.sqrt(numer/denom)
    return radius

def distance(angle1: float, angle2: float, radius: float, absolute: bool = True) -> float:
    """
    Returns distance along earths surface along latitude or longitude  
    
    Parameters:
    -----
    angle1, angle2: float. angles
    radius: float. Earths geocentric radius (see geocentric_radius)
    
    Returns:
    -----
    dist: float. distance along earths surface
    """
    if absolute:
        dist = abs(radius*(angle2-angle1))
    else:
        dist = radius*(angle2-angle1)
    return dist

def angle_north(d_phi, d_theta) -> float:
    alpha = np.arctan(d_theta/d_phi)
    return alpha


def convert_to_rad(coord: list) -> None:
    for i in range(len(coord)):
        coord[i] = np.radians(coord[i])