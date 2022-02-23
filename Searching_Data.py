
import pandas as pd

class SearchingData:

    def __init__(self, pollutionFilePath):
        self.__pollutionFilePath = pollutionFilePath
        self.__Datas = [list(), list(), list()]


    def Add(self, x, y, z):
        self.__Datas[0].append(x)
        self.__Datas[1].append(y)
        self.__Datas[2].append(z)




    def MovingAmount(self):
        pass

    def Save(self, savePath, format):
        #濃度ファイル名とか

        indexNames = ['x', 'y', 'z']
        x, y, z = self.__Datas[0], self.__Datas[1], self.__Datas[2]
        values = [x, y, z]

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
