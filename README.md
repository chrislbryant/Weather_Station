# Weather Pi

This was by far one of my favorite projects! I followed this great [tutorial](https://projects.raspberrypi.org/en/projects/build-your-own-weather-station) on Raspberry.org. 

After finishing the the initial tutorial, I added a camera, Google Drive file management system, local & cloud Postgres databases connected wtih a FDW, and some scripts to create a daily Time Lapse Video with Audio that is uploaded to Youtube.

## Weather Station
Data on Wind Speed, Wind Gust, Wind Direction, Rain, Ambient Temperature, Ground Temperature, Pressure, and Humidity are inserted into a local database every 5 minutes.

1 minute later the data is uploaded to [wunderground](https://www.wunderground.com/dashboard/pws/KNCLANDI10) and a cloud database. Every night the cloud database checks the local data base for missing entries, inserts any missing entries (sometimes the pi loses internet connectivity), and varifies there are no duplicate entries. The databases are connected using a FDW and the script is run via a cronjob that outputs a log file.

## Camera
A PiCam takes a picure every 5 minutes and uploads it to the appropriate folder on the Google Drive. The picture file name is the current timestamp. This script is run via a cron job that outputs a log file. The log files are checked by a seperate script once day for errors and an email is sent if issues uploading are are found.

## Google Drive File Management
The Google drive is managed with a service account. The folders are structured as follows:
* Weather Station
* Year (ie 2021)
* Month (ie April)
* Day (ie 2021-01-01)

The program will create folders as neccessary ie every day it creates a new day folder. This helps keep all the photos organized.

## Time Lapse Video
This script runs once a day on a cloud server and creates a time lapse video with audio. 

The script retrieves all the pictures from the previous day and completes the following process: 

* PyDub   - measures the length of a randomly selected song to set the framerate of the timelapse video
* OpenCV  - creates the timelapse video
* MoviePy - combines the timelapse video and audio

The final video is uploaded to the Google drive previous day folder and uploaded to Youtube. After this all files used to make the video are deleted off the cloud server.

## Weather Station Parts List

Rasberry Pi Weather Station

* Wind Speed/Gust Sensor
* Wind Direection Sensor
* Rain Guage Sensor
* Ambient Temperature, Pressure, and Humidity Sensor
* Ground Temperature Sensor

(1) [CanaKit Raspberry Pi 4](https://www.amazon.com/CanaKit-Raspberry-4GB-Starter-Kit/dp/B07V5JTMV9)

(1) Wind and Rain Sensors [Argent Data Systems](https://www.argentdata.com/catalog/product_info.php?products_id=145) 

(1) Ambient Temperature, Pressure, and Humidity Sensor [BME280](https://www.amazon.com/gp/product/B07P4CWGGK/ref=ppx_yo_dt_b_asin_title_o03_s00?ie=UTF8&psc=1)

(1) Ground Temperature Sensors [DS18B20](https://www.amazon.com/gp/product/B087JQ6MCP/ref=ppx_yo_dt_b_asin_title_o02_s00?ie=UTF8&psc=1)

(2) Board to connect Wind and Rain Sensors [CZH-LABS D-1039](https://www.amazon.com/gp/product/B01GNO4L6K/ref=ppx_yo_dt_b_asin_title_o00_s00?ie=UTF8&psc=1)

(1) ADC for Wind Direction [Adafruit MCP3008](https://www.amazon.com/gp/product/B00NAY3RB2/ref=ppx_yo_dt_b_asin_title_o00_s01?ie=UTF8&psc=1)

(1) 4.7k Ohm, 1/2 W, 5% [Resistors](https://www.amazon.com/gp/product/B0185FKBG4/ref=ppx_yo_dt_b_asin_title_o00_s02?ie=UTF8&psc=1) 

(1) Breadboard Kit [SunFounder Super Starter Learning Kit V3.0](https://www.amazon.com/gp/product/B06XZ833QW/ref=ppx_yo_dt_b_asin_title_o02_s00?ie=UTF8&psc=1)

Misc Boxes and Tubing from Lowes

## Camera Parts List
(1) [Raspberry Pi Camera Module V2](https://www.amazon.com/Raspberry-Pi-Camera-Module-Megapixel/dp/B01ER2SKFS)

(1) [Flex Cable for Raspberry Pi Camera or Display - 2 meters](https://www.adafruit.com/product/2144)

(1) [WeatherBox For Raspberry Pi Camera (v2)](https://www.innaturerobotics.com/product-page/weatherbox-for-raspberry-pi-camera-v2)

(1) [JMX 3.1 Inch Acrylic Dome](https://www.amazon.com/dp/B012OLS4Q4?psc=1&ref=ppx_yo2_dt_b_product_details)

## Weather Station Picutures

### Weather Station Components
![Testing Components](/images/Testing_Components.jpg)

### Print Out From Functional Weather Station
![Weather Station Print Out](/images/Weather_Station_Print.png)

### The Weather Station!
![Weather Station](/images/Weather_Station.jpg)

### Control Box
![Control Box](https://github.com/chrislbryant/Weather_Station/blob/main/images/Contol_Box.jpg)

### BME280 Temperature, Humidity, and Pressure Sensor
![BME280](/images/BME280.jpg)



