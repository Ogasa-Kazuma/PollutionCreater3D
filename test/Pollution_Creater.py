
import os, sys
sys.path.append(os.pardir)
import importlib


import Pollution_Creater
import matplotlib.pyplot as plt

importlib.reload(Pollution_Creater)

import PointClass
importlib.reload(PointClass)
from PointClass import Point

import Pollution
importlib.reload(Pollution)
from Pollution import Pollution


def RandomPollutions(pollutionCreater, pollutionField):
    for i in range(10):
        point_center = Point(x = 100, y = 100, z = 10)
        sphericalPollution = pollutionCreater.SphericalPollution(point_center, diameter = 10, pollution_at_center_point = 100)
        pollutionField.Add(sphericalPollution)

    return pollutionField

def main():

    pollutionCreater = Pollution_Creater.PollutionCreater()
    pollutionField = Pollution([[[0 for z in range(20)] for y in range(300)] for x in range(300)])
    sphericalPollution = RandomPollutions(pollutionCreater, pollutionField)


    xList, yList, zList, pollutionList = sphericalPollution.to_list()

    fig = plt.figure()
    ax = fig.add_subplot(111, projection = '3d')
    ax.scatter(xList, yList, zList, c = pollutionList, cmap = 'binary', alpha = 0.3)
    sphericalPollution.Save("unko.csv", format = 'csv')


if __name__ == "__main__":
    main()
