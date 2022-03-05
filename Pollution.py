
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import copy
from itertools import chain
import math
import os.path


class Pollution:
    """濃度分布モデルの保存、描画、値調整を行うクラス"""

    #コンストラクタ
    def __init__(self, pollutionPoints):
    #濃度分布の3次元リストをコンストラクタに渡す
        self.__pollutionPoints = pollutionPoints


#---------------------- パブリックメソッド ---------------------------
#
#　パブリックメソッドはクラス外からアクセスできる
#
#------------------------------------------------------------------

    def GetPollution(self, x, y, z):
        """指定した座標での濃度値を読み取る"""
        return self.__pollutionPoints[x][y][z]


    def IsInRange(self, x, y, z):
        """指定した座標が濃度分布モデルの上限と下限の範囲内にあるかどうかを判断する"""
        xlim, ylim, zlim = self.__XYZ_Limits()
        isInRange = (x >= 0 and x < xlim and y >= 0 and y < ylim and z >= 0 and z < zlim)
        return isInRange



    def Add(self, pollution):
        """濃度分布モデルどうしを足し合わせる"""
        xlim, ylim, zlim = self.__XYZ_Limits()
        for x_i in range(xlim):
            for y_i in range(ylim):
                for z_i in range(zlim):
                    #一点ずつ濃度計算を行う
                    self.__AddOnePointPollution(x_i, y_i, z_i, pollution)


    def AdjustValueRange(self, pollution_max):
        """濃度値の範囲を調整する"""

        #計算のため、濃度データを一次元に変換
        before_max = max(chain(*(chain(*self.__pollutionPoints))))

        #現時点での最大濃度値と、設定したい濃度最大値の比を計算
        ratio = before_max / pollution_max

        #一応コピーして、もともとのデータに影響がでないようにしておく
        result = copy.deepcopy(self.__pollutionPoints)

        xlim, ylim, zlim = self.__XYZ_Limits()

        for x_i in range(xlim):
            for y_i in range(ylim):
                for z_i in range(zlim):
                    #濃度の最大値が、指定した設定どおりになるように一点ずつ（1つの座標ずつ)濃度を再計算する
                    result[x_i][y_i][z_i] = self.__pollutionPoints[x_i][y_i][z_i] / ratio

        return Pollution(result)



    def View(self, graph_object, pollution_lower_limit, cmap = 'binary', alpha = 0.3, marker='o', norm=None, vmin=None, vmax=None, linewidths=None, verts=None, edgecolors=None, hold=None, data=None):
        """濃度分布を描画する"""
        #描画にはmatplotlibライブラリのscatterメソッドを使っている。
        #scatterとは、散布図という意味である
        #デフォルトで透明度（alpha)を0.3, カラーマップを白黒のbinaryに設定している

        #3Dの濃度分布モデルでは、表示する濃度値に下限を設定できるようにしている。濃度値が10未満なら表示しない、など
        xList, yList, zList, pollutionList = self.__DeletePollutionPointNotInViewRange(pollution_lower_limit)

        graph_object.scatter(xList, yList, zList, c = pollutionList, cmap = cmap, alpha = alpha, marker = marker, norm = norm,\
                              vmin = vmin, vmax = vmax, linewidths = linewidths,\
                              edgecolors = edgecolors, data = data)

        return graph_object





    def Save(self, savePath):
        """データの保存を行う関数"""

        #保存を行えるように濃度や座標データの構造を変換
        x, y, z, pollution = self.__to_list()

        #ここは絶対に変更しないでくたさい-------------------
        indexNames = ['x', 'y', 'z', 'pollution']
        values = [x, y, z, pollution]
        #--------------------------------------------

        #保存にはPandasライブラリのデータフレーム型を使っています（詳しくはWebで)
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

        #保存先は文字列型で指定する必要があるのでパスを文字列型に変換
        savePath = str(savePath)
        #保存ファイル名から拡張子を取得
        not_used, ext = os.path.splitext(savePath)

        #拡張子によって保存方法を判断する
        if(ext == '.pkl'):
            datas.to_pickle(savePath)

        elif(ext == '.csv'):
            datas.to_csv(savePath)

        else:
            raise TypeError('pkl形式かcsv形式の保存にのみ対応しています')




#---------------------  プライベートメソッド ---------------------------------
#
# プライベートメソッドはクラス外からはアクセスできない
#
#--------------------------------------------------------------------------

    def __to_list(self):
        """データの保存を行いやすいように、データの構造を変換する"""
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
        if(pollution.IsInRange(x, y, z)):
            self.__pollutionPoints[x][y][z] += pollution.GetPollution(x, y, z)


    def __XYZ_Limits(self):
        """各座標の長さを取得する"""
        #多次元のデータにおいて、各次元の長さを求めることでx, y, z座標の上限値を判定する
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
