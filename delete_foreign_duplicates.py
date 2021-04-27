import psycopg2
import os

#----------------------------#
# Set connection credentials #
#----------------------------#
HOST="****"
DB="****"
USER="****"
PSWD="****"

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
print()

#-------------------#
# Delete Duplicates #
#-------------------#
sql_stmt = """
    DELETE FROM foreign_weather_station a
    USING foreign_weather_station b
    WHERE a.ctid < b.ctid
    AND a.timestamp = b.timestamp
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