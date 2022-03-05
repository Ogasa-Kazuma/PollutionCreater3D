
#PollutionCreaterをSphericalPollutionCreaterに変更
#このファイルをmain.pyにする
#########################################################################
##         モジュール・ライブラリ
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


import Pollution
importlib.reload(Pollution)
from Pollution import Pollution

###########################################################################


######################################################################


###################################################################


def CreateGraphObject():
    """グラフの設定をしたいときはこの関数の中に書き足してください"""
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

    #濃度分布作成者オブジェクトを生成
    pollutionCreater = Pollution_Creater.PollutionCreater()

    #フィールドサイズの設定（プログラムは0から数字を数えるので, この場合、フィールドのx座標は0メートルから49メートル、となる
    #大きくしすぎるとメモリリークが発生してフリーズするので注意
    x_end = 50
    y_end = 50
    z_end = 20


    #シミュレーション用のフィールドを作成
    #Pythonの「リスト内包表記」により三次元リストを作成
    pollutionDatas = [[[0 for z in range(z_end)] for y in range(y_end)] for x in range(x_end)]

    #Pollutionオブジェクトを生成
    #この時点では全体の濃度値がゼロの空の濃度分布モデルを作成しているだけです（あとでこの空のモデルに球形汚染源を足していきます）
    pollutionField = Pollution(pollutionDatas)

    #球形汚染源を作成。中心点の座標と直径、中心部の濃度値を指定
    sphericalPollution1 = pollutionCreater.SphericalPollution(point_center = Point(x = 10, y = 10, z = 10), diameter = 10, pollution_at_center_point  = 100)
    sphericalPollution2 = pollutionCreater.SphericalPollution(point_center = Point(x = 0, y = 0, z = 0), diameter = 15, pollution_at_center_point  = 100)

    #フィールド上に球形汚染源を配置（空のモデルに球形汚染源を足していく）
    pollutionField.Add(sphericalPollution1)
    pollutionField.Add(sphericalPollution2)

    #濃度値の値を調整
    pollutionField = pollutionField.AdjustValueRange(pollution_max = 100)


    #うまく濃度分布モデルがつくられてない、と思っても表示の問題だったりするので
    #表示パラメータを調整してみてください
    graph_object = CreateGraphObject() #この関数で、x軸のラベルなどグラフ設定をしています　
    #表示する濃度の下限値と透明度を指定
    pollutionField.View(graph_object, pollution_lower_limit = 10, alpha = 0.3) #alphaは透明度

    #csvファイルよりpklファイルの方が保存時の実行速度が早くなる
    #多くの汚染源を作成するときは大きな時間の差が出る
    pollutionField.Save("PollutionLog/pData.pkl")

    #一点の濃度値を取得する
    print(pollutionField.GetPollution(x = 0, y = 0, z = 0))
    print(pollutionField.GetPollution(x = 10, y = 10, z = 10))



if __name__ == "__main__":
    main()
##########################################################################
