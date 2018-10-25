import os
import time
import subprocess
import sys
import re
from datetime import datetime

global date,time,hum_inside,temp_inside,hum_outside,temp_outside,pressure,wind_ave,wind_gust,wind_dir,rain

arr = []
i = 0
year = datetime.now().strftime('%Y')
month = datetime.now().strftime('%m')
day = datetime.now().strftime('%d')

def removeLog():
    subprocess.call("sudo rm -v /home/pi/weather/weatherlog.csv",shell=True)

def getData():
    subprocess.call("sudo python3 -m pywws.logdata -vvv /home/pi/weather/data",shell=True)

def formatData():
    global arr, i
    f = open('/home/pi/weather/data/raw/'+year+'/'+year+'-'+month+'/'+year+'-'+month+'-'+day+'.txt')    
    for line in f:
        arr.append(re.split('[, ]+',line))
        #print(arr[i])
        i += 1


def logData():
    if os.path.isdir("/home/pi/weather/"):
        try:
            file = open("/home/pi/weather/weatherlog.csv","a")
        except IOError as e:
            print("IOerror: ",e)
            return 0

        if os.stat("/home/pi/weather/weatherlog.csv").st_size == 0:
            file.write('Date, Time[UTC], Hum_inside[RH], Temp_inside[C], Hum_outside[RH], Temp_outside[C], Abs_pressure[hpa], wind_ave[m/s], wind_gust[m/s], wind_dir, rain[mm]\n')

        file.write(str(date) + ", " + str(time) + ", " + str(hum_inside) + ", " + str(temp_inside) + ", " + str(hum_outside) + ", " + str(temp_outside)
                   + ", " + str(pressure)+ ", " + str(wind_ave)+ ", " + str(wind_gust)+ ", " + str(wind_dir)+ ", " + str(rain) + "\n")
        file.close()

getData()

print("Data gatherd")
formatData()
print("Data formatted")
for row in arr:
    date = row[0]
    time = row[1]
    hum_inside = row[3]
    temp_inside = row[4]
    hum_outside = row[5]
    temp_outside = row[6]
    pressure = row[7]
    wind_ave = row[8]
    wind_gust = row[9]
    wind_dir = row[10]
    rain = row[11] 
    logData()
    print("Logging....")

print("Clearing raw data..")
#Clear the raw data file to avoid formatting the same data twice
open("/home/pi/weather/data/raw/"+year+"/"+year+"-"+month+"/"+year+"-"+month+"-"+day+".txt", "w").close()
#Clear wireless device memory
subprocess.call("sudo pywws-setweatherstation -z",shell=True)
