import RPi.GPIO as GPIO
import DHT_Driver
import SAYING
import Microdust
#import Microdust
#!/usr/bin/python
import sys
import time
import spidev




    

          

while True:
    timenow = time.localtime()
    hour = timenow.tm_hour+8
    if(((hour >= 8)&(hour<=9)) | ((hour>=17)&(hour<=18))):  
        SAYING.word1()
        time.sleep(2)
        SAYING.word2()
    DHT_Driver.dht()
    Microdust.dust()
    


 


  
  
