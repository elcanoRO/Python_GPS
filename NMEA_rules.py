#RPI.GPIO interrupts: 			http://raspi.tv/2013/how-to-use-interrupts-with-python-on-the-raspberry-pi-and-rpi-gpio-part-3
#PY Serial: 				http://pyserial.sourceforge.net/shortintro.html, pentru citirea ttyS0
#GrooveOLED python library: 		https://github.com/DexterInd/GrovePi/blob/master/Software/Python/grove_oled.py SAU https://github.com/dda/MicroPython/blob/master/Grove_OLED.py
#Remove login from RPI: 		http://elinux.org/RPi_Debian_Auto_Login
#Physical shutdown button for RPI: 	http://www.instructables.com/id/Physical-Shutdown-Button-For-Raspberry-Pi/
#Launch Python script on startup:	http://www.instructables.com/id/Raspberry-Pi-Launch-Python-script-on-startup/?ALLSTEPS
#Change font for SSD1327D I2C ctrl:	https://code.google.com/p/u8glib/
#U8Glib with RPI:			http://hallard.me/driving-oled-lcd/
#Gauggete(doar ptr SSD1306):		http://guy.carpenter.id.au/gaugette/2012/11/11/font-support-for-ssd1306/
#Python impl fot T6963C:		https://github.com/Orabig/Rasp-T6963C

import pynmea2
from geographiclib.geodesic import Geodesic#import geographiclib
# open file
with open("C:\\Users\\lucian_crisan\\Downloads\\GeoSphere\\SparkFun\\NMEA_example.txt", "r") as ins:
    array = []
    for line in ins:
        array.append(line)
# indeparteaza \n de la final de linie(optional)
_.rstrip('\n')
# poate sa parsese cu sau fara \n la final
msg = pynmea2.parse(array[2])
# verificare daca este mesaj de tip GPGGA
array[2][:6]== "$GPGGA"
# crearea unei array de obiecte dictionar de tip lat/lon
array2= []
array2.append({'lat':123, 'lon':231})

import pynmea2
from geographiclib.geodesic import Geodesic#import geographiclib
with open("C:\\Users\\lucian_crisan\\Downloads\\GeoSphere\\SparkFun\\NMEA_example.txt", "r") as ins:
    array = []
    for line in ins:
        if  line[:6]== "$GPGGA":
            array.append(line)
arrayDictLatLon= []
for elem in array:
         msg = pynmea2.parse(elem)
         arrayDictLatLon.append({'lat':msg.latitude, 'lon':msg.longitude})
Geodesic.WGS84.Area(arrayDictLatLon)
# sau, folosing un average pe 10 puncte
arrayDictLatLon, latAvg, lonAvg, index= [], 0.0, 0.0, 0
for elem in array:
         msg = pynmea2.parse(elem)
         index+= 1
         if(index>= 10):
             arrayDictLatLon.append({'lat':latAvg/10.0, 'lon':lonAvg/10.0})
             index, latAvg, lonAvg= 0, 0, 0
         else:
             latAvg+= msg.latitude
             lonAvg+= msg.longitude
Geodesic.WGS84.Area(arrayDictLatLon)
#sau folosind un average pe 10 puncte si o diferenta de cel putin 5m intre puncte
arrayDictLatLon, latAvg, lonAvg, index= [], 0.0, 0.0, 0
for elem in array:
	msg = pynmea2.parse(elem)
	index+= 1
	if(index>= 10):
		try:
			dist= Geodesic.WGS84.Inverse(arrayDictLatLon[-1]['lat'], arrayDictLatLon[-1]['lon'], latAvg/10.0, latAvg/10.0)['s12']
			#distance between last point and the point to be add is greater then 5 m.
			print(dist)
			if(dist>= 5.0):
				arrayDictLatLon.append({'lat':latAvg/10.0, 'lon':latAvg/10.0})
		except Exception:
			#the first point should be add manualy
			arrayDictLatLon.append({'lat':latAvg/10.0, 'lon':latAvg/10.0})
		index, latAvg, lonAvg= 0, 0, 0
	else:
		latAvg+= msg.latitude
		lonAvg+= msg.longitude
Geodesic.WGS84.Area(arrayDictLatLon)
