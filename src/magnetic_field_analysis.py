from __future__ import annotations
import numpy as np
import load_data


# ! Vemund har flippet y-aksen ?


def calculate_magnetic_field_reference_angle(
    B_x_array: np.ndarray, B_y_array: np.ndarray
) -> np.ndarray:
    return np.rad2deg(np.pi - np.arctan2(B_y_array, B_x_array))


def calculate_inclination(
    B_x_array: np.ndarray, B_y_array: np.ndarray, B_z_array: np.ndarray
) -> np.ndarray:
    B_xy_plane = np.sqrt(B_x_array**2 + B_y_array**2)
    return np.rad2deg(np.arctan(-B_z_array / B_xy_plane))
    # negativ B_z fordi den allerede er negativ => negativ theta,
    # men inklinasjonen er oppgitt som positiv


def get_magnetic_field_reference_angles(measurement: str) -> dict[str, np.ndarray]:
    """_summary_

    Args:
        measurement (str): hvilken måling en ser på

    Raises:
        ValueError: measurement gitt inn finnes ikke

    Returns:
        dict[str, np.ndarray]: { person => [tid_array, vinkel_array] }
    """
    person_angle_dict = {}
    magfield_data_obj = load_data.load_magnetic_field_data()
    for person, data_dict in magfield_data_obj.data.items():
        rawdata_obj = data_dict.get(measurement)
        if rawdata_obj == None:
            continue
        start, slutt = rawdata_obj.indexstamps
        rawdata = rawdata_obj.data[:, start:slutt]
        angles_array = calculate_magnetic_field_reference_angle(rawdata[1], rawdata[2])
        time = rawdata[0]
        person_angle_dict[person] = np.vstack((time, angles_array))

    if len(person_angle_dict.keys()) == 0:
        raise ValueError(f"Ingen målinger med dette navnet: {measurement}")
    return person_angle_dict


def get_inclination(measurement: str) -> dict[str, np.ndarray]:
    """_summary_

    Args:
        measurement (str): Hvilken måling ser du på

    Raises:
        ValueError: _description_

    Returns:
        dict[str, np.ndarray]: _description_
    """
    person_inclination_dict = {}
    location_data_obj = load_data.load_magnetic_field_data()
    for person, data_dict in location_data_obj.data.items():
        rawdata_obj = data_dict.get(measurement)
        if rawdata_obj == None:
            continue
        start, slutt = rawdata_obj.indexstamps
        data = rawdata_obj.data[:, start:slutt]
        inclination = calculate_inclination(data[1], data[2], data[3])
        person_inclination_dict[person] = np.vstack((data[0], inclination))

    if len(person_inclination_dict.keys()) == 0:
        raise ValueError(f"Ingen målinger med dette navnet: {measurement}")
    return person_inclination_dict
