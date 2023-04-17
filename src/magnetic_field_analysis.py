from __future__ import annotations
import numpy as np
from scipy.stats import tstd
import tomli_w
from pathlib import Path
import load_data


# ! Vemund har flippet y-aksen ?


def calculate_magnetic_field_reference_angle(
    B_x_array: np.ndarray, B_y_array: np.ndarray
) -> np.ndarray:
    """Beregner vinkelen mellom magnetfeltet og referansepunktet (langs negativ x-akse)

    Args:
        B_x_array (np.ndarray): Feltet i x-retning
        B_y_array (np.ndarray): Feltet i y-retning

    Returns:
        np.ndarray: vinkel_array (grader)
    """
    return np.rad2deg(np.pi - np.arctan2(B_y_array, B_x_array))


def calculate_inclination(
    B_x_array: np.ndarray, B_y_array: np.ndarray, B_z_array: np.ndarray
) -> np.ndarray:
    B_xy_plane = np.sqrt(B_x_array**2 + B_y_array**2)
    return np.rad2deg(np.arctan(-B_z_array / B_xy_plane))
    # negativ B_z fordi den allerede er negativ => negativ theta,
    # men inklinasjonen er oppgitt som positiv


def calculate_declination(
    field_reference_angles: np.ndarray, north_reference_angle: float
) -> np.ndarray:
    """Kalkulerer deklinasjonen

    Args:
        field_reference_angles (np.ndarray): vinkel_array (grader) mellom magnetfelt og referansepunkt
        north_reference_angle (float): vinkel_array (grader) mellom geografisk nord og referansepunkt

    Returns:
        np.ndarray: deklinasjon_array (grader)
    """
    return field_reference_angles - north_reference_angle


def get_magnetic_field_reference_angles_dict(measurement: str) -> dict[str, np.ndarray]:
    """_summary_

    Args:
        measurement (str): hvilken måling en ser på

    Raises:
        ValueError: målingen tatt inn som argument finnes ikke

    Returns:
        dict[str, np.ndarray]: { person => [tid_array, vinkel_array] }
    """
    person_angle_dict = {}
    magfield_data_obj = load_data.load_magnetic_field_data()
    for person, data_dict in magfield_data_obj.data.items():
        rawdata_obj = data_dict.get(measurement)
        if rawdata_obj == None:
            continue
        start, end = rawdata_obj.indexstamps
        rawdata = rawdata_obj.data[:, start:end]
        angles_array = calculate_magnetic_field_reference_angle(rawdata[1], rawdata[2])
        time = rawdata[0]
        person_angle_dict[person] = np.vstack((time, angles_array))

    if len(person_angle_dict.keys()) == 0:
        raise ValueError(f"Ingen målinger med dette navnet: {measurement}")
    return person_angle_dict


def get_inclination_dict(measurement: str) -> dict[str, np.ndarray]:
    """Henter ut alle resultatene fra en bestemt måling

    Args:
        measurement (str): Hvilken måling ser du på

    Raises:
        ValueError: Dersom målingen ikke eksisterer

    Returns:
        dict[str, np.ndarray]: { person => [tid_array, inklinasjon_array] }
    """
    person_inclination_dict = {}
    location_data_obj = load_data.load_magnetic_field_data()
    for person, data_dict in location_data_obj.data.items():
        rawdata_obj = data_dict.get(measurement)
        if rawdata_obj == None:
            continue
        start, end = rawdata_obj.indexstamps
        data = rawdata_obj.data[:, start:end]
        inclination = calculate_inclination(data[1], data[2], data[3])
        person_inclination_dict[person] = np.vstack((data[0], inclination))

    if len(person_inclination_dict.keys()) == 0:
        raise ValueError(f"Ingen målinger med dette navnet: {measurement}")
    return person_inclination_dict


def analyze_results(
    results_dict: dict[str, np.ndarray],
    measurement_type: str,
    measurement_name: str,
    save: bool = True,
) -> dict[str, dict[str, float]]:
    """utfører en analyse av alle dataene for en gitt måling

    Args:
        inclination_dict (dict[str, np.ndarray]): { person => resultater_array } (Alt gjelder for én bestemt måling)
        measurement_type: Inklinasjon eller deklinasjon
        measurement_name (str): Navn på målingen
        save_results (bool, optional): Hvorvidt man skal lagre resultatene i en fil. Defaults to True.

    Returns:
        dict[str, dict[str, float]]: { person => { mål (avg, stdev, o.l.) => resultat } } (For en gitt måling)
    """
    if not (measurement_type == "Inclination" or measurement_type == "Declination"):
        raise ValueError(
            f"Measurement_type skal enten være 'Deklinasjon' eller 'Inklinasjon', ikke: {measurement_type}"
        )
    results: dict[str, dict[str, float]] = {}
    for person, results_array in results_dict.items():
        angles_array = results_array[1]
        person_result = {
            "avg": np.mean(angles_array),
            "median": np.median(angles_array),
            "stdev": tstd(angles_array),
        }
        results[person] = person_result
    if save:
        load_data.save_results(
            results, Path(measurement_type) / f"{measurement_name}.toml"
        )
    return results


def get_declination(measurement, angle_input_dict, save = True):
    """
    angle: {'person': angle}
    """
    tot_dict = get_magnetic_field_reference_angles_dict(measurement)
    results = {}
    for i, j in tot_dict.items():
        for k in range(len(j[1])):
            angle = angle_input_dict[i]
            tot_dict[i][1][k] = calculate_declination(j[1][k], angle)
    
    for l in tot_dict.keys():
        angle_array = tot_dict[l][1]
        internal_dict = {
            "Average": np.average(angle_array),
            "Median": np.median(angle_array),
            "Stdev" : tstd(angle_array)
        }

        results[l] = internal_dict

    if save:
        load_data.save_results(
            results, Path('Declination') / f"{measurement}.toml"
        )
    return results



