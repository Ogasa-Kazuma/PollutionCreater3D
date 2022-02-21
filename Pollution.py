
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import copy
from itertools import chain

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


        pollutions_converted_to_array = np.array(self.__pollutionPoints)
        x_element_count, y_element_count, z_element_count = pollutions_converted_to_array.shape

        new_x = []
        new_y = []
        new_z = []
        new_pollutions = []
        for x_count in range(x_element_count):
            for y_count in range(y_element_count):
                for z_count in range(z_element_count):
                    if(self.__pollutionPoints[x_count][y_count][z_count] > 10):
                        new_x.append(x_count)
                        new_y.append(y_count)
                        new_z.append(z_count)
                        new_pollutions.append(self.__pollutionPoints[x_count][y_count][z_count])

        fig = plt.figure()
        ax = fig.add_subplot(111, projection = '3d')
        ax.scatter(xList, yList, zList, c = pollutionList, cmap = 'binary', alpha = 0.3)


        return None


    def Save(self, savePath, format):
        """データの保存を行う関数"""

        x, y, z, pollution = self.to_list()

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
