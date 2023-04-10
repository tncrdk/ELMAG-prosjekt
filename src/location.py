from __future__ import annotations
import numpy as np
from geopy import distance
import load_data
from dataclasses import dataclass
from scipy.stats import tstd
from pathlib import Path

# earth semi- and major axis. se main.ipynb
a = distance.ELLIPSOIDS["WGS-84"][0]
b = distance.ELLIPSOIDS["WGS-84"][1]


@dataclass
class Location:
    altitude: dict[str, float]
    longitude: dict[str, float]
    latitude: dict[str, float]


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


def get_location(person: str) -> dict[str, dict[str, float]]:
    """Få posisjonen for en gitt person

    Returns:
        dict[str, dict[str, float]]: { verdi (lat/alt/long) => { mål (std/avg/median) => resultat } }
    """
    location_data = load_data.load_location_data()
    data_bundle = location_data.data.get(person)
    if data_bundle == None:
        raise ValueError(f"Dette er ikke et gyldig navn: {person}")
    data = data_bundle.data
    start, end = data_bundle.indexstamps
    filtered_data = data[[1, 2, 3], start:end]
    filtered_data_fields = np.array(location_data.data_fields)[[1, 2, 3]]
    return analyze_location_data(filtered_data, filtered_data_fields, person)


def analyze_location_data(
    measurement_data: np.ndarray, datafields: np.ndarray, person: str, save: bool = True
) -> dict[str, dict[str, float]]:
    results: dict[str, dict[str, float]] = {}
    for data, datafield in zip(measurement_data, datafields):
        data_results = {
            "avg": np.mean(data),
            "median": np.median(data),
            "stdev": tstd(data),
        }
        results[datafield] = data_results
    if save:
        load_data.save_results(results, Path("Location") / f"{person}_location.toml")
    return results
