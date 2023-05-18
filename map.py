from  degree_damage_buildings import distance_km, macroseismic_intensity, degree_of_damage
import folium
from sqlalchemyDB import request_to_DB


if __name__ == '__main__':

    mapObj = folium.Map(zoom_start=15, 
                        location=[53.0666582,158.5960724])

    
    event_depth = 105 #float(input())
    event_latitude = 52.580 #float(input())
    event_longitude = 158.784 #float(input())
    event_magnitude = 6.5 #float(input())
    building_list = request_to_DB()
    folium.Marker(location=[event_latitude, event_longitude],
                  tooltip=f"{event_latitude}, {event_longitude}",
                  popup=folium.Popup(f'Магнитуда: {event_magnitude}<br>Глубина: {event_depth}', max_width=400)
                  ).add_to(mapObj)
    for i in building_list:
            # параметры здания загружаем из базы
            buildign_latitude = i[3]# широта
            building_longitude = i[4]  # долгота
            building_resistance = i[5]  # Класс сейсмостойкости сооружений
            building_zone_SMZ = float(((i[6] + i[7]) / 2) - 9) # поправка на грунт
            year_constr = i[9]
            print(f'Дом: {i[1]} {i[2]}')
            # --- расчет гипоцентрального расстояния
            distance = distance_km(event_latitude, event_longitude, buildign_latitude, building_longitude)
            # --- расчет интенсивности по ГОСТ
            intensity = round(macroseismic_intensity(event_magnitude, event_depth, distance))
            # --- расчет интенсивности с учетом карты микросейсморайонирования
            intensity = intensity + building_zone_SMZ
            
            # --- расчет Степени повреждений зданий (надо смотреть ГОСТ и реализовать в коде)
            D = round(degree_of_damage(intensity, building_resistance))
            match D:
                case 0:
                    s = 'Отсутствие видимых повреждений'
                    color = 'lightgray'
                case 1:
                    s = 'Видимые повреждения конструктивных элементов отсутствуют.\n Работоспособное техническое состояние по ГОСТ 31937'
                    color = 'green'
                case 2:
                    s = 'Ограниченно работоспособное техническое состояние по ГОСТ 31937'
                    color = 'orange'
                case 3:
                    s = 'Аварийное состояние по ГОСТ 31937'
                    s += f'<br>Ущерб составил {round(i[8] / 1000000, 2)} млн.руб.'
                    color = 'red'
                case 4:
                    s = 'Здание под снос'
                    color = 'red'
                    s += f'<br>Ущерб составил {round(i[8] / 1000000, 2)} млн. руб.'
                case 5:
                    s = 'Разрушение'
                    color = 'black'
                    s += f'<br>Ущерб составил {round(i[8] / 1000000, 2)} млн. руб.'

            if i[10] == i[11]:
                s += f'<br>Сейсмостойкость здания: {int(i[10])}'
            else:
                s += f'<br>Сейсмостойкость здания: {int(i[10])}-{int(i[11])}'

            
            if i[6] == i[7]:
                s += f'<br>Зона по карте СМР: {int(i[6])}'
            else:
                s += f'<br>Зона по карте СМР: {int(i[6])}-{int(i[7])}'
            s += f'<br>Интенсивность: {intensity}'
            # D = 1 – слабые повреждения здания, можно не заморачиваться с ремонтом
            # D = 2 – слабые повреждения здания, требуется косметический ремонт
            # D = 3 – серьезные повреждения здания, аварийное состояние
            # D = 4 – здание очень сильно повреждено (под снос) – полная потеря кадастровой стоимости
            # D = 5 – здания больше нет – полная потеря кадастровой стоимости
            print(s)
            folium.Marker(location=[buildign_latitude, building_longitude], 
                          tooltip=f"{i[1]}, д. {i[2]}", 
                          popup=folium.Popup(s, max_width=400),
                          icon=folium.Icon(icon='home', color=color)).add_to(mapObj)
            mapObj.save('output.html')
    