# В приложенном файле realty.csv содержатся данные о продаваемых квартирах.
# Необходимо рассчитать корреляцию по Пирсону, по Кендаллу и по Спирмену и визуально
# показать корреляцию по Пирсону между стоимостью квартиры и ее метражом (первая цифра в соответствующем столбце), 
# между стоимостью и этажом (первая цифра в соответствующем столбце), 
# между стоимостью и количеством комнат. 
# Аналогичные расчеты выполнить для всех квартир из одного района. 
# Сравнить полученные результаты для района и для всего города.

from experiment import Experiment

if __name__ == "__main__":
    csv_file = "data/realty.csv"
    encoding = "cp1251"
    alpha = 0.05 # коэффициент для оценки степени корреляции

    experiment = Experiment(csv_file, encoding, alpha)

    # Рассчет корреляций и пояснение полученных результатов для города
    correlations_city = experiment.calculate_city_corellations()
    experiment.explain_city_corellations(correlations_city)

    # Отрисовать графики корреляций по Пирсону для города
    experiment.draw_city_correlations()

    # Рассчет корреляций и пояснение полученных результатов для районов
    correlations_districts = experiment.calculate_district_corellations()
    experiment.explain_district_correlation(correlations_districts)
    