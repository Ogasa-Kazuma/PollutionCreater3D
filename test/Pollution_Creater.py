
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
    for i in range(2):
        point_center = Point(x = 100, y = 100, z = 10)
        sphericalPollution = pollutionCreater.SphericalPollution(point_center, diameter = 10, pollution_at_center_point = 100)
        pollutionField.Add(sphericalPollution)

    return pollutionField

def main():

    pollutionCreater = Pollution_Creater.PollutionCreater()
    x_end = 300
    y_end = 300
    z_end = 20

    #シミュレーション用のフィールドを作成
    pollutionField = Pollution([[[1 for z in range(z_end)] for y in range(y_end)] for x in range(x_end)])
    #フィールド上に球形汚染源を配置
    #sphericalPollutions = LocateSphericalPollutions(pollutionCreater, pollutionField)
    #pollutionField.Add(sphericalPollutions)

    #濃度値の下限はゼロ
    pollutionField = pollutionField.AdjustValueRange(pollution_max = 100)
    print(pollutionField.GetPollution(0, 0, 0))
    print(pollutionField.GetPollution(10, 10, 10))
    print(pollutionField.GetPollution(20, 20, 20))

    #pollutionField.View()
    #csvファイルよりpklファイルの方が保存時の実行速度が早くなる
    #多くの汚染源を作成するときは大きな時間の差が出る
    #pollutionField.Save("unko.csv", format = 'csv')




if __name__ == "__main__":
    main()
