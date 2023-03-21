import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

FOLDER_PATH = Path(__name__).parent / "Plots"


def plot_one_to_one(
    x_array: np.ndarray,
    y_array: np.ndarray,
    legend: str,
    xlabel: str,
    ylabel: str,
    title: str,
    filepath: str | None = None,
) -> None:
    """Function that plots one set of data. One list of x-values and one list of y-values

    Args:
        x_array (np.ndarray): x-values
        y_array (np.ndarray): y-values
        legend (str): _description
        xlabel (str): _description_
        ylabel (str): _description_
        title (str): _description_
        file_path (Optional str): Hvis plottet skal lagres må en filsti legges ved
    """
    plt.plot(x_array, y_array, label=legend)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    save_or_show_plot(filepath)


def plot_one_to_many(
    x_array: np.ndarray,
    y_arrays: list[np.ndarray],
    legends: list[str],
    xlabel: str,
    ylabel: str,
    title: str,
    filepath: str | None = None,
) -> None:
    """Function that plots multiple sets of data. All the x-values arrays goes in x_arrays, and likewise for y_arrays.

    Args:
        x_arrays (list[np.ndarray]): _description_
        y_arrays (list[np.ndarray]): _description_
        legends (list[str]): _description_
        xlabel (str): _description_
        ylabel (str): _description_
        title (str): _description_
        file_path (Optional str): Hvis plottet skal lagres må en filsti legges ved
    """
    for y_array, legend in zip(y_arrays, legends):
        plt.plot(x_array, y_array, label=legend)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    save_or_show_plot(filepath)


def plot_many_to_many(
    x_arrays: list[np.ndarray],
    y_arrays: list[np.ndarray],
    legends: list[str],
    xlabel: str,
    ylabel: str,
    title: str,
    filepath: str | None = None,
) -> None:
    """Function that plots multiple sets of data. All the x-values arrays goes in x_arrays, and likewise for y_arrays.

    Args:
        x_arrays (list[np.ndarray]): _description_
        y_arrays (list[np.ndarray]): _description_
        legends (list[str]): _description_
        xlabel (str): _description_
        ylabel (str): _description_
        title (str): _description_
        file_path (Optional str): Hvis plottet skal lagres må en filsti legges ved
    """
    for x_array, y_array, legend in zip(x_arrays, y_arrays, legends):
        plt.plot(x_array, y_array, label=legend)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    save_or_show_plot(filepath)


def save_or_show_plot(filepath: str | None):
    if filepath:
        save_path = FOLDER_PATH / f"{filepath}.svg"
        plt.savefig(save_path)
    else:
        plt.show()
    plt.cla()
