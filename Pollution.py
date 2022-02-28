
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import copy
from itertools import chain
import math
import os.path


class Pollution:



    def __init__(self, pollutionPoints):
        self.__pollutionPoints = pollutionPoints


    def GetPollution(self, x, y, z):
        return self.__pollutionPoints[x][y][z]


    def Add(self, pollution):

        xlim, ylim, zlim = self.__XYZ_Limits()
        for x_i in range(xlim):
            for y_i in range(ylim):
                for z_i in range(zlim):
                    self.__AddOnePointPollution(x_i, y_i, z_i, pollution)


    def AdjustValueRange(self, pollution_max):
        #before_maxが0なら例外を投げる
        before_max = max(chain(*(chain(*self.__pollutionPoints))))

        ratio = before_max / pollution_max


        xlim, ylim, zlim = self.__XYZ_Limits()
        #deepコピーしないとエラーの原因
        result = copy.deepcopy(self.__pollutionPoints)

        for x_i in range(xlim):
            for y_i in range(ylim):
                for z_i in range(zlim):

                    result[x_i][y_i][z_i] = self.__pollutionPoints[x_i][y_i][z_i] / ratio

        return Pollution(result)



    def View(self, graph_object, display_pollution_range, cmap = 'binary', alpha = 0.3, marker='o', norm=None,
                          vmin=None, vmax=None, linewidths=None,
                          verts=None, edgecolors=None, hold=None, data=None):


        xList, yList, zList, pollutionList = self.__DeletePollutionPointNotInViewRange(display_pollution_range)
        #matplotlibという描画ライブラリで散布図を描画
        graph_object.scatter(xList, yList, zList, c = pollutionList, cmap = cmap, alpha = alpha)

        return graph_object





    def Save(self, savePath):
        """データの保存を行う関数"""

        x, y, z, pollution = self.__to_list()

        #ここは絶対に変更しないでくたさい-------------------
        indexNames = ['x', 'y', 'z', 'pollution']
        values = [x, y, z, pollution]
        #--------------------------------------------

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
        root, ext = os.path.splitext(savePath)


        if(ext == '.pkl'):
            datas.to_pickle(savePath)

        elif(ext == '.csv'):
            datas.to_csv(savePath)

        else:
            raise TypeError('pkl形式かcsv形式の保存にのみ対応しています')













######################  プライベートメソッド ##################################################333

    def __to_list(self):

        xlim, ylim, zlim = self.__XYZ_Limits()

        new_x = []
        new_y = []
        new_z = []
        new_pollutions = []

        for x_i in range(xlim):
            for y_i in range(ylim):
                for z_i in range(zlim):
                    new_x.append(x_i)
                    new_y.append(y_i)
                    new_z.append(z_i)
                    new_pollutions.append(self.GetPollution(x_i, y_i, z_i))

        return new_x, new_y, new_z, new_pollutions







    def __AddOnePointPollution(self, x, y, z, pollution):
        if(pollution.__IsInRange(x, y, z)):
            self.__pollutionPoints[x][y][z] += pollution.GetPollution(x, y, z)

    def __IsInRange(self, x, y, z):
        xlim, ylim, zlim = self.__XYZ_Limits()
        isInRange = (x >= 0 and x < xlim and y >= 0 and y < ylim and z >= 0 and z < zlim)
        return isInRange

    def __XYZ_Limits(self):
        xlim = len(self.__pollutionPoints)
        ylim = len(self.__pollutionPoints[0])
        zlim = len(self.__pollutionPoints[0][0])
        return xlim, ylim, zlim


    def __DeletePollutionPointNotInViewRange(self, view_range):
        xlim, ylim, zlim = self.__XYZ_Limits()

        new_x = []
        new_y = []
        new_z = []
        new_pollutions = []

        for x_i in range(xlim):
            for y_i in range(ylim):
                for z_i in range(zlim):
                    if(self.__pollutionPoints[x_i][y_i][z_i] > view_range):
                        new_x.append(x_i)
                        new_y.append(y_i)
                        new_z.append(z_i)
                        new_pollutions.append(self.__pollutionPoints[x_i][y_i][z_i])


        return new_x, new_y, new_z, new_pollutions
