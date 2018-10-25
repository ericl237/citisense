import i2c2
import time
import subprocess
import sys

clock = i2c2.DS1307()
global month,dayOfMonth,hour,minute,second

while 1:
    
    clock.getTime()
    time.sleep(1)
    print(clock.hour, ":", clock.minute, ":", \
            clock.second, " ", clock.dayOfMonth, "/", \
            clock.month, "/", clock.year,"  ", "weekday", \
            ":", clock.dayOfWeek        )



