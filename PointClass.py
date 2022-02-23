import math

class Point:

    def __init__(self, x, y, z):
        self.__x = x
        self.__y = y
        self.__z = z


    def GetX(self):
        return self.__x


    def GetY(self):
        return self.__y


    def GetZ(self):
        return self.__z


    def distance(self, point):
        if(not type(point) == Point):
            raise TypeError("座標クラス以外とは距離を計算できません")

        start_x = self.GetX()
        last_x = point.GetX()
        start_y = self.GetY()
        last_y = point.GetY()
        start_z = self.GetZ()
        last_z = point.GetZ()

        distance = math.sqrt((last_x - start_x) ** (2) + (last_y - start_y) ** (2) + (last_z - start_z) ** (2))

        return distance


    def Degrees(self, point):
        if(not type(point) == Point):
            raise TypeError("座標クラス以外とは距離を計算できません")

        xBegin, yBegin, zBegin = self.GetX(), self.GetY(), self.GetZ()
        xEnd, yEnd, zEnd = point.GetX(), point.GetY(), point.GetZ()
        #2点間の角度計算
        xy_angle = math.atan2((yEnd - yBegin), (xEnd - xBegin))
        xy_distance = math.sqrt((xEnd - xBegin) ** (2) + (yEnd - yBegin) ** (2))
        z_angle = math.atan2((zEnd - zBegin), xy_distance)

        xy_angle = math.degrees(xy_angle)
        z_angle = math.degrees(z_angle)

        return xy_angle, z_angle


    def PolarPoint(self, distance, degree_xy, degree_z):
        x = self.GetX() + distance * math.cos(degree_xy)
        y = self.GetY() + distance * math.sin(degree_xy)
        z = self.GetZ() + distance * math.sin(degree_z)

        return Point(x, y, z)
