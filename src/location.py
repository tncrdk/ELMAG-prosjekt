from __future__ import annotations
import numpy as np
from geopy import distance
from geographiclib.geodesic import Geodesic
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

def calculate_angle_north():
    '''
    Uses location data in ./Data/Location/ to calculate angles (azimuts)

    Returns: dict {MEASURMENT: {PERSON: angle}}
    e.g.: {'Nidarosdomen': {'Oskar': 25.144, 'Thorb': 25.4857}}
    '''
    loc_data = {}
    for pth in DIR_PATH_RESULTS_LOCATION.iterdir():
        name = pth.name.split('_')[0]
        with open(pth, 'rb') as f:
            loc_data[name] = tomllib.load(f)

    north_reference_angle_dict = {}
    measure_person = [(m, p) for m in load_data.MEASUREMENTS for p in load_data.PERSONS]
    for (m, p) in measure_person:
        if not m in north_reference_angle_dict:
            north_reference_angle_dict[m] = {}
        north_reference_angle_dict[m][p] = NotImplemented

    for name, item in loc_data.items():
        angle: int = None
        coord_maalepunkt = (item['Latitude (deg)']['avg'], item['Longitude (deg)']['avg'])

        for measurement in load_data.MEASUREMENTS:
            if measurement == load_data.Measurement.nidarosdomen:
                angle = -1 * Geodesic.WGS84.Inverse(*coord_maalepunkt, *coord_nidaros)['azi1']
            else:
                angle = -1 * Geodesic.WGS84.Inverse(*coord_maalepunkt, *coord_tyholt)['azi1']
            
            north_reference_angle_dict[measurement][name] = angle

    return north_reference_angle_dict


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

if __name__ == "__main__":
    dictio = calculate_angle_north()
    print(dictio)