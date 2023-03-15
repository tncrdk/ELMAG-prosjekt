import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

FOLDER_PATH = Path(__name__).parent / "Plots"


def plot_one_dataset(
    x_array: np.ndarray,
    y_array: np.ndarray,
    legend: str,
    xlabel: str,
    ylabel: str,
    title: str,
    file_name: str,
) -> None:
    """Function that plots one set of data. One list of x-values and one list of y-values

    Args:
        x_array (np.ndarray): x-values
        y_array (np.ndarray): y-values
        legend (str): _description
        xlabel (str): _description_
        ylabel (str): _description_
        title (str): _description_
        file_name (str): _description_
    """
    save_path = FOLDER_PATH / f"{file_name}.svg"
    plt.plot(x_array, y_array, label=legend)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.savefig(save_path)


def plot_multiple_datasets(
    x_arrays: list[np.ndarray],
    y_arrays: list[np.ndarray],
    legends: list[str],
    xlabel: str,
    ylabel: str,
    title: str,
    filename: str,
) -> None:
    """Function that plots multiple sets of data. All the x-values arrays goes in x_arrays, and likewise for y_arrays.

    Args:
        x_arrays (list[np.ndarray]): _description_
        y_arrays (list[np.ndarray]): _description_
        legends (list[str]): _description_
        xlabel (str): _description_
        ylabel (str): _description_
        title (str): _description_
        filename (str): _description_
    """
    file_path = FOLDER_PATH / f"{filename}.svg"
    for x_array, y_array, legend in zip(x_arrays, y_arrays, legends):
        plt.plot(x_array, y_array, legend)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.savefig(file_path)
