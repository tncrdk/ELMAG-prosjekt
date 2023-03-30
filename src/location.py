from __future__ import annotations
import numpy as np
from geopy import distance

# earth semi- and major axis. se main.ipynb
a = distance.ELLIPSOIDS["WGS-84"][0]
b = distance.ELLIPSOIDS["WGS-84"][1]


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
    numer = (a**2 * np.cos(phi)) ** 2 + (b**2 * np.sin(phi)) ** 2
    denom = (a * np.cos(phi)) ** 2 + (b * np.sin(phi)) ** 2
    radius = np.sqrt(numer / denom)
    return radius


def angle_north(d_phi, d_theta) -> float:
    alpha = np.arctan(d_theta / d_phi)
    return alpha


def convert_to_rad(coord: list) -> None:
    for i in range(len(coord)):
        coord[i] = np.radians(coord[i])


def distance_geopy(p1, p2):
    return distance.geodesic(p1, p2, ellipsoid="WGS-84").m
