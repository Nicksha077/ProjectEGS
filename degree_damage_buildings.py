from math import log, log10, radians, cos, sin, asin, sqrt
from sqlalchemyDB import request_to_DB
import openpyxl



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
                           region: str = ''):
    """
    Расчет макросейсмической интенсивности с помощью уравнения макросейсмического поля ГОСТ 2017
    :param magnitude: магнитуда по поверхностным волнам,
    :param depth: глубина очага землетрясения,
    :param distance: расстояние от эпицентра до точки наблюдения, км
    :param region:
    :return:
    """
    coefficient_macroseismic_field_equation_GOST2017 = {'Камчатка': (1.5, 2.6, 2.5),
                                                        '': (1.5, 3.5, 3.0),
                                                        'Курильские острова': (1.5, 4.5, 4.5),
                                                        'Сахалин': (1.6, 4.3, 3.3)}
    a, b, c = coefficient_macroseismic_field_equation_GOST2017[region]
    intensity = a * magnitude - b * log10(depth**2 + distance**2)**0.5 + c

    return intensity
# -------------------------------------------------------------

def degree_of_damage(intensity: float = None, resistance: float = None):
    """
    D = 1 – слабые повреждения здания, можно не заморачиваться с ремонтом
    D = 2 – слабые повреждения здания, требуется косметический ремонт
    D = 3 – серьезные повреждения здания, аварийное состояние
    D = 4 – здание очень сильно повреждено (под снос) – полная потеря кадастровой стоимости
    D = 5 – здания больше нет – полная потеря кадастровой стоимости
    """
    print(f"intensity = {intensity}, resistance = {resistance}")
    if intensity < 0 or resistance > 9:
        return None
    if intensity > 10 or resistance <  6:
        return 5 
    match resistance:
        case 9:

            if intensity < 6:
                return max(0.2*intensity-1, 0)
            else:
                return 0.6*(intensity-6)+0.2
            
        case 8:

            if intensity < 6:
                return max(0.6*intensity-3, 0)
            elif intensity <= 8:
                return 0.6*(intensity-6)+0.6
            else:
                return 0.6*(intensity-6)+0.4
            
        case 7:

            return max((intensity-5), 0)
        
        case 7.5:

            if intensity <= 6:
                return max(1.5*intensity-7.5, 0)
            if intensity <= 7:
                return 1.2*(intensity-6)+1.5
            elif intensity <= 8:
                return 1.3*(intensity-6)+1.4
            else:
                return 0.5*(intensity-6)+3
            
        case 6:
            if intensity <= 6:
                return max(2*intensity-10, 0)
            if intensity <= 7:
                return 1.4*(intensity-6)+2
            elif intensity <= 8:
                return 1.6*(intensity-6)+1.8
            else:
                return 5.0

def count_damage():
    sum_cadastral = 0
    cadastral_damage = 0

def main():
    #params_from_sql = Connect_to_DB()
    #print(params_from_sql)
    # параметры землетрясения пока задаем произвольно
    book = openpyxl.open('Самые_ощутимые_землетрясения_в_ПК.xlsx', read_only=False)
    sheet = book.active
    for k in range(18):
        event_depth = float(sheet["E"+str(k+7)].value)
        event_latitude = float(sheet["C"+str(k+7)].value)
        event_longitude = float(sheet["D"+str(k+7)].value)
        event_magnitude = float(sheet["G"+str(k+7)].value)
        building_list = request_to_DB()
        sum_cadastral = 0
        cadastral_damage = 0
        sum_int = 0
        damage_counter = {
            'not_damaged': 0,
            'need_repair': 0,
            'emergency': 0,
            'ruined': 0
        }
        cnt = 0
        for i in building_list:
            # параметры здания загружаем из базы
            buildign_latitude = i[3]# широта
            building_longitude = i[4]  # долгота
            building_resistance = i[5]  # Класс сейсмостойкости сооружений
            building_zone_SMZ = float(((i[6] + i[7]) / 2) - 9) # поправка на грунт
            year_constr = i[9]
            if year_constr != None:
                if year_constr > int(sheet["A"+str(k+7)].value[:4]):
                    continue
            print(f'Дом: {i[1]} {i[2]}')
            # --- расчет гипоцентрального расстояния
            distance = distance_km(event_latitude, event_longitude, buildign_latitude, building_longitude)
            # --- расчет интенсивности по ГОСТ
            intensity = round(macroseismic_intensity(event_magnitude, event_depth, distance))
            # --- расчет интенсивности с учетом карты микросейсморайонирования
            intensity = float(sheet["J"+str(k+7)].value)
            sum_int += intensity
            cnt += 1
            intensity = intensity + building_zone_SMZ
            
            # --- расчет Степени повреждений зданий (надо смотреть ГОСТ и реализовать в коде)
            D = round(degree_of_damage(intensity, building_resistance))
            sum_cadastral += i[8]
            match D:
                case 0:
                    s = 'повреждений нет '
                    damage_counter['not_damaged'] += 1
                case 1:
                    s = 'слабые повреждения здания, можно не заморачиваться с ремонтом'
                    damage_counter['not_damaged'] += 1
                case 2:
                    s = 'слабые повреждения здания, требуется косметический ремонт'
                    damage_counter['need_repair'] += 1
                case 3:
                    s = 'серьезные повреждения здания, аварийное состояние'
                    cadastral_damage += i[8]
                    damage_counter['emergency'] += 1
                case 4:
                    s = 'здание очень сильно повреждено (под снос) – полная потеря кадастровой стоимости'
                    cadastral_damage += i[8]
                    damage_counter['ruined'] += 1
                case 5:
                    s = 'здания больше нет – полная потеря кадастровой стоимости'
                    cadastral_damage += i[8]
                    damage_counter['ruined'] += 1
            
            # D = 1 – слабые повреждения здания, можно не заморачиваться с ремонтом
            # D = 2 – слабые повреждения здания, требуется косметический ремонт
            # D = 3 – серьезные повреждения здания, аварийное состояние
            # D = 4 – здание очень сильно повреждено (под снос) – полная потеря кадастровой стоимости
            # D = 5 – здания больше нет – полная потеря кадастровой стоимости
            print(s)
            
        
        # sheet["Q"+str(k+7)].value = damage_counter["not_damaged"]
        # sheet["R"+str(k+7)].value = damage_counter['need_repair']
        # sheet["S"+str(k+7)].value = damage_counter['emergency']
        # sheet["T"+str(k+7)].value = damage_counter['ruined']
        # sheet["U"+str(k+7)].value = round(cadastral_damage  / 1000000, 2)#qrstu lmnop
        # sheet["K"+str(k+7)].value = sum_int / cnt
        
        sheet["L"+str(k+7)].value = damage_counter["not_damaged"]
        sheet["M"+str(k+7)].value = damage_counter['need_repair']
        sheet["N"+str(k+7)].value = damage_counter['emergency']
        sheet["O"+str(k+7)].value = damage_counter['ruined']
        sheet["P"+str(k+7)].value = round(cadastral_damage  / 1000000, 2)

        book.save("Самые_ощутимые_землетрясения_в_ПК.xlsx")
        print(f'''Сумма кадастровой стоимости исследуемых зданий = {'{0:,}'.format(sum_cadastral).replace(',', ' ')} руб.\n 
        {damage_counter["not_damaged"]} зданий уцелело;\n
        {damage_counter["need_repair"]} зданий требуют ремонта;\n
        {damage_counter["emergency"]} зданий стали аварийными;\n
        {damage_counter["ruined"]} разрушено\n
    Ущерб от землетрясения составил {'{0:,}'.format(round(cadastral_damage  / 1000000, 2)).replace(',', ' ')} млн.руб.\n''')



if __name__ == '__main__':
    main()
    
    