from random import randint
from geographiclib.geodesic import Geodesic

#using a KML file and some find and replace after ",0 " with "],["
teren= [[23.68970153488142,46.19120332951173],[23.68959667475334,46.19107550056226],[23.68944440525471,46.19085744832206],[23.68928689255713,46.1906103168421],[23.68922710442046,46.19051680344764],[23.68917812136847,46.19043653899671],[23.68914316550367,46.19037925951842],[23.68913841693797,46.1903418022131],[23.68916433489885,46.19030975336306],[23.68920834200039,46.19028531462806],[23.68937870592084,46.19023577460963],[23.68947799030815,46.19020641198885],[23.68957478382055,46.1901568787077],[23.68969634448233,46.19011302362734],[23.68978738434844,46.19007405379971],[23.68987025414047,46.19004101625719],[23.68995846866162,46.19001173978383],[23.69030593504039,46.18987701087457],[23.69051186401216,46.18980175832679],[23.69068157991739,46.18973009805196],[23.69077797112229,46.18968697990837],[23.69088563393125,46.18964412501263],[23.69173488062812,46.190846634822],[23.69153582676503,46.19090955850043],[23.6913110816598,46.19096447871959],[23.69113605820223,46.19099854426297],[23.69091111298964,46.19101075546097],[23.69073953495833,46.19101889515951],[23.69064454218459,46.19101890163583],[23.69053881256091,46.19103116529374],[23.69043045150249,46.19106423993637],[23.69029120280761,46.19111078693992],[23.6901831033999,46.19115768783973],[23.69003416155047,46.19123917781445],[23.6899158277609,46.19127204854518],[23.6897985652076,46.19128997778105]]

# METHOD 1: make noise using random
terenZgomot, terenZgomotKML= [], []
randLat, randLong= 0, 0
for elem in teren:
	for i in range(1, 10):
		randLong= randint(0,9)*(1- 0.9999999)
		while(randLong == 0):
			randLong= randint(0,9)*(1- 0.9999999)
		randLat= randint(0,9)*(1- 0.9999999)
		while(randLat == 0):
			randLat= randint(0,9)*(1- 0.9999999)
		terenZgomot.append([elem[0]+ randLong, elem[1]+randLat])
		
# METHOD 2: make noyse using average, will double the size
def avg_array(array):
	returnArray= []
	for i in range(1, len(array)-1):
		returnArray.append(
			[array[i][0], array[i][1]])
		returnArray.append(
			[(array[i][0]+ array[i-1][0])/2, (array[i][1]+ array[i-1][1])/2])
	return returnArray
terenZgomotAvg= avg_array(teren)
	
#VAR 1: run the alg on original/noisy path
arrayDictLatLon= []
for elem in teren:
	arrayDictLatLon.append({'lat':elem[1], 'lon':elem[0]})
	
g= Geodesic.WGS84.Area(arrayDictLatLon)
g['area']/10000
#VAR 2: make an average of N points
arrayDictLatLon, latAvg, lonAvg, index, medie= [], 0.0, 0.0, 0, 5.0
for elem in terenZgomot:
         index+= 1
         if(index> medie):
             arrayDictLatLon.append({'lat':latAvg/medie, 'lon':lonAvg/medie})
             index, latAvg, lonAvg= 0, 0, 0
         else:
             latAvg+= elem[1]
             lonAvg+= elem[0]
             
g= Geodesic.WGS84.Area(arrayDictLatLon)
g['area']/10000
#VAR 3: average on N+ minimum distance M
arrayDictLatLon, latAvg, lonAvg, index, medie, distMin, = [], 0.0, 0.0, 0, 5.0, 5.0
for elem in terenZgomot:
	index+= 1
	if(index> medie):
		try:
			dist= Geodesic.WGS84.Inverse(arrayDictLatLon[-1]['lat'], arrayDictLatLon[-1]['lon'], latAvg/medie, latAvg/medie)['s12']
			#distance between last point and the point to be add is greater then 5 m.
			print(Geodesic.WGS84.Inverse(arrayDictLatLon[-1]['lat'], arrayDictLatLon[-1]['lon'], latAvg/medie, latAvg/medie))
			if(dist>= distMin):
				arrayDictLatLon.append({'lat':latAvg/medie, 'lon':lonAvg/medie})
			else:
				print("Dist to small")
		except Exception:
			#the first point should be add manualy
			print("Exception")
			arrayDictLatLon.append({'lat':latAvg/medie, 'lon':lonAvg/medie})
		index, latAvg, lonAvg= 0, 0, 0
	else:
		latAvg+= elem[1]
		lonAvg+= elem[0]

g= Geodesic.WGS84.Area(arrayDictLatLon)
g['area']/10000
#prepare to be put again in KML file
for elem in terenZgomot:
	terenZgomotKML.append(elem[0])
	terenZgomotKML.append(elem[1])
	terenZgomotKML.append(0)
