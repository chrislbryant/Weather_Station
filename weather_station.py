import time
import math
import statistics
from gpiozero import Button
import psycopg2

import bme280_sensor
import wind_direction
import ds18b20_therm

#----------------------------#
# Set connection credentials #
#----------------------------#
HOST="****"
DB="****"
USER="***"
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

def insert_weather_row(wind_average, wind_speed, wind_gust, rainfall, humidity, pressure, ambient_temp, ground_temp):
    """ Inserts row into DB """
    insert_row = (
            wind_average,
            wind_speed,
            wind_gust,
            rainfall,
            humidity,
            pressure,
            ambient_temp,
            ground_temp
        )
    sql_stmt = """
        INSERT INTO local_weather_station
        (
            wind_average,
            wind_speed,
            wind_gust,
            rainfall,
            humidity,
            pressure,
            ambient_temp,
            ground_temp     
        ) 
        VALUES
        (
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s
        ); """
    try:
        cursor.execute(sql_stmt, insert_row)
    except (Exception, psycopg2.Error) as error :
        print ("DB Error: Insert into weather_Station", error)
        print(sql_stmt)
        exit()
    connection.commit()


#----------------------#
# Weather Station Code #
#----------------------#

wind_count        = 0 # Counts how many half-rotations
radius_cm         = 9 # Radius of anemometor 
wind_interval     = 5 # How often to report speed
interval          = 300 # How often weather station collects data
cm_in_a_km        = 100000.0 # Centimeters in a kilometer
seconds_in_hours  = 3600
adjusment         = 1.18 # Adjustment for the loss of wind energy due when arms spin
convert_km_to_mph = 1.609344
bucket_size       = 0.2794 # Amount of millimeters of rain needed to tip rain gauge
rain_count        = 0
gust              = 0
store_speeds      = []
store_directions  = []

def spin():
    """ Every half-rotation, add 1 to count """
    global wind_count
    wind_count = wind_count + 1

def calculate_speed(time_sec):
    """ Calculate wind speed """
    global wind_count
    global gust
    circumference_cm = (2 * math.pi) * radius_cm
    rotations = wind_count / 2.0

    # Calculate distance travelled by a cup in cm
    dist_km = circumference_cm * rotations / cm_in_a_km
    km_per_sec  = dist_km / time_sec
    km_per_hour = km_per_sec * seconds_in_hours

    # Calculate speed and convert from km to mph
    final_speed = (km_per_hour * adjusment) / convert_km_to_mph

    return final_speed

def bucket_tipped():
    """ Counts number of time rain gauge bucket is tipped """
    global rain_count
    rain_count = rain_count + 1


def reset_rainfall():
    global rain_count
    rain_count = 0

def reset_wind():
    global wind_count
    wind_count = 0

def reset_gust():
    global gust
    gust = 0

wind_speed_sensor = Button(5) 
wind_speed_sensor.when_activated = spin
temp_probe  = ds18b20_therm.DS18B20()
rain_sensor = Button(6)
rain_sensor.when_activated = bucket_tipped

while True:
    start_time = time.time()
    while time.time() - start_time <= interval:
        wind_start_time = time.time()
        reset_wind()
        while time.time() - wind_start_time <= wind_interval:
            store_directions.append(wind_direction.get_value())
        final_speed = calculate_speed(wind_interval)
        store_speeds.append(final_speed)

    wind_average     = wind_direction.get_average(store_directions)    
    wind_gust        = max(store_speeds)
    wind_speed       = statistics.mean(store_speeds)    
    rainfall         = rain_count * bucket_size
    reset_rainfall()
    store_speeds     = []
    store_directions = []
    ground_temp      = temp_probe.read_temp()
    humidity, pressure, ambient_temp = bme280_sensor.read_all()
    print(wind_average, wind_speed, wind_gust, rainfall, humidity, pressure, ambient_temp, ground_temp)
    insert_weather_row(wind_average, wind_speed, wind_gust, rainfall, humidity, pressure, ambient_temp, ground_temp)