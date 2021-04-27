import psycopg2
import os

#-------------------------------#
# Set connection db credentials #
#-------------------------------#
HOST="db-postgresql-nyc1-33094-do-user-7855815-0.a.db.ondigitalocean.com"
DB="defaultdb"
USER="doadmin"
PSWD="tfgidwqkcduxaf5z"
PORT="25060"

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

#-------------------#
# Delete Duplicates #
#-------------------#
sql_stmt = """
        SELECT 
            timestamp,
            COUNT(*) 
        FROM 
            foreign_weather_station
        GROUP BY
            timestamp
        ORDER BY 
            timestamp
  ; """

try:
  cursor.execute(sql_stmt)
except (Exception, psycopg2.Error) as error :
  print ("DB Error: Select * from weather_station", error)
  print(sql_stmt)
  exit()
try:
  all_rows = cursor.fetchall()
except (Exception, psycopg2.Error) as error :
  print ("DB Error: Fetch all rows - weather_station table", error)
  print(sql_stmt)
  exit()

#---------------------#
# Is the table empty? #
#---------------------#
if not all_rows:
  print()
  print("The weather_station table is empty")
  cursor.close()
  connection.close()
  print()
  print("PostgreSQL connection is closed")
  print()
  exit()

#------------------#
# Print result set #
#------------------#
print()
print('weather_station table result set')
for row in all_rows:
  print(row)
print()

#-----------------------------#
# Close cursor and connection #
#-----------------------------#
cursor.close()
connection.close()
print("PostgreSQL connection is closed")