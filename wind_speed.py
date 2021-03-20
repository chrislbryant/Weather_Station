from gpiozero import Button
import time
import math
import statistics

wind_count = 0 # Counts how many half-rotations
radius_cm = 9 # Radius of anemometor 
wind_interval = 5 # How often to report speed
CM_IN_A_KM = 100000.0
SECS_IN_AN_HOURS = 3600
ADJUSTMENT = 1.18
CONVERT_KM_TO_MPH = 1.609344

store_speeds = []

# Every half-rotation, add 1 to count
def spin():
    """ Every half-rotation, add 1 to count """
    global wind_count
    wind_count = wind_count + 1
    #print("spin" + str(wind_count))

def calculate_speed(time_sec):
    """ Calculate wind speed """
    global wind_count
    circumference_cm = (2 * math.pi) * radius_cm
    rotations = wind_count / 2.0

    # Calculate distance travelled by a cup in cm
    dist_km = circumference_cm * rotations / CM_IN_A_KM

    km_per_sec  = dist_km / time_sec
    km_per_hour = km_per_sec * SECS_IN_AN_HOURS

    return (km_per_hour * ADJUSTMENT) / CONVERT_KM_TO_MPH

def reset_wind():
    global wind_count
    wind_count = 0

wind_speed_sensor = Button(5) 
wind_speed_sensor.when_activated = spin

# Loop to measure wind speed and report every 5 seconds
while True:
    start_time = time.time()
    while time.time() - start_time <= wind_interval:
        reset_wind()
        time.sleep(wind_interval)
        final_speed = calculate_speed(wind_interval)
        store_speeds.append(final_speed)
    wind_gust = max(store_speeds)
    wind_speed = statistics.mean(store_speeds)    
    print(f"Wind Speed: {(round(wind_speed))} mph | Wind Gust: {(round(wind_gust))} mph")

