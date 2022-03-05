
import importlib
import Pollution
importlib.reload(Pollution)
from Pollution import Pollution

import PointClass
importlib.reload(PointClass)
from PointClass import Point

import statistics


class PollutionCreater:

    def __init__(self):
        pass

    def SphericalPollution(self, point_center, diameter, pollution_at_center_point):

        ##diameterが奇数や小数のときは受け付けないようにすべき？

        x_range, y_range, z_range, sphericalPollution = self.__CalcXYZ_Limits(point_center, diameter)

        for x_i in x_range:
            for y_i in y_range:
                for z_i in z_range:
                    pollutionPoint = Point(x_i, y_i, z_i)
                    distance = pollutionPoint.distance(point_center)
                    sphericalPollution[x_i][y_i][z_i] = self.__CalcPollutionAtOnePoint(distance, diameter, pollution_at_center_point)

        sphericalPollution = Pollution(sphericalPollution)
        return sphericalPollution



    def __CalcXYZ_Limits(self, point_center, diameter):
        radius = int(diameter / 2)
        x_range = range(point_center.GetX() - radius, point_center.GetX() + radius + 1)
        y_range = range(point_center.GetY() - radius, point_center.GetY() + radius + 1)
        z_range = range(point_center.GetZ() - radius, point_center.GetZ() + radius + 1)
        sphericalPollution = [[[0 for z in range(max(z_range) + 1)] for y in range(max(y_range) + 1)] for x in range(max(x_range) + 1)]


        return x_range, y_range, z_range, sphericalPollution


    def __CalcPollutionAtOnePoint(self, distance, diameter, pollution_at_center_point):
        radius = diameter / 2
        pollution_decreasing_per_meter =  pollution_at_center_point / radius
        pollution = pollution_at_center_point - (pollution_decreasing_per_meter * distance)
        pollution = self.__DeleteMinusPollution(pollution)
        return pollution

    def __DeleteMinusPollution(self, pollution):
        if(pollution < 0):
            return 0
        return pollution
