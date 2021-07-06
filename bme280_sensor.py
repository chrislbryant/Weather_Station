import board
import busio
import adafruit_bme280

i2c = busio.I2C(board.SCL, board.SDA)
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)
bme280.sea_level_pressure = 1013.25

def read_all():
    return bme280.humidity, bme280.pressure, (bme280.temperature * 1.8 + 32)
