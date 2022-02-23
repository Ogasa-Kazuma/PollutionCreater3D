#########################################################################
import os, sys
sys.path.append(os.pardir)
import importlib


import Pollution_Creater
import matplotlib.pyplot as plt

importlib.reload(Pollution_Creater)

import PointClass
importlib.reload(PointClass)
from PointClass import Point


#ここらでなんかエラー　読み込み順？
import Pollution
importlib.reload(Pollution)
from Pollution import Pollution

import Searching_Data
importlib.reload(Searching_Data)

###########################################################################


######################################################################
def AddSphericalPollutionsToField(pollutionCreater, pollutionField):

    for i in range(5):
        addPollution = pollutionCreater.SphericalPollution(point_center = Point(0, 10, 5),\
                                        diameter     =              10 + i * 10,\
                                        pollution_at_center_point = 100\
                                        )
        pollutionField.Add(addPollution)

    return None
###################################################################


def PrintStraightLinePoint(points_straight_line):
##### Pollutionクラス内に表示メソッドがない場合、こうなる!
    for point_i in range(len(points_straight_line)):

        points = list()

        x = points_straight_line[point_i].GetX()
        y = points_straight_line[point_i].GetY()
        z = points_straight_line[point_i].GetZ()

        points.append([x, y, z])
        print(points)


####################### main ##########################################
def main():


    pollutionCreater = Pollution_Creater.PollutionCreater()
    x_end = 50
    y_end = 50
    z_end = 20

    #シミュレーション用のフィールドを作成
    #Pythonの「リスト内包表記」により三次元リストを作成
    pollutionField = Pollution([[[0 for z in range(z_end)] for y in range(y_end)] for x in range(x_end)])

    #フィールド上に球形汚染源を配置
    #なんでこれはクラスメソッドにしない方がいい気がするんだろう
    AddSphericalPollutionsToField(pollutionCreater, pollutionField)

    #濃度値の下限はゼロ
    #副作用太郎
    pollutionField = pollutionField.AdjustValueRange(pollution_max = 100)

    #一点の濃度値を取得する
    print(pollutionField.GetPollution(x = 0, y = 0, z = 0))
    print(pollutionField.GetPollution(x = 10, y = 10, z = 10))


    straight_line = pollutionField.StraightLine(Point(0, 0, 0), Point(5, 5, 5))
    #超便利
    straight_line.Print()


    searching_data = Searching_Data.SearchingData("unko")
    #直線上を探索
    for x_i, y_i, z_i, p_i in straight_line.Next():
        print('x' + str(x_i))
        print('y' + str(y_i))
        print('z' + str(z_i))
        print('pollution' + str(p_i))
        searching_data.Add(x_i, y_i, z_i)


    searching_data.Save("Search_Log/unko.csv", 'csv')



    #プログラムがきれいすぎて怖い





    #うまく濃度分布がつくられてない、と思っても表示の問題だったりするので
    #表示パラメータを調整してみてください
    pollutionField.View(display_pollution_range = 10)

    #csvファイルよりpklファイルの方が保存時の実行速度が早くなる
    #多くの汚染源を作成するときは大きな時間の差が出る
    pollutionField.Save("PollutionLog/unko.csv", format = 'csv')






if __name__ == "__main__":
    main()
##########################################################################
