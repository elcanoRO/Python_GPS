/****************************************************************
 * ReadSHT2x
 *  https://github.com/misenso/SHT2x-Arduino-Library
 *  An example sketch that reads the sensor and prints the
 *  relative humidity to the PC's serial port
 *
 *  Tested with:
 *    - SHT21-Breakout Humidity sensor from Modern Device
 *    - SHT2x-Breakout Humidity sensor from MisensO Electronics
 *
 * Online calc for dew point: http://andrew.rsmas.miami.edu/bmcnoldy/Humidity.html
 * Online function plot for dew point formula for different temps: http://fooplot.com/
 ***************************************************************/

#include <Wire.h>
#include <SHT2x.h>

float temp, humi, k, drewPoint;

void setup()
{
  Serial.begin(9600);
  Serial.println("Finish");
  Wire.begin();
}

void loop()
{
  temp= SHT2x.GetHumidity();
  humi= SHT2x.GetTemperature();
  k= log(humi/100) + (17.62 * temp) / (243.12 + temp);
  drewPoint= 243.12 * k / (17.62 - k);
  Serial.print("Humidity(%RH): ");
  Serial.print(temp);
  Serial.print("     Temperature(C): ");
  Serial.print(humi);
  Serial.print("     Punct de roua: ");
  Serial.println(drewPoint);
  
  delay(1000);
}
