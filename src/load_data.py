from __future__ import annotations
import numpy as np
from pathlib import Path
from dataclasses import dataclass
import tomllib
import tomli_w

DATA_DIR = Path(__name__).parent / "Data"
RESULTS_DIR = Path(__name__).parent / "Results"


@dataclass
class Person:
    thorbjorn = "Thorb"
    oskar = "Oskar"
    vemund = "Vemund"


PERSONS = [Person.oskar, Person.thorbjorn, Person.vemund]


@dataclass
class Measurement:
    nidarosdomen = "Nidarosdomen"
    tyholt = "Tyholt"
    tyholt_restart = "Tyholt_restart"
    tyholt_flymodus = "Tyholt_flymodus"


MEASUREMENTS = [
    Measurement.nidarosdomen,
    Measurement.tyholt,
    Measurement.tyholt_restart,
    Measurement.tyholt_flymodus,
]


@dataclass
class RawDataObject:
    """
    Inneholder data

    data: np.ndarray (dataene fra én måleserie)
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
    { person_navn => { måling => RawDataObject } }

    data_fields:
    [ navn på datafeltene i dataene i rekkefølgen til kolonnene til dataene ]
    """

    data: dict[str, dict[str, RawDataObject]]
    data_fields: list[str]


@dataclass
class LocationData:
    """
    Klasse for å håndtere lokasjonsdataene

    data:
    { person_navn => RawDataObject }

    data_fields:
    [ navn på datafeltene i dataene i rekkefølgen til kolonnene til dataene ]
    """

    data: dict[str, RawDataObject]
    data_fields: list[str]


@dataclass
class ResultsObject:
    """
    Klasse for å kunne returnere resultatene

    declination:
    { måling => { navn => { resultattype => data } } }

    inclination:
    { måling => { navn => { resultattype => data } } }
    """

    declination: dict[str, dict[str, dict[str, float]]]
    inclination: dict[str, dict[str, dict[str, float]]]


def get_index_stamps(
    time_array: np.ndarray, timestamps: tuple[float, float]
) -> tuple[int, int]:
    delta_t = time_array[11] - time_array[10]
    index_0 = int((timestamps[0] - time_array[1]) / delta_t)
    index_1 = int((timestamps[1] - time_array[1]) / delta_t)
    return (index_0, index_1)


def load_magnetic_field_data() -> MagneticFieldData:
    """Laster inn de magnetiske dataene i alle undermappene av Data og grupperer dem etter person og måling.

    Returns:
        DataObject: Et objekt som inneholder dataene.
    """
    magnetic_field_data_dict = {}
    for person_dir in DATA_DIR.iterdir():
        person_data_files = person_dir.rglob("*[!Location]*/Raw Data.csv")
        timestamps_file = person_dir / "timestamps.toml"
        person_data_dict: dict[str, RawDataObject] = {}
        timestamps_dict: dict[str, dict[str, int]] = tomllib.load(
            timestamps_file.open("rb")
        )

        for measurement_file in person_data_files:
            data = np.loadtxt(
                measurement_file,
                skiprows=1,
                delimiter=",",
                unpack=True,
            )
            measurement_name = measurement_file.parent.name
            timestamps = (
                timestamps_dict[measurement_name]["start"],
                timestamps_dict[measurement_name]["end"],
            )
            index_stamps = get_index_stamps(data[0], timestamps)
            person_data_dict[measurement_name] = RawDataObject(
                data, timestamps, index_stamps
            )

        magnetic_field_data_dict[person_dir.name] = person_data_dict

    data_fields = [
        r"Time (s)",
        r"Magnetic Field x $[\mu T]$",
        r"Magnetic Field y $[\mu T]$",
        r"Magnetic Field z $[\mu T]$",
        r"Absolute field $[\mu T]$",
    ]
    return MagneticFieldData(magnetic_field_data_dict, data_fields)


def load_location_data() -> LocationData:
    """Laster inn lokasjonsdataene i person-mappen som blir gitt som argument.

    Returns:
        np.ndarray: Et array med dataene i lokasjonsmappen
    """
    location_data_dict = {}
    for person_dir in DATA_DIR.iterdir():
        location_file = person_dir / "Location/Raw Data.csv"
        timestamps_file = person_dir / "timestamps.toml"
        timestamps_dict: dict[str, dict[str, float]] = tomllib.load(
            timestamps_file.open("rb")
        )
        data = np.loadtxt(
            location_file,
            skiprows=1,
            delimiter=",",
            unpack=True,
            usecols=[0, 1, 2, 3, 9, 10],
        )
        measurement_name = location_file.parent.name
        timestamps = (
            timestamps_dict[measurement_name]["start"],
            timestamps_dict[measurement_name]["end"],
        )
        index_stamps = get_index_stamps(data[0], timestamps)

        location_data_dict[person_dir.name] = RawDataObject(
            data, timestamps, index_stamps
        )

    data_fields = [
        "Time (s)",
        "Latitude (deg)",
        "Longitude (deg)",
        "Altitude (m)",
        "Horizontal Accuracy (m)",
        "Vertical Accuracy (m)",
    ]
    return LocationData(location_data_dict, data_fields)


def load_results() -> ResultsObject:
    inclination_dict = {}
    declination_dict = {}
    DECLINATION_DIR = RESULTS_DIR / "Declination"
    INCLINATION_DIR = RESULTS_DIR / "Inclination"
    for file in DECLINATION_DIR.iterdir():
        with open(file, "rb") as f:
            results: dict[str, dict[str, float]] = tomllib.load(f)
        declination_dict[file.name] = results
    for file in INCLINATION_DIR.iterdir():
        with open(file, "rb") as f:
            results: dict[str, dict[str, float]] = tomllib.load(f)
        inclination_dict[file.name] = results
    return ResultsObject(declination_dict, inclination_dict)


def save_results(results: dict, filepath: Path) -> None:
    RESULTS_DIR = Path(__name__).parent / "Results"
    with open(RESULTS_DIR / filepath, "wb") as f:
        tomli_w.dump(results, f)
