import requests

from postgres_interface import DatabaseInterface

db = DatabaseInterface()

def get_weather():
    query = """
            SELECT *
            FROM local_weather_station
            ORDER BY timestamp DESC
            LIMIT 1
        ; """
    result      = db.fetch_all(query)
    weather_row = [element for tuple in result for element in tuple]
    return weather_row

def insert_to_cloud_db():
    query = """
            INSERT INTO foreign_weather_station

            SELECT *
            FROM local_weather_station

            EXCEPT
            
            SELECT *
            FROM foreign_weather_station
        ; """
    db.execute(query)
    db.commit()

def hpa_to_inches(pressure_in_hpa):
    """ Converts Pressure to Inches """
    pressure_in_inches_of_m = float(pressure_in_hpa) * 0.02953
    return pressure_in_inches_of_m

def degc_to_degf(temperature_in_c):
    """ Converts Celsius to Fahrenheit """
    temperature_in_f = (float(temperature_in_c) * (9/5.0)) + 32
    return temperature_in_f

def mm_to_inches(rainfall_in_mm):
    """ Converts Millimeters to Inches """
    rainfall_in_inches = float(rainfall_in_mm) * 0.0393701
    return rainfall_in_inches

def kmh_to_mph(speed_in_kmh):
    """Converts Kilometers per hour to Miles per hour"""
    speed_in_mph = float(speed_in_kmh) * 0.621371
    return speed_in_mph

WUurl          = "https://weatherstation.wunderground.com/weatherstation/updateweatherstation.php?"
WU_station_id  = *****
WU_station_pwd = *****
WUcreds        = f"ID=" + WU_station_id + "&PASSWORD=" + WU_station_pwd
date           = "&dateutc=now"
action         = "&action=updateraw"
weather_row    = get_weather()
wind_average   = str(weather_row[0])
wind_speed     = "{0:.2f}".format(kmh_to_mph(weather_row[1]))
wind_gust      = "{0:.2f}".format(kmh_to_mph(weather_row[2]))
rainfall       = "{0:.2f}".format(mm_to_inches(weather_row[3]))
humidity       = "{0:.2f}".format(weather_row[4])
pressure       = "{0:.2f}".format(hpa_to_inches(weather_row[5]))
ambient_temp   = "{0:.2f}".format(degc_to_degf(weather_row[6]))
ground_temp    = "{0:.2f}".format(degc_to_degf(weather_row[7]))

def main():
    try:
        requests.get(
            WUurl +
            WUcreds +
            date +
            "&humidity=" + humidity +
            "&baromin=" + pressure +
            "&windspeedmph=" + wind_speed +
            "&windgustmph=" + wind_gust +
            "&tempf=" + ambient_temp +
            "&rainin=" + rainfall +
            "&soiltempf=" + ground_temp +
            "&winddir=" + wind_average +
            action
            )
    except Exception as e:
        print(f"Error Message: {e}")   
    
    insert_to_cloud_db()
    db.close()
    print("data_uploaded")
    #print(wind_average, wind_speed, wind_gust, rainfall, humidity, pressure, ambient_temp, ground_temp)

if __name__ == "__main__":
    main()