import psycopg2
import requests

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
print()

#-----------------------------------------------------------#
# Create variables from DB to upload to weather underground #
#-----------------------------------------------------------#
sql_stmt = """
    SELECT *
    FROM local_weather_station
    ORDER BY timestamp DESC
    LIMIT 1
    ; """
try:
    cursor.execute(sql_stmt)
except (Exception, psycopg2.Error) as error :
    print ("DB Error: Select * from local_weather_station", error)
    print(sql_stmt)
    exit()
try:
    row = cursor.fetchall()
except (Exception, psycopg2.Error) as error :
    print ("DB Error: Fetch all rows - local_weather_station table", error)
    print(sql_stmt)
    exit()

wind_average = float(row[0][0])
wind_speed   = float(row[0][1])
wind_gust    = float(row[0][2])
rainfall     = float(row[0][3])
humidity     = float(row[0][4])
pressure     = float(row[0][5])  
ambient_temp = float(row[0][6])
ground_temp  = float(row[0][7])

#--------------------------------#
# Send Local DB data to Cloud DB #
#--------------------------------#
sql_stmt = """
    INSERT INTO foreign_weather_station 
    (
      wind_average,
      wind_speed,
      wind_gust,
      rainfall,
      humidity,
      pressure,
      ambient_temp,
      ground_temp,
      timestamp
    )
    SELECT 
      wind_average,
      wind_speed,
      wind_gust,
      rainfall,
      humidity,
      pressure,
      ambient_temp,
      ground_temp,
      timestamp
    FROM local_weather_station
    ORDER BY timestamp DESC
    LIMIT 1
    ; """
try:
    cursor.execute(sql_stmt)
    connection.commit()
except (Exception, psycopg2.Error) as error :
    print ("DB Error: Select * from local_weather_station", error)
    print(sql_stmt)
    exit()
connection.close()

def hpa_to_inches(pressure_in_hpa):
    """ Converts pressure to inches """
    pressure_in_inches_of_m = pressure_in_hpa * 0.02953
    return pressure_in_inches_of_m

def degc_to_degf(temperature_in_c):
    """ Converts Celsius to Fahrenheit """
    temperature_in_f = (temperature_in_c * (9/5.0)) + 32
    return temperature_in_f

def mm_to_inches(rainfall_in_mm):
    rainfall_in_inches = rainfall_in_mm * 0.0393701
    return rainfall_in_inches

def kmh_to_mph(speed_in_kmh):
    speed_in_mph = speed_in_kmh * 0.621371
    return speed_in_mph

WUurl = "https://weatherstation.wunderground.com/weatherstation/updateweatherstation.php?"
WU_station_id = "KNCLANDI10"
WU_station_pwd = "6mfOi8LE"
WUcreds = "ID=" + WU_station_id + "&PASSWORD=" + WU_station_pwd
date_str = "&dateutc=now"
action_str = "&action=updateraw"

wind_average_str = str(wind_average)
wind_speed_mph_str = "{0:.2f}".format(kmh_to_mph(wind_speed))
wind_gust_mph_str = "{0:.2f}".format(kmh_to_mph(wind_gust))
rainfall_in_str = "{0:.2f}".format(mm_to_inches(rainfall))
humidity_str = "{0:.2f}".format(humidity)
pressure_str = "{0:.2f}".format(hpa_to_inches(pressure))
ambient_temp_str = "{0:.2f}".format(degc_to_degf(ambient_temp))
ground_temp_str = "{0:.2f}".format(degc_to_degf(ground_temp))

#print(wind_average_str, wind_speed_mph_str, wind_gust_mph_str, rainfall_in_str, humidity_str, pressure_str, ambient_temp_str, ground_temp_str)

try:
    r = requests.get(
                    WUurl +
                    WUcreds +
                    date_str +
                    "&humidity=" + humidity_str +
                    "&baromin=" + pressure_str +
                    "&windspeedmph=" + wind_speed_mph_str +
                    "&windgustmph=" + wind_gust_mph_str +
                    "&tempf=" + ambient_temp_str +
                    "&rainin=" + rainfall_in_str +
                    "&soiltempf=" + ground_temp_str +
                    "&winddir=" + wind_average_str +
                    action_str
                    )

except Exception as e:
    print(f"Error Message: {e}")   

print("data_uploaded")
