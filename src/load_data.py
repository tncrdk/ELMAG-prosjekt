from __future__ import annotations
import numpy as np
from pathlib import Path
from dataclasses import dataclass

DATA_DIR = Path(__name__).parent / "Data"


@dataclass
class MagneticFieldData:
    """
    Klasse for å gruppere magnetisk-felt data
    person_data: {person_navn => {måling => dataene}}
    data_fields: [navn på datafeltet i dataene]
    """

    person_data: dict[str, dict[str, np.ndarray]]
    data_fields: list[str]


@dataclass
class LocationData:
    person_data: dict[str, np.ndarray]
    data_fields: list[str]


def load_magnetic_field_data() -> MagneticFieldData:
    """Laster inn de magnetiske dataene i person-mappen som blir gitt som argument.

    Args:
        person_directory (Path): _description_

    Returns:
        DataObject: Et objekt som inneholder data.
    """
    person_data = {}
    for person_dir in DATA_DIR.iterdir():
        person_data_files = person_dir.rglob("*[!Location]*/Raw Data.csv")
        person_data_dict = {}
        for file in person_data_files:
            data = np.loadtxt(
                file,
                skiprows=1,
                delimiter=",",
                unpack=True,
            )
            person_data_dict[file.parent.name] = data

        person_data[person_dir.name] = person_data_dict

    data_fields = [
        "Time (s)",
        "Magnetic Field x (µT)",
        "Magnetic Field y (µT)",
        "Magnetic Field z (µT)",
        "Absolute field (µT)",
    ]
    return MagneticFieldData(person_data, data_fields)


def load_location_data() -> LocationData:
    """Laster inn lokasjonsdataene i person-mappen som blir gitt som argument.

    Args:
        person_directory (Path): _description_

    Returns:
        np.ndarray: Et array med dataene i lokasjonsmappen
    """
    data_dict = {}
    for person_dir in DATA_DIR.iterdir():
        location_files = person_dir.rglob("Location/Raw Data.csv")
        data = np.array([])
        for file in location_files:
            data = np.loadtxt(
                file,
                skiprows=1,
                delimiter=",",
                unpack=True,
                usecols=[0, 1, 2, 3, 9, 10],
            )
        data_dict[person_dir.name] = data

    data_fields = [
        "Time (s)",
        "Latitude (deg)",
        "Longitude (deg)",
        "Altitude (m)",
        "Horizontal Accuracy (m)",
        "Vertical Accuracy (m)",
    ]
    return LocationData(data_dict, data_fields)
