import psycopg2
import os

#----------------------------#
# Set connection credentials #
#----------------------------#
HOST = os.environ.get("HOST")
DB   = os.environ.get("DB")
USER = os.environ.get("USER")
PSWD = os.environ.get("PSWD")
PORT = os.environ.get("PORT")

#-------------------------------------#
# Get connected and create a 'cursor' #
#-------------------------------------#
try:
  connection = psycopg2.connect(host=HOST,database=DB,user=USER,password=PSWD,port=PORT)
except (Exception, psycopg2.Error) as error :
  print ("Error while connecting to PostgreSQL", error)
  exit()
cursor = connection.cursor()
print("Connected to PosgreSQL")
print()

#----------------------------#
# Drop weather_station table #
#----------------------------#
sql_stmt = """
  DROP TABLE IF EXISTS weather_station;
  """
try:
  cursor.execute(sql_stmt)
except (Exception, psycopg2.Error) as error :
  print ("DB Error: Drop weather_station table", error)
  exit()
print('weather_station table dropped')
connection.commit()

#------------------------#
# Create weather_station #
#------------------------#
sql_stmt = """
  CREATE TABLE weather_station
  (
    wind_average       decimal,
    wind_speed         decimal,
    wind_gust          decimal,
    rainfall           decimal,
    humidity           decimal,
    pressure           decimal,
	  ambient_temp       decimal,
    ground_temp        decimal,
    timestamp          timestamp default current_timestamp 
    
  ); """
try:
  cursor.execute(sql_stmt)
except (Exception, psycopg2.Error) as error :
  print ("DB Error: Create weather_station table", error)
  print(sql_stmt)
  exit()
connection.commit()
print('weather_station table created')

#-----------------------------#
# Close cursor and connection #
#-----------------------------#
cursor.close()
connection.close()
print()
print("PostgreSQL connection is closed")