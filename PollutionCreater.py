

class PollutionCreater:

    def __init__(self):
        pass

    def SphericalPollution(self, diameter, pollution_at_center_point):

        ##diameterが奇数や小数のときは受け付けないようにすべき？


        sphericalPollution = list()

        for x_i in range(0, diameter + 1):
            for y_i in range(0, diameter + 1):
                for z_i in range(0, diameter + 1):
                    pollutionPoint = Point(x_i, y_i, z_i)
                    distance = self.__CalcDistanceFromCenter(pollutionPoint, diameter)
                    sphericalPollution[x_i][y_i][z_i] = self.__CalcPollutionAtOnePoint(distance, pollution_at_center_point)

        sphericalPollution = Pollution(sphericalPollution)
        return sphericalPollution


    def __CalcDistanceFromCenter(self, pollutionPoint, diameter):

        centerPoint = Point(x = (diameter / 2), y = (diameter / 2), z = (diameter / 2))

        distance = pollutionPoint.distance(centerPoint)

        return distance



    def __Calc_Decreasing_Per_Distance(self, diameter, pollution_min, pollution_max):
        pollution_range = pollution_max - pollution_min
        decreasing_per_distance = pollution_range / diameter
        return decreasing_per_distance

    def __CalcPollutionAtOnePoint(self, distance):
        pollution_decreasing_ratio = self.__Calc_Decreasing_Per_Distance(diameter, pollution_min, pollution_max)
