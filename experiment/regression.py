import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

class Regression():
    def __init__(self, csv_file:str, encoding:str):
        self.__csv = pd.read_csv(csv_file, encoding=encoding, sep=";")

        # Ищем зависимость стоимости от площади
        self.__price = self.__csv["Price"].astype(int)
        self.__meters = self.__csv["Meters"].str.split("/").str[0].astype(float)

        # берем семплы сразу, чтобы во всех расчетах были одинаковые данные
        self.__price_sample = self.__price.sample(300)
        self.__meters_sample = self.__meters.sample(300)


    def calculate_simple_regression(self) -> dict:
        result = {}
        # Берем семплы для случайных выборок
        x = self.__price_sample.to_numpy().reshape((-1,1))
        y = self.__meters_sample.to_numpy()

        model = LinearRegression().fit(x, y)

        x_new = self.__price_sample.to_numpy().reshape((-1,1))
        y_pred = model.predict(x_new)

        # Собираем результаты в словарь
        result['method'] = 'simple'
        result['r_sq'] = model.score(x, y)
        result['intercept'] = model.intercept_
        result['slope'] = model.coef_
        result['data'] = x_new
        result['predict'] = y_pred

        return result

    
    def calculate_multiplie_regression(self) -> dict:
        result = {}

        # для графика возьмем нормальный x
        x = self.__price_sample.to_numpy().reshape((-1,2))
        # Так как мы поделили x/2, то y тоже нужно взять выборку в 2 раза меньше
        y = self.__meters_sample[:150].to_numpy()

        model = LinearRegression().fit(x, y)

        x_once = self.__price_sample.to_numpy()
        x_new = x_once.reshape((-1,2))
        
        y_pred = model.predict(x_new)

        result['method'] = 'multiplie'
        result['r_sq'] = model.score(x, y)
        result['intercept'] = model.intercept_
        result['slope'] = model.coef_
        result['data'] = x_once[:150]
        result['predict'] = y_pred

        return result

    
    def calculate_polynomail_regression(self) -> dict:
        result = {}

        x = self.__price_sample.to_numpy().reshape((-1,1))
        y = self.__meters_sample.to_numpy()

        transformer = PolynomialFeatures(degree=2, include_bias=False)
        x_ = transformer.fit_transform(x)

        model = LinearRegression().fit(x_, y)

        x_new = self.__price_sample.to_numpy().reshape((-1,1))
        x__new = transformer.fit_transform(x_new)
        y_pred = model.predict(x__new)

        result['method'] = 'polynomail'
        result['r_sq'] = model.score(x_, y)
        result['intercept'] = model.intercept_
        result['slope'] = model.coef_
        result['data'] = x_new
        result['predict'] = y_pred

        return result
    

    def explain_regressions(self, simple:dict, multiplie:dict, polynomail:dict):
        science_data = []

        for dict in [simple, multiplie, polynomail]:
            print(f"{dict['method']} r_sq simple: {dict['r_sq']}")
            print(f"{dict['method']} intercept simple: {dict['intercept']}")
            print(f"{dict['method']} slope simple: {dict['slope']}")
            print()
            # ну и пихнем словарь, почему бы и нет?
            science_data.append(dict)

        fig, ax = plt.subplots(1, 3)

        counter = 0
        for science in science_data:
            ax[counter].plot(science['data'], science["predict"], linewidth=0, marker='o', markersize=4, label='processed')
            ax[counter].plot(science['data'], science["intercept"] + science["slope"][0] * science['data'], label='theoretical')
            ax[counter].set_xlabel('x')
            ax[counter].set_ylabel('y')
            ax[counter].legend(facecolor='white')
            counter += 1

        plt.show()