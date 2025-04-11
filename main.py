from experiment import Correlation, Anova, Regression

def run_correlations() -> None:
    # Лабораторка 1
    # В приложенном файле realty.csv содержатся данные о продаваемых квартирах.
    # Необходимо рассчитать корреляцию по Пирсону, по Кендаллу и по Спирмену и визуально
    # показать корреляцию по Пирсону между стоимостью квартиры и ее метражом (первая цифра в соответствующем столбце), 
    # между стоимостью и этажом (первая цифра в соответствующем столбце), 
    # между стоимостью и количеством комнат. 
    # Аналогичные расчеты выполнить для всех квартир из одного района. 
    # Сравнить полученные результаты для района и для всего города.

    correlation = Correlation(csv_file, encoding, alpha)

    # Рассчет корреляций и пояснение полученных результатов для города
    correlations_city = correlation.calculate_city_corellations()
    correlation.explain_city_corellations(correlations_city)

    # Отрисовать графики корреляций по Пирсону для города
    correlation.draw_city_correlations()

    # Рассчет корреляций и пояснение полученных результатов для районов
    correlations_districts = correlation.calculate_district_corellations()
    correlation.explain_district_correlation(correlations_districts)


def run_anova() -> None:
    # Лабораторка 2    
    # Составить выборку из нескольких квартир (40-50), выделить факторы для
    # анализа и провести однофакторный и двухфакторный дисперсионный анализ
    # их влияния на стоимость квартиры.
    anova = Anova(csv_file, encoding, alpha)
    anova.calculate_one_way()
    anova.calculate_two_way()


def run_regression_model() -> None:
    # Лабораторка 3
    # Для выбранного района города построить регрессионные модели
    # зависимости стоимости квартиры от ее площади. Выбрать тип модели на
    # основе визуального представления. Результат сравнить с теоретической моделью.
    regression = Regression()


if __name__ == "__main__":
    csv_file = "data/realty.csv"
    encoding = "cp1251"
    alpha = 0.05

    #run_correlations()
    #run_anova()
    run_regression_model()
