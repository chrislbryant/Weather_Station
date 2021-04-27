import psycopg2
import os

#----------------------------#
# Set connection credentials #
#----------------------------#
HOST="localhost"
DB="pi"
USER="pi"
PSWD="0623Tiff"

#-------------------------------------#
# Get connected and create a 'cursor' #
#-------------------------------------#
try:
    connection = psycopg2.connect(host=HOST,database=DB,user=USER,password=PSWD)
except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)
    exit()
cursor = connection.cursor()
print("Connected to PosgreSQL")

#--------------------------------------------#
# Select all rows from weather_station table #
#--------------------------------------------#
sql_stmt = """
    INSERT INTO foreign_weather_station

    SELECT *
    FROM local_weather_station

    EXCEPT

    SELECT *
    FROM foreign_weather_station

  ; """
try:
    cursor.execute(sql_stmt)
except (Exception, psycopg2.Error) as error :
    print ("DB Error: Select * from weather_station", error)
    print(sql_stmt)
    exit()
connection.commit()

#-----------------------------#
# Close cursor and connection #
#-----------------------------#
cursor.close()
connection.close()
print("PostgreSQL connection is closed")