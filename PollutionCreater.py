

class PollutionCreater:

    def __init__(self):
        pass

    def SphericalPollution(self, radius, pollution_min, pollution_max):

        ##radiusが偶数や小数のときは受け付けないようにすべき？
        pollution_decreasing_ratio = self.__Calc_Decreasing_Per_Distance(radius, pollution_min, pollution_max)
        #汚染源の中心座標を計算
        centerPoint = self.__DecideCenterPoint(radius)
        #中心座標から離れるほど濃度を低く計算
        self.__CalcPollutionsCorrespondingTo_xyzPoints(centerPoint, radius, pollution_decreasing_ratio)


        return sphericalPollution

    def __CalcPollutionsCorrespondingTo_xyzPoints(centerPoint, radius, pollution_decreasing_ratio):


        sphericalPollution = list()

        for x_i in range(0, radius + 1):
            for y_i in range(0, radius + 1):
                for z_i in range(0, radius + 1):
                    self.__CalcDistanceFromCenter()
                    sphericalPollution[x_i][y_i][z_i] = self.__CalcPollutionAtOnePoint()



    def __CalcDistanceFromCenter(self, radius, x, y, z):
        for x_count in range(0, radius + 1):
            for y_count in range(0, radius + 1):
                for z_count in range(0, radius + 1):
                        pollutionPoint = Point(x_i, y_i, z_i)
                        distance = pollutionPoint.distance(centerPoint)

        return distance



    def __Calc_Decreasing_Per_Distance(self, radius, pollution_min, pollution_max):
        pollution_range = pollution_max - pollution_min
        decreasing_per_distance = pollution_range / radius
        return decreasing_per_distance
