from picamera import PiCamera
import datetime
import board
import digitalio
import busio
import time
import adafruit_bme280
import psycopg2

#----------------#
# DB credentials #
#----------------#
HOST = "db-postgresql-nyc1-33094-do-user-7855815-0.a.db.ondigitalocean.com"
DB   = "defaultdb"
USER = "doadmin"
PSWD = "tfgidwqkcduxaf5z"
PORT = "25060"

#------------------------------------
# Get connected and create a 'cursor'
#------------------------------------
try:
  connection = psycopg2.connect(host=HOST,database=DB,user=USER,password=PSWD,port=PORT)
except (Exception, psycopg2.Error) as error :
  print ("Error while connecting to PostgreSQL", error)
  exit()
cursor = connection.cursor()
print("Connected to PosgreSQL")

def insert_row(temperature, humidity, pressure, altitude ):
    insert_row = (
        altitude,
        humidity,
        pressure,
        altitude
        )
    sql_stmt = """
        INSERT INTO weather
        (
            temperature,
            humidity,
            pressure,
            altitude          
        ) 
        VALUES
        (
            %s,
            %s,
            %s,
            %s
        ); """
    try:
        cursor.execute(sql_stmt, insert_row)
    except (Exception, psycopg2.Error) as error :
        print ("DB Error: Insert into messenger_polygon", error)
        print(sql_stmt)
        exit()
    connection.commit()

#--------#
# Camera #
#--------#
camera       = PiCamera()
now          = datetime.datetime.now().replace(microsecond=0)
#camera.capture(f"/home/pi/Desktop/pics/test{now}.jpg") #takes the hourly picture

#-----------------------------------------------#
# Temperature, Humidity, Altitude, and Pressure #
#-----------------------------------------------#
i2c                       = busio.I2C(board.SCL, board.SDA)
bme280                    = adafruit_bme280.Adafruit_BME280_I2C(i2c)
bme280.sea_level_pressure = 1013.25
temperature               = (bme280.temperature * 1.8 + 32)
humidity                  = bme280.relative_humidity
pressure                  = bme280.pressure
altitude                  = bme280.altitude


while True:
    print("\nTemperature: %0.1f F" % (bme280.temperature * 1.8 + 32))
    print("Humidity: %0.1f %%" % bme280.relative_humidity)
    print("Pressure: %0.1f hPa" % bme280.pressure)
    print("Altitude %0.2f meters" % bme280.altitude)
    time.sleep(5)