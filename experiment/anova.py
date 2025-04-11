import pandas as pd
import scipy.stats
import statsmodels.api as sm
from statsmodels.formula.api import ols

class Anova():
    def __init__(self, csv_file:str, encoding:str, alpha:float):
        self.__csv = pd.read_csv(csv_file, encoding=encoding, sep=";")
        self.__alpha = alpha

        self.__sample = self.__csv.sample(n=50)

        # Ищем связь между стоимостью
        self.__price = self.__sample["Price"].astype(int)
        # И площадью, этажом
        self.__meters = self.__sample["Meters"].str.split("/").str[0].astype(float)
        self.__floor = self.__sample["Floor"].str.split("/").str[0].astype(int)

    
    def calculate_one_way(self) -> list:
        result = scipy.stats.f_oneway(self.__price, self.__meters)
        print(result)
    

    def calculate_two_way(self) -> list:
        # Упорядочиваем данные, чтобы избежать большого разнообразия (без этого модель не построить, нужно больше условностей)
        cut_meters = pd.cut(self.__meters, bins=[12, 35, 100, 501], labels=["small", "medium", "large"])
        cut_floor = pd.cut(self.__floor, bins=[0, 3, 9, 26], labels=["low", "medium", "high"])

        # Иногда пишет кучу ошибок из-за низкого ранга матрицы, это нормально, так как может случиться так, что
        # попадаются неуникальные значения и число комбинаций падает, если так произошло, то просто перезапустить прогон
        df = pd.DataFrame({"meters": cut_meters, "floor": cut_floor, "price": self.__price})
        model = ols("price ~ C(meters) + C(floor) + C(meters):C(floor)", data=df).fit()
        print(sm.stats.anova_lm(model, typ=2).iloc[:, [0, 2, 3]].values)

