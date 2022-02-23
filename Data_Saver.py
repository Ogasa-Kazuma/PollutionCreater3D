
import pandas as pd
import datetime
import os
import numpy as np

class DataSaver:

    def __init__(self):
        pass

    def Save(self, indexNames, values, fileNameAndPath):
        """データの保存を行う関数"""

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

        self.__ToFile(datas, fileNameAndPath)


    def __ToFile(self, datas, fileNameAndPath):
        datas.to_pickle(str(fileNameAndPath))
