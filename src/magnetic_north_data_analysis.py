from __future__ import annotations
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import load_data

# ! Vemund har flippet y-aksen ?


def calculate_magnetic_field_reference_angle(
    B_x_array: np.ndarray, B_y_array: np.ndarray
) -> np.ndarray:
    return np.rad2deg(np.pi - np.arctan2(B_y_array, B_x_array))


def get_magnetic_field_reference_angles(measurement: str) -> dict[str, np.ndarray]:
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
