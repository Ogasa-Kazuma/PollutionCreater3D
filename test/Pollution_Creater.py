#読み込み順のエラー
#表示下限濃度値の変数名
#PollutionCreaterをSphericalPollutionCreaterに変更
#このファイルをmain.pyにする
#Data_Saver消す
#########################################################################

####################################################################
#読み込み順を変更しないでください

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


def CreateGraphObject():
    #matplotlibという描画ライブラリを使用
    #matplotlibについて詳しくはWebで
    fig = plt.figure()
    graph_object = fig.add_subplot(111, projection = '3d') #111, は描画サイズの設定.
    #軸名の設定
    graph_object.set_xlabel('x [m]')
    graph_object.set_ylabel('y [m]')
    graph_object.set_zlabel('z [m]')
    return graph_object



####################### main ##########################################
def main():


    pollutionCreater = Pollution_Creater.PollutionCreater()
    #フィールドサイズの設定（プログラムは0から数字を数えるので, この場合、フィールドのx座標は0 - 49メートル、となる
    x_end = 50
    y_end = 50
    z_end = 20

    #シミュレーション用のフィールドを作成
    #Pythonの「リスト内包表記」により三次元リストを作成
    pollutionField = Pollution([[[0 for z in range(z_end)] for y in range(y_end)] for x in range(x_end)])

    #フィールド上に球形汚染源を配置
    AddSphericalPollutionsToField(pollutionCreater, pollutionField)

    #濃度値の値を調整
    #濃度値の下限はゼロ
    pollutionField = pollutionField.AdjustValueRange(pollution_max = 100)

    #一点の濃度値を取得する
    print(pollutionField.GetPollution(x = 0, y = 0, z = 0))
    print(pollutionField.GetPollution(x = 10, y = 10, z = 10))


    #うまく濃度分布がつくられてない、と思っても表示の問題だったりするので
    #表示パラメータを調整してみてください
    graph_object = CreateGraphObject()
    pollutionField.View(graph_object, pollution_lower_limit = 10, alpha = 0.1) #alphaは透明度

    #csvファイルよりpklファイルの方が保存時の実行速度が早くなる
    #多くの汚染源を作成するときは大きな時間の差が出る
    pollutionField.Save("PollutionLog/unko2.pkl")


if __name__ == "__main__":
    main()
##########################################################################
