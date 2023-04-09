import psycopg2
import openpyxl
from  time import time
from config import host, user, password, db_name
from sql_resp import req, filling, fill_sql_tables

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

    cursor.execute(req)
    fill_sql_tables(cursor)
   

    print('Готово, брат!!')
    print(time() - t)



except Exception as _ex:
    print("SQL Error: ", _ex)
finally:
    if connection:
        cursor.close()
        connection.close()
        print("connection closed")