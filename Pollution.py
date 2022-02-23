
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import copy
from itertools import chain
import math

class Pollution:

    def __init__(self, pollutionPoints):
        self.__pollutionPoints = np.array(pollutionPoints)


    def GetPollution(self, x, y, z):
        return self.__pollutionPoints[x][y][z]

    def IsInRange(self, x, y, z):
        xlim, ylim, zlim = self.__pollutionPoints.shape
        isInRange = (x >= 0 and x < xlim and y >= 0 and y < ylim and z >= 0 and z < zlim)
        return isInRange

    def Add(self, pollution):

        xlim, ylim, zlim = self.__pollutionPoints.shape
        for x_i in range(xlim):
            for y_i in range(ylim):
                for z_i in range(zlim):
                    if(pollution.IsInRange(x_i, y_i, z_i)):
                        self.__pollutionPoints[x_i][y_i][z_i] += pollution.GetPollution(x_i, y_i, z_i)


        return self


    def AdjustValueRange(self, pollution_max):
        #before_maxが0なら例外を投げる
        before_max = max(chain(*(chain(*self.__pollutionPoints))))

        ratio = before_max / pollution_max


        xlim, ylim, zlim = self.__pollutionPoints.shape
        result = copy.deepcopy(self.__pollutionPoints)

        for x_i in range(xlim):
            for y_i in range(ylim):
                for z_i in range(zlim):

                    result[x_i][y_i][z_i] = self.__pollutionPoints[x_i][y_i][z_i] / ratio

        return Pollution(result)



    def View(self, display_pollution_range, cmap = 'binaly'):



        xList, yList, zList, pollutionList = self.__DeletePollutionPointNotInViewRange(display_pollution_range)
        #matplotlibという描画ライブラリで散布図を描画
        ax = plt.figure().add_subplot(111, projection = '3d')
        ax.scatter(xList, yList, zList, c = pollutionList, cmap = 'binary', alpha = 0.3)

        return None


    def __XYZ_Limits(self):
        return self.__pollutionPoints.shape


    def __DeletePollutionPointNotInViewRange(self, view_range):
        xlim, ylim, zlim = self.__XYZ_Limits()

        new_x = []
        new_y = []
        new_z = []
        new_pollutions = []

        for x_count in range(xlim):
            for y_count in range(ylim):
                for z_count in range(zlim):
                    if(self.__pollutionPoints[x_count][y_count][z_count] > view_range):
                        new_x.append(x_count)
                        new_y.append(y_count)
                        new_z.append(z_count)
                        new_pollutions.append(self.__pollutionPoints[x_count][y_count][z_count])


        return new_x, new_y, new_z, new_pollutions




    def Save(self, savePath, format):
        """データの保存を行う関数"""

        x, y, z, pollution = self.__to_list()

        indexNames = ['x', 'y', 'z', 'pollution']
        values = [x, y, z, pollution]

        datas = pd.DataFrame(index=[], columns=[])
        #保存するインデックス名前と値を対応づける
        for i in range(len(indexNames)):
            datalog = pd.DataFrame(index=[], columns=[])
            #単一の値（非リスト）だと保存できない。そのため、単一の値である場合はリストに変換する
            if(type(values[i]) == list):
                datalog[indexNames[i]] = values[i]
            else: #非リストの場合
                datalog[indexNames[i]] = [values[i]]

            datas = pd.concat([datas, datalog], axis = 1)


        savePath = str(savePath)

        if(format == 'pkl'):
            datas.to_pickle(savePath)

        if(format == 'csv'):
            datas.to_csv(savePath)


    def __to_list(self):

        xlim, ylim, zlim = self.__XYZ_Limits()

        new_x = []
        new_y = []
        new_z = []
        new_pollutions = []

        for x_count in range(xlim):
            for y_count in range(ylim):
                for z_count in range(zlim):
                    new_x.append(x_count)
                    new_y.append(y_count)
                    new_z.append(z_count)
                    new_pollutions.append(self.__pollutionPoints[x_count][y_count][z_count])

        return new_x, new_y, new_z, new_pollutions

    def Print(self):
        print(self.__pollutionPoints)



    def StraightLine(self, point_start, point_last):

        #learn
        degree_xy, degree_z = point_start.Degrees(point_last)
        distance = point_start.distance(point_last)

        #どちらをPollutionの知識とするか, Pointクラスの知識とするか
        #Pointが有するのは二点間の距離の直線距離の求め方
        #Pollutionが有するのは、濃度値座標は離散値という知識
        #Pointから離散座標を返すようにすると密結合になる
        #Pointは角度計算の知識も持つ
        #pointクラスに角度計算も距離計算も任せることでだいぶクリアになる

        xyz_and_pollutions = list()

        for distance_i in range(0, math.floor(distance)):
            xyz_and_pollutions.append(self.__AppendXYZ_AndPollution(point_start, distance_i, degree_xy, degree_z))

        #終点も含める
        xyz_and_pollutions.append(self.__AppendXYZ_AndPollution(point_start, distance, degree_xy, degree_z))


        return self.PollutionStraightLine(xyz_and_pollutions)



    def __AppendXYZ_AndPollution(self, point_start, distance, degree_xy, degree_z):
        point_next = point_start.PolarPoint(distance, degree_xy, degree_z)
        x, y, z = point_next.GetXYZ()
        x, y, z = round(x), round(y), round(z)
        pollution = self.GetPollution(x, y, z)

        return [x, y, z, pollution]



        return self.PollutionStraightLine(straight)


    class PollutionStraightLine():

        def __init__(self, pointAndPollutions):
            self.__pointAndPollutions = pointAndPollutions
            self.__counter = 0

        def Print(self):
            print(self.__pointAndPollutions)


        def Next(self):
            #TODO　呼び出しのたびにカウンタを初期化しよう
            if(self.__counter > len(self.__pointAndPollutions)):
                self.__counter = 0
                return []

            self.__counter += 1
            return self.__pointAndPollutions
