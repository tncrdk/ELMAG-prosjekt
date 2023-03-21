from __future__ import annotations
import numpy as np
from pathlib import Path
from dataclasses import dataclass
import tomllib

DATA_DIR = Path(__name__).parent / "Data"


"""
[Objekt]
datafields
data

[Object.data]
person

[Object.data.Person]
måling

[Object.data.person.måling]
data
timestamp 
indexstamp
"""


@dataclass
class RawDataObject:
    """
    Inneholder data

    data: np.ndarray
    timestamps: tuple[float, float]
    indexstamps: tuple[int, int]
    """

    data: np.ndarray
    timestamps: tuple[float, float]
    indexstamps: tuple[int, int]


@dataclass
class MagneticFieldData:
    """
    Klasse for å håndtere magnetfelt-dataene.

    magnetic_field_data:
    { person_navn => { måling => dataObject } }

    data_fields:
    [ navn på datafeltene i dataene i rekkefølgen til kolonnene til dataene ]
    """

    data: dict[str, dict[str, RawDataObject]]
    data_fields: list[str]


@dataclass
class LocationData:
    """
    Klasse for å håndtere lokasjonsdataene

    location_data:
    { person_navn => data: np.ndarray }

    data_fields:
    [ navn på datafeltene i dataene i rekkefølgen til kolonnene til dataene ]
    """

    data: dict[str, RawDataObject]
    data_fields: list[str]


def load_magnetic_field_data() -> MagneticFieldData:
    """Laster inn de magnetiske dataene i alle undermappene av Data og grupperer dem etter person og måling.

    Returns:
        DataObject: Et objekt som inneholder dataene.
    """
    magnetic_field_data_dict = {}
    for person_dir in DATA_DIR.iterdir():
        person_data_files = person_dir.rglob("*[!Location]*/Raw Data.csv")
        timestamps_file, _ = person_dir.glob("timestamps.toml")
        timestamps: dict[str, dict[str, str]] = tomllib.load(timestamps_file.open("b"))
        person_data_dict = {}

        for measurement_file in person_data_files:
            data = np.loadtxt(
                measurement_file,
                skiprows=1,
                delimiter=",",
                unpack=True,
            )
            person_data_dict[measurement_file.parent.name] = data

        magnetic_field_data_dict[person_dir.name] = person_data_dict

    data_fields = [
        r"Time (s)",
        r"$Magnetic Field x (\mu T)$",
        r"$Magnetic Field y (\mu T)$",
        r"$Magnetic Field z (\mu T)$",
        r"$Absolute field (\mu T)$",
    ]
    return MagneticFieldData(magnetic_field_data_dict, data_fields)


def load_location_data() -> LocationData:
    """Laster inn lokasjonsdataene i person-mappen som blir gitt som argument.

    Args:
        person_directory (Path): _description_

    Returns:
        np.ndarray: Et array med dataene i lokasjonsmappen
    """
    location_data_dict = {}
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
        location_data_dict[person_dir.name] = data

    data_fields = [
        "Time (s)",
        "Latitude (deg)",
        "Longitude (deg)",
        "Altitude (m)",
        "Horizontal Accuracy (m)",
        "Vertical Accuracy (m)",
    ]
    return LocationData(location_data_dict, data_fields)
