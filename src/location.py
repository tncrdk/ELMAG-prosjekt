from __future__ import annotations
import numpy as np
from geopy import distance
import load_data
from dataclasses import dataclass
from scipy.stats import tstd
from pathlib import Path
import tomllib

DIR_PATH_RESULTS_LOCATION = Path(__name__).parent / "Results" / "Location"

# Fra google maps:
coord_nidaros = (63.42690834516923, 10.396940527455543)
coord_tyholt = (63.422364810418905, 10.431957717382154)

@dataclass
class Location:
    altitude: dict[str, float]
    longitude: dict[str, float]
    latitude: dict[str, float]


def convert_to_rad(coord: list) -> None:
    for i in range(len(coord)):
        coord[i] = np.radians(coord[i])

def distance_geopy(p1, p2):
    return distance.geodesic(p1, p2, ellipsoid="WGS-84").m

def calculate_angle_north():
    '''
    Returns: dict med filnavn som key og dict med verdier for vinkler (grad) som values.
    e.g.: {'navn_location.toml': {'nidaros': 25, 'tyholt': 80}}
    '''
    loc_data = {}
    for pth in DIR_PATH_RESULTS_LOCATION.iterdir():
        with open(pth, 'rb') as f:
            loc_data[pth.name] = tomllib.load(f)

    north_referance_angle_dict = {}
    for key, item in loc_data.items():
        coord_maalepunkt = (item['Latitude (deg)']['avg'], item['Longitude (deg)']['avg'])
    
        # tre punkter i rettvinklet trekant. arctan gir vinkel.
        # NIDAROS
        fortegn = np.sign(coord_maalepunkt[1] - coord_nidaros[1])
        rettvinklet_nidaros = (coord_nidaros[0], coord_maalepunkt[1])
        katet_nidaros_1 = distance_geopy(rettvinklet_nidaros, coord_maalepunkt)
        katet_nidaros_2 = distance_geopy(rettvinklet_nidaros, coord_nidaros)

        angle_nidaros = fortegn*np.degrees(np.arctan2(katet_nidaros_2, katet_nidaros_1))

        #TYHOLT
        fortegn = np.sign(coord_maalepunkt[1] - coord_tyholt[1])
        rettvinklet_tyholt = (coord_tyholt[0], coord_maalepunkt[1])

        katet_tyholt_1 = distance_geopy(rettvinklet_tyholt, coord_maalepunkt)
        katet_tyholt_2 = distance_geopy(rettvinklet_tyholt, coord_tyholt)

        angle_tyholt = fortegn*np.degrees(np.arctan2(katet_tyholt_2, katet_tyholt_1))

        north_referance_angle_dict[key] = {'nidaros': angle_nidaros, 'tyholt': angle_tyholt}
    return north_referance_angle_dict


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
