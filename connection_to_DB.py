import psycopg2
import openpyxl
import tabulate
from  time import time
from config import host, user, password, db_name
from creating_base import req, filling, fill_sql_tables


def selection(cursor):
    postgreSQL_select_Query = """select buildings.id, streets.name, buildings.house, buildings.latitude, buildings.longitude, 
                                 buildings.seismic_resistance_soft, buildings.zone_smz_min, buildings.zone_smz_min, buildings.cadastral_cost
                                 from buildings
                                 INNER JOIN streets
                                 on buildings.street = streets.id
                                 where buildings.cadastral_cost IS NOT NULL and buildings.seismic_resistance_soft IS NOT NULL
                                 """
    cursor.execute(postgreSQL_select_Query)
    records = cursor.fetchall()
    print(tabulate.tabulate(records))
    return records
    
def get_data():
    try:
        connection = psycopg2.connect(
            host = host,
            user = user,
            password = password,
            database = db_name
        )
        connection.autocommit = True
        cursor = connection.cursor()
        
        book = openpyxl.open('data.xlsx', read_only=True)
        sheet = book.active #None
        print('wait a moment')
        t = time()

        cursor.execute(req) #drop table
        fill_sql_tables(cursor)
        
        resp = selection(cursor=cursor)

        print('Готово, брат!!')
        print(time() - t)
        if connection:
            cursor.close()
            connection.close()
            print("connection closed")
        return resp

    except Exception as _ex:
        print("SQL Error: ", _ex)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("connection closed")
    

get_data()