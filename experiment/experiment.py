import pandas as pd
import scipy.stats
import matplotlib.pyplot as plt

class Experiment():
    def __init__(self, csv_file:str, encoding:str, alpha:float):
        self.__csv = pd.read_csv(csv_file, encoding=encoding, sep=";")

        self.__alpha = alpha

        # Ищем корреляцию между стоимостью
        self.__price = self.__csv["Price"].astype(int)
        # Районом
        self.__districts = self.__csv["District"].astype(object)
        # И этим рядом параметров
        meters = self.__csv["Meters"].str.split("/").str[0].astype(float)
        floor = self.__csv["Floor"].str.split("/").str[0].astype(int)
        rooms = self.__csv["Rooms"].astype(int)

        self.__metrics = [meters, floor, rooms]


    def calculate_city_corellations(self) -> list:
        pearson = {"Name": "Пирсон"}
        kendall = {"Name": "Кендалл"}
        spearman = {"Name": "Спирмен"}

        for metric in self.__metrics:
            r, p = scipy.stats.pearsonr(self.__price, metric)
            pearson[metric.name] = [r, p]
            r, p = scipy.stats.kendalltau(self.__price, metric)
            kendall[metric.name] = [r, p]
            r, p = scipy.stats.spearmanr(self.__price, metric)
            spearman[metric.name] = [r, p]

        return pearson, kendall, spearman
    

    def explain_city_corellations(self, correlations:list) -> None:
        for correlation in correlations:
            for k, v in correlation.items():
                if k != "Name":
                    if v[1] > self.__alpha:
                        print(f"Корреляция {correlation.get('Name')} для {self.__price.name} от {k} равна {v[0]}, достоверность низкая {v[1]} > alpha")
                    else:
                        print(f"Корреляция {correlation.get('Name')} для {self.__price.name} от {k} равна {v[0]}, достоверность высокая {v[1]} < alpha")
        print()


    def draw_city_correlations(self) -> None:
        science_data = []
        for metric in self.__metrics:
            slope, intercept, r, *__ = scipy.stats.linregress(self.__price, metric)
            line = f'Regression line: y={intercept:.2f}+{slope:.2f}x, r={r:.2f}'
            result = {"Slope": slope, "Intercept": intercept, "Corr": r, "Line": line, "Metric": metric}
            science_data.append(result)
        
        fig, ax = plt.subplots(1, 3)

        counter = 0
        for science in science_data:
            ax[counter].plot(self.__price, science["Metric"], linewidth=0, marker='o', markersize=4, label='Data points')
            ax[counter].plot(self.__price, science["Intercept"] + science["Slope"] * self.__price, label=science["Line"])
            ax[counter].set_xlabel('x')
            ax[counter].set_ylabel('y')
            ax[counter].legend(facecolor='white')
            counter += 1

        plt.show()


    def calculate_district_corellations(self) -> list:
        csv_disticts = {}
        districts = list(self.__districts.unique())

        for district in districts:
            csv_disticts[district] = self.__csv[self.__csv["District"] == district]

        data_pearson = []
        data_kendall = []
        data_spearman = []

        pearson = {"Name": "Пирсон"}
        kendall = {"Name": "Кендалл"}
        spearman = {"Name": "Спирмен"}

        for district in districts:
            # Локально переопредляем метрики для районов
            price = csv_disticts[district]["Price"].astype(int)
            meters = csv_disticts[district]["Meters"].str.split("/").str[0].astype(float)
            floor = csv_disticts[district]["Floor"].str.split("/").str[0].astype(int)
            rooms = csv_disticts[district]["Rooms"].astype(int)
            
            metrics = [meters, floor, rooms]

            sub_pearson = {}
            sub_kendall = {}
            sub_spearman = {}
            for metric in metrics:
                r, p = scipy.stats.pearsonr(price, metric)
                sub_pearson[metric.name] = [r, p]
                r, p = scipy.stats.kendalltau(price, metric)
                sub_kendall[metric.name] = [r, p]
                r, p = scipy.stats.spearmanr(price, metric)
                sub_spearman[metric.name] = [r, p]

                data_pearson.append([district, metric.name, sub_pearson[metric.name]])
                data_kendall.append([district, metric.name, sub_kendall[metric.name]])
                data_spearman.append([district, metric.name, sub_spearman[metric.name]])

        pearson["District"] = data_pearson
        kendall["District"] = data_kendall
        spearman["District"] = data_spearman

        return pearson, kendall, spearman


    def explain_district_correlation(self, correlations_districts:list) -> None:
        for district in correlations_districts: 
            for k, v in district.items():
                print()
                if k != "Name":
                    for values in v:
                        print(f"Корреляция {district.get('Name')} для {self.__price.name} от {values[1]} по району {values[0]} = {values[2][0]}")