import openpyxl
import psycopg2

street_list = []
appointment_list = []
roof_list = []
facade_list = []
wall_list = []
floor_list = []
project_list = []
foundation_list = []
const_list = []


def fill_tables(sheet, j, l, table_name, colomn_name):
    req = ''
    for i in range(3, sheet.max_row): # filling streets
        if sheet[i][j].value not in l and sheet[i][j].value is not None:
            l.append(sheet[i][j].value)
            req +=f'''INSERT INTO {table_name}({colomn_name})
            VALUES('{sheet[i][j].value}');\n'''
    return req

def fill_main_table(sheet,cursor):
    req = ''
    for i in range(3, sheet.max_row):
        ins = 'INSERT INTO BUILDINGS('
        val = 'VALUES('
        if sheet[i][1].value is not None and sheet[i][1].value != '':
            ins += 'street, '
            val +=  f'{street_list.index(sheet[i][1].value)}, '
        if sheet[i][2].value is not None and sheet[i][2].value != '':
            ins += 'house, '
            val +=  f'\'{sheet[i][2].value}\', '
        if sheet[i][3].value is not None and sheet[i][3].value != '':
            ins += 'building, '
            val +=  f'\'{sheet[i][3].value}\', '
        if sheet[i][4].value is not None and sheet[i][4].value != '':
            ins += 'latitude, '
            val +=  f'{sheet[i][4].value}'.replace(',', '.') + ', '
        if sheet[i][5].value is not None and sheet[i][5].value != '':
            ins += 'longitude, '
            val +=  f'{sheet[i][5].value}'.replace(',', '.') + ', '
        if sheet[i][6].value is not None and sheet[i][6].value != '':
            ins += 'year_construction, '
            val +=  f'{sheet[i][6].value}, '
        if sheet[i][7].value is not None and sheet[i][7].value != '':
            ins += 'number_floors, '
            val +=  f'{sheet[i][7].value}, '
        if sheet[i][8].value is not None and sheet[i][8].value != '':
            ins += 'number_entrances, '
            val +=  f'{sheet[i][8].value}, '
        if sheet[i][9].value is not None and sheet[i][9].value != '':
            ins += 'number_buildings, '
            val +=  f'{sheet[i][9].value}, '
        if sheet[i][10].value is not None and sheet[i][10].value != '':
            ins += 'number_living_quarters, '
            val +=  f'{sheet[i][10].value}, '
        if sheet[i][11].value is not None and sheet[i][11].value != '':
            ins += 'type_construction, '
            val +=  f'{const_list.index(sheet[i][11].value)}, '
        if sheet[i][12].value is not None and sheet[i][12].value != '':
            ins += 'basic_project, '
            val +=  f'{project_list.index(sheet[i][12].value)}, '
       
        if sheet[i][13].value is not None and sheet[i][13].value != '':
            ins += 'appointment, '
            val +=  f'{appointment_list.index(sheet[i][13].value)}, ' 

        if sheet[i][14].value is not None and sheet[i][14].value != '':
            ins += 'seismic_resistance_min, '
            val +=  f'{sheet[i][14].value}'.replace(',', '.') + ', ' 
        if sheet[i][15].value is not None and sheet[i][15].value != '':
            ins += 'seismic_resistance_max, '
            val +=  f'{sheet[i][15].value}'.replace(',', '.') + ', '
        if sheet[i][16].value is not None and sheet[i][16].value != '':
            ins += 'seismic_resistance_soft, '
            val +=  f'{sheet[i][16].value}'.replace(',', '.') + ', '  
        if sheet[i][17].value is not None and sheet[i][17].value != '':
            ins += 'zone_SMZ_min, '
            val +=  f'{sheet[i][17].value}'.replace(',', '.') + ', '
        if sheet[i][18].value is not None and sheet[i][18].value != '':
            ins += 'zone_SMZ_max, '
            val +=  f'{sheet[i][18].value}'.replace(',', '.') + ', '
        if sheet[i][19].value is not None and sheet[i][19].value != '':
            ins += 'zone_SMZ_increment, '
            val +=  f'{sheet[i][19].value}'.replace(',', '.') + ', '
        if sheet[i][20].value is not None and sheet[i][20].value != '':
            ins += 'wear_rate, '
            val +=  f'{sheet[i][20].value}'.replace(',', '.') + ', '        
        # if sheet[i][21].value is not None and sheet[i][21].value != '':
        #     ins += 'priming, '
        #     val +=  f'{priming_list.index(sheet[i][21].value)}, '
        if sheet[i][22].value is not None and sheet[i][22].value != '':
            ins += 'load_bearing_walls, '
            val +=  f'{wall_list.index(sheet[i][22].value)}, ' 
        if sheet[i][23].value is not None and sheet[i][23].value != '':
            ins += 'basement_area, '
            val +=  f'{sheet[i][23].value}'.replace(',', '.') + ', ' 
        if sheet[i][24].value is not None and sheet[i][24].value != '':
            ins += 'building_roof, '
            val +=  f'{roof_list.index(sheet[i][24].value)}, '
        if sheet[i][25].value is not None and sheet[i][25].value != '':
            ins += 'building_floor, '
            val +=  f'{floor_list.index(sheet[i][25].value)}, '
        if sheet[i][26].value is not None and sheet[i][26].value != '':
            ins += 'facade, '
            val +=  f'{facade_list.index(sheet[i][26].value)}, '
        if sheet[i][27].value is not None and sheet[i][27].value != '':
            ins += 'foundation, '
            val +=  f'{foundation_list.index(sheet[i][27].value)}, '     
        if sheet[i][28].value is not None and sheet[i][28].value != '':
            ins += 'azimuth, '
            val +=  f'{sheet[i][28].value}'.replace(',', '.') + ', '
        if sheet[i][29].value is not None and sheet[i][29].value != '':
            ins += 'cadastral_number, '
            val +=  f'\'{sheet[i][29].value}\', '
        if sheet[i][30].value is not None and sheet[i][30].value != '':
            ins += 'year_overhaul, '
            val +=  f'{sheet[i][30].value}, '
        if sheet[i][31].value is not None and sheet[i][31].value != '':
            ins += 'accident_rate, '
            val +=  f'\'{sheet[i][31].value}\', '
            
        if sheet[i][32].value is not None and sheet[i][32].value != '':
            ins += 'land_area, '
            val +=  f'{sheet[i][32].value}'.replace(',', '.') + ', '

        cursor.execute(ins[:-2] + ') ' + val[:-2] + '); \n')
        print(i, ins[:-2] + ') ' + val[:-2] + '); \n')







def fill_sql_tables(cursor):
    
    req = ''
    book = openpyxl.open('data.xlsx', read_only=True) # [row(first index - 1)][column(first index - 0)]
    sheet = book.active # first page (None in empty cell)

    req += fill_tables(sheet, 1, street_list, 'STREETS', 'name')
    req += fill_tables(sheet, 13, appointment_list, 'APPOINTMENTS', 'appointment')
    req += fill_tables(sheet, 24, roof_list, 'ROOFS', 'roof_type')
    req += fill_tables(sheet, 26, facade_list, 'FACADES', 'facade_type')
    req += fill_tables(sheet, 22, wall_list, 'WALLS', 'wall_type')
    req += fill_tables(sheet, 25, floor_list, 'BUILDING_FOORS', 'floor_type')
    req += fill_tables(sheet, 12, project_list, 'BASIC_PROJECT', 'project_code')
    req += fill_tables(sheet, 27, foundation_list, 'FOUNDATION', 'fundation_type')
    req += fill_tables(sheet, 11, const_list, 'CONSTRUCTIONS', 'const_type')

    cursor.execute(req)       
    fill_main_table(sheet, cursor)








req  = """
    DROP TABLE IF EXISTS BUILDINGS, CONSTRUCTIONS, STREETS, APPOINTMENTS, ROOFS, FACADES, WALLS, BUILDING_FOORS, BASIC_PROJECT, FOUNDATION;
    CREATE TABLE STREETS (
        id serial PRIMARY KEY,
        name varchar(100) NOT NULL
    );
    CREATE TABLE APPOINTMENTS(
        id serial PRIMARY KEY,
        appointment varchar(100) NOT NULL 
    );
    CREATE TABLE ROOFS(
        id serial PRIMARY KEY,
        roof_type varchar(100) NOT NULL
    );
    CREATE TABLE FACADES(
        id serial PRIMARY KEY,
        facade_type varchar(100) NOT NULL
    );
    CREATE TABLE WALLS(
        id serial PRIMARY KEY,
        wall_type varchar(100) NOT NULL
    );
    CREATE TABLE BUILDING_FOORS(
        id serial PRIMARY KEY,
        floor_type varchar(100) NOT NULL
    );
    CREATE TABLE BASIC_PROJECT(
        id serial PRIMARY KEY,
        project_code varchar(100) NOT NULL
    );
    CREATE TABLE FOUNDATION(
        id serial PRIMARY KEY,
        fundation_type varchar(100) NOT NULL
    );
    CREATE TABLE CONSTRUCTIONS(
        id serial PRIMARY KEY,
        const_type varchar(100) NOT NULL
    );
    CREATE TABLE BUILDINGS(
        id serial PRIMARY KEY,
        street smallint,
        house varchar(30),
        building varchar(30),
        latitude NUMERIC(9, 6),
        longitude NUMERIC(9, 6),
        year_construction smallint,
        number_floors smallint,
        number_entrances smallint,
        number_buildings smallint,
        number_living_quarters smallint,
        type_construction smallint,
        basic_project smallint,
        appointment smallint,
        seismic_resistance_min NUMERIC(3, 1),
        seismic_resistance_max NUMERIC(3, 1),
        seismic_resistance_soft NUMERIC(3, 1),
        zone_SMZ_min NUMERIC(3, 1),
        zone_SMZ_max NUMERIC(3, 1),
        zone_SMZ_increment NUMERIC(3, 1),
        wear_rate NUMERIC(3, 1),
        priming smallint,
        load_bearing_walls smallint,
        basement_area smallint,
        building_roof smallint,
        building_floor smallint,
        facade smallint,
        foundation smallint,
        azimuth NUMERIC(4, 2),
        cadastral_number varchar(100),
        year_overhaul smallint,
        accident_rate varchar(3),
        land_area NUMERIC(6, 2)
    );
"""
filling = """
        INSERT INTO STREETS(name)
        VALUES('Абеля');

        INSERT INTO APPOINTMENTS(appointment)
        VALUES('многоквартирный дом');

        INSERT INTO ROOFS(roof_type)
        VALUES('плоская');

        INSERT INTO FACADES(facade_type)
        VALUES('облицованный камнем');

        INSERT INTO WALLS(wall_type)
        VALUES('панельные');

        INSERT INTO BUILDING_FOORS(floor_type)
        VALUES('железобетонные');

        INSERT INTO BASIC_PROJECT(project_code)
        VALUES('1-464-АС');

        INSERT INTO FOUNDATION(fundament_type)
        VALUES('ленточный');

        INSERT INTO CONSTRUCTIONS(const_type)
        VALUES('панельный');

        INSERT INTO BUILDINGS(street, house, latitude, longitude,
        year_construction, number_floors, number_living_quarters,
        type_construction, basic_project, appointment, seismic_resistance_min, seismic_resistance_max,
        seismic_resistance_soft, zone_SMZ_min, zone_SMZ_max, zone_SMZ_increment,
        year_overhaul, accident_rate)
        VALUES(1, 4, 53.068921, 158.600465, 1969, 5, 90, 1, 1, 1, 7,  8, 7.5, 10.0, 10.0, 1.0, 2022, 'нет');

"""