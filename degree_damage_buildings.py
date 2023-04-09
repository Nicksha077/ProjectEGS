from math import log, log10, radians, cos, sin, asin, sqrt



def distance_km(latitude: float = 0, longitude: float = 0, latitude2: float = 0, longitude2: float = 0) -> float:
    """
    # For calculating the distance in Kilometres
    :param latitude:
    :param longitude:
    :param latitude2:
    :param longitude2:
    :return float:
    """
    # The math module contains the function name "radians" which is used for converting the degrees value into radians.
    longitude = radians(longitude)
    longitude2 = radians(longitude2)
    latitude = radians(latitude)
    latitude2 = radians(latitude2)
    # Using the "Haversine formula"
    D_longitude = longitude2 - longitude
    D_latitude = latitude2 - latitude
    P = sin(D_latitude / 2) ** 2 + cos(latitude) * cos(latitude2) * sin(D_longitude / 2) ** 2
    Q = 2 * asin(sqrt(P))
    # The radius of earth in kilometres.
    R_km = 6371
    # Then, we will calculate the result
    return Q * R_km
# -------------------------------------------------------------

def macroseismic_intensity(magnitude: float = None, depth: float = None, distance: float = None,
                           region: str = 'Камчатка'):
    """
    Расчет макросейсмической интенсивности с помощью уравнения макросейсмического поля ГОСТ 2017
    :param magnitude: магнитуда по поверхностным волнам,
    :param depth: глубина очага землетрясения,
    :param distance: расстояние от эпицентра до точки наблюдения, км
    :param region:
    :return:
    """
    coefficient_macroseismic_field_equation_GOST2017 = {'Камчатка': (1.5, 2.6, 2.5),
                                                        'Курильские острова': (1.5, 4.5, 4.5),
                                                        'Сахалин': (1.6, 4.3, 3.3)}
    a, b, c = coefficient_macroseismic_field_equation_GOST2017[region]
    intensity = a * magnitude - b * log10(depth**2 + distance**2)**0.5 + c

    return intensity
# -------------------------------------------------------------

if __name__ == '__main__':
	
	# параметры землетрясения пока задаем произвольно
	event_depth = 110
	event_latitude = 52.5
	event_longitude = 158.5
	event_magnitude = 6
	# параметры здания загружаем из базы
	buildign_latitude = latitude  # широта
	building_longitude = longitude  # долгота
	building_resistance = seismic_resistance_soft  # Класс сейсмостойкости сооружений
	building_zone_SMZ = ((zone_SMZ_min + zone_SMZ_min) / 2) - 9  # поправка на грунт
	# --- расчет гипоцентрального расстояния
	distance = distance_km(event_latitude, event_longitude, buildign_latitude, building_longitude)
	# --- расчет интенсивности по ГОСТ
	intensity = macroseismic_intensity(event_magnitude, event_depth, distance)
	# --- расчет интенсивности с учетом карты микросейсморайонирования
	intensity = intensity + building_zone_SMZ
	# --- расчет Степени повреждений зданий (надо смотреть ГОСТ и реализовать в коде)
	# D = function(intensity, building_resistance)
	# D = 1 – слабые повреждения здания, можно не заморачиваться с ремонтом
	# D = 2 – слабые повреждения здания, требуется косметический ремонт
	# D = 3 – серьезные повреждения здания, аварийное состояние
	# D = 4 – здание очень сильно повреждено (под снос) – полная потеря кадастровой стоимости
	# D = 5 – здания больше нет – полная потеря кадастровой стоимости
	
