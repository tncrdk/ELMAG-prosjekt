import load_data
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap
from pathlib import Path

PERSON_COLORS = {
    load_data.Person.thorbjorn: 0,
    load_data.Person.oskar: 1,
    load_data.Person.vemund: 2,
}

PERSON_PHONE = {
    load_data.Person.thorbjorn: "iPhone SE",
    load_data.Person.oskar: "Samsung Galaxy A40",
    load_data.Person.vemund: "iPhone 13",
}

RESULTS_DIR = Path(__name__).parent / "Plots" / "Results"


def scatter_plot_declination():
    results = load_data.load_results()
    declination_dict = results.declination
    fig, ax = plt.subplots(subplot_kw={"projection": "polar"})
    angle_list = []
    radius_list = []
    phone_color_list = []
    radius = 0.4
    d_radius = 0.05
    for measurement_dict in declination_dict.values():
        for person, result_dict in measurement_dict.items():
            angle = result_dict["Average"]
            angle_rad = np.deg2rad(angle)
            angle_list.append(angle_rad)
            radius_list.append(radius)
            phone_color_list.append(PERSON_COLORS[person])
            radius += d_radius

    scatter = ax.scatter(
        angle_list,
        radius_list,
        s=30,
        c=phone_color_list,
        cmap=ListedColormap(["red", "darkblue", "orange"]),
        alpha=0.75,
    )
    ax.scatter(0, 1, s=0.01)
    ax.set_title("Deklinasjon")
    ax.set_thetamin(-90)
    ax.set_thetamax(90)
    ax.set_theta_direction(-1)
    ax.set_theta_zero_location("N")
    ax.set_yticklabels([])
    ticks = np.arange(-np.pi / 2, np.pi / 2 + 0.1, np.pi / 12)
    ticks[np.round(ticks, 3) == 0] = 0
    ax.xaxis.set_ticks(ticks)
    ax.tick_params(axis="x", which="major", pad=10)
    ax.text(-0.05, 1.14, "N", fontsize=23)
    ax.text(-np.pi / 2 * 1.08, 1.1, "W", fontsize=23)
    ax.text(np.pi / 2 * 1.1, 1, "E", fontsize=23)
    # produce a legend with the unique colors from the scattenr
    ax.legend(
        handles=scatter.legend_elements()[0],
        loc=(0.8, 0.8),
        title="Person",
        labels=PERSON_PHONE.values(),
    )
    fig.savefig(RESULTS_DIR / "declination.pdf")
    fig.savefig(RESULTS_DIR / "declination.png")
    fig.clear()


def scatter_plot_inclination():
    results = load_data.load_results()
    inclination_dict = results.inclination
    fig, ax = plt.subplots(subplot_kw={"projection": "polar"})
    angle_list = []
    radius_list = []
    person_color_list = []
    radius = 0.4
    d_radius = 0.05
    for measurement_dict in inclination_dict.values():
        for person, result_dict in measurement_dict.items():
            angle = result_dict["Average"]
            angle_rad = np.deg2rad(angle)
            angle_list.append(angle_rad)
            radius_list.append(radius)
            person_color_list.append(PERSON_COLORS[person])
            radius += d_radius

    scatter = ax.scatter(
        angle_list,
        radius_list,
        s=30,
        c=person_color_list,
        cmap=ListedColormap(["red", "darkblue", "orange"]),
        alpha=0.75,
    )
    ax.scatter(0, 1, s=0.01)
    ax.set_title("Inklinasjon")
    ax.set_thetamin(0)
    ax.set_thetamax(90)
    ax.set_theta_direction(-1)
    ax.set_yticklabels([])
    ticks = np.arange(0, np.pi / 2 + 0.1, np.pi / 12)
    ticks[np.round(ticks, 3) == 0] = 0
    ax.xaxis.set_ticks(ticks)
    ax.tick_params(axis="x", which="major", pad=10)
    # produce a legend with the unique colors from the scattenr
    ax.legend(
        handles=scatter.legend_elements()[0],
        loc=(0.75, 0),
        title="Person",
        labels=PERSON_PHONE.values(),
    )
    fig.savefig(RESULTS_DIR / "inclination.pdf")
    fig.savefig(RESULTS_DIR / "inclination.png")
    fig.clear()
