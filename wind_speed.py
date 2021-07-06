from gpiozero import Button
import time
import math
import statistics

wind_count        = 0 
radius_cm         = 9 
wind_interval     = 5 
cm_in_a_km        = 100000.0 # Centimeters in a kilometer
seconds_in_hours  = 3600
adjusment         = 1.18 # Adjustment for the loss of wind energy due when arms spin
convert_km_to_mph = 1.609344
store_speeds      = []

# Every half-rotation, add 1 to count
def spin():
    """ Every half-rotation, add 1 to count """
    global wind_count
    wind_count = wind_count + 1

def calculate_speed(time_sec):
    """ Calculate wind speed """
    global wind_count
    circumference_cm = (2 * math.pi) * radius_cm
    rotations = wind_count / 2.0

    # Calculate distance travelled by a cup in cm
    dist_km = circumference_cm * rotations / cm_in_a_km

    km_per_sec  = dist_km / time_sec
    km_per_hour = km_per_sec * seconds_in_hours

    return (km_per_hour * adjusment) / convert_km_to_mph

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

