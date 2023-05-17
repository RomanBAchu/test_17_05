# import psycopg2
#
# conn = psycopg2.connect(dbname="postgres", user="postgres", password="123123", host="127.0.0.1")
# cursor = conn.cursor()
#
# conn.autocommit = True
# # команда для создания базы данных metanit
# psql = "CREATE DATABASE Zalupa"
#
# # выполняем код sql
# cursor.execute(psql)
# print("База данных успешно создана")
#
# cursor.close()
# conn.close()
