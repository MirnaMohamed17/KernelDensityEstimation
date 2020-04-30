import csv
import argparse
import numpy as np
import random
from matplotlib import pyplot
from sklearn.neighbors import KernelDensity


def options():
    """
    Options

    Parser to the inputs of the program

    :return: arguments parsed through the program run
    """
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-d", "--data", type=str, required=False, default="data/nph-nstedAPI.csv",
                        help="Dataset path")
    args = parser.parse_args()
    return args


def get_data(exoplanets_file_path):
    """
    Get Data

    Reads input csv file as a dictionary and returns list of dictionaries
    :param exoplanets_file_path: (str) the path of the csv file having the data
    :return: list of dictionaries of the file content
    """
    data = []
    with open(exoplanets_file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append({
                "pl_name": row['pl_name'],
                "pl_bmassj": row['pl_bmassj'],
                "pl_radj": row['pl_radj'],
                "pl_dens": row['pl_dens'],
                "st_mass": row['st_mass'],
                "st_rad": row['st_rad']
            })
    return data


# Working on plotting the M-R graph
def get_mean(p1, p2):
    return (p1[0] + p2[0]) / 2.0, (p1[1] + p2[1]) / 2.0


# Working on Sampling the masses with 120 limitation for data points
def slice_data(data, sep):
    radius_init = 0
    radius_fin = radius_init + sep
    ret_data_masses = []
    j = -1
    k = 0
    while True:
        if radius_init > 2.5:
            break
        random.shuffle(data)
        for i in range(len(data)):
            if i == 0:
                k = 0
                ret_data_masses.append([])
                j += 1
            if radius_init <= data[i][1] < radius_fin:
                ret_data_masses[j].append(data[i][0])
                k += 1
            if k > 120:
                break
        else:
            radius_init = radius_fin
            radius_fin = radius_init + sep
        if k > 120:
            radius_init = radius_fin
            radius_fin = radius_init + sep

    return np.array(ret_data_masses)


def main():
    # read the parsed arguments
    args = options()
    exoplanets_file_path = args.data

    # read file data
    planets_data = get_data(exoplanets_file_path)

    # generate a sample
    # sample = normal(loc=20, scale=5, size=300)
    # sample = normal(loc=40, scale=5, size=700)
    # sample = hstack((sample1, sample2))

    # get sample only from planet masses
    # stellar_mass = [float(planet["st_mass"]) for planet in planets_data if planet["st_mass"] and planet["st_rad"]]
    # stellar_mass = np.array(stellar_mass)
    #
    # stellar_radius = [float(planet["st_rad"]) for planet in planets_data if planet["st_mass"] and planet["st_rad"]]
    # stellar_radius = np.array(stellar_radius)

    planet_mass_radius = [[float(planet["pl_bmassj"]), float(planet["pl_radj"])]
                          for planet in planets_data if planet["pl_bmassj"] and planet["pl_radj"]]
    planet_mass_radius = np.array(planet_mass_radius)

    planet_mass_mean = []
    planet_radius_mean = []
    # print(planet_mass_radius)
    planet_mass_radius_sort = np.sort(planet_mass_radius, axis=0)
    # print(planet_mass_radius_sort)
    for i in range(len(planet_mass_radius_sort) - 1):
        x, y = get_mean(planet_mass_radius_sort[i], planet_mass_radius_sort[i + 1])
        planet_mass_mean.append(x)
        planet_radius_mean.append(y)

    # print(planet_mass_radius)
    # pyplot.scatter(planet_mass, planet_radius)
    pyplot.plot(planet_mass_mean, planet_radius_mean)
    pyplot.xlabel("Mass (planet mass)")
    pyplot.ylabel("Radius (planet radius)")
    pyplot.show()

    sliced_masses = slice_data(planet_mass_radius, 0.2)
    stacked_masses = np.hstack(sliced_masses)
    stacked_masses = stacked_masses.reshape((len(stacked_masses), 1))
    # fit density
    model = KernelDensity(bandwidth=0.02, kernel='gaussian')
    # planet_mass = planet_mass.reshape((len(planet_mass), 1))
    model.fit(stacked_masses)
    # shape of data is (n * f)

    # sample probabilities for a range of outcomes
    values = np.asarray([value / 2000 * 3 for value in range(2000)])
    values = values.reshape((len(values), 1))
    probabilities = model.score_samples(values)
    probabilities = np.exp(probabilities)
    # plot the histogram and pdf
    pyplot.hist(stacked_masses, bins=500, density=True)
    pyplot.plot(values[:], probabilities)
    pyplot.xlim(0.0, 2.5)
    pyplot.show()


if __name__ == '__main__':
    main()
