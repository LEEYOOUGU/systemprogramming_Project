import RPi.GPIO as GPIO
import RPi_I2C_driver
import sys
import Adafruit_DHT
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(19,GPIO.OUT)
GPIO.cleanup()

mylcd = RPi_I2C_driver.lcd()


hum_word = [
        #hum
        # UL1
        [ 0x00,0x00,0x01,0x03,0x03,0x07,0x07,0x0F],
        
        # LL1
        [ 0x0F,0x1F,0x1F,0x1F,0x1F,0x1F,0x0E,0x07],
        
        # UR1
        [ 0x00,0x10,0x18,0x18,0x1C,0x1C,0x1C,0x1E],
        
        # LR1
        [ 0x1E,0x1F,0x1D,0x1D,0x1D,0x1B,0x06,0x1C],
        
        #temp
        # UL1
        [ 0x01,0x02,0x02,0x02,0x02,0x02,0x02,0x02],
        
        # LL1
        [ 0x01,0x05,0x0B,0x17,0x17,0x13,0x08,0x07],
        
        # UR1
        [ 0x10,0x08,0x18,0x08,0x18,0x08,0x18,0x08],
        
        # LR1
        [ 0x10,0x14,0x1A,0x1D,0x1D,0x19,0x02,0x1C],
                
]


def write():
    mylcd.lcd_load_custom_chars(hum_word)
    mylcd.lcd_write(0x80)
    mylcd.lcd_write_char(0)
    mylcd.lcd_write_char(2)
    mylcd.lcd_write(0xC0)
    mylcd.lcd_write_char(1)
    mylcd.lcd_write_char(3)
    mylcd.lcd_write(0x88)
    mylcd.lcd_write_char(4)
    mylcd.lcd_write_char(6)
    mylcd.lcd_write(0xC8)
    mylcd.lcd_write_char(5)
    mylcd.lcd_write_char(7)
    

    
def dht():
    GPIO.setup(19,GPIO.OUT)
    humidity, temperature = Adafruit_DHT.read_retry(11, 4)
    write()
    if(temperature >= 30):
        GPIO.output(19,True)
    else:
        GPIO.output(19,False)
    mylcd.lcd_display_string_pos('Temp', 1,10)
    mylcd.lcd_display_string_pos('{0:0.1f}C'.format(temperature), 2,10)
    mylcd.lcd_display_string_pos('Humi', 1,2)
    mylcd.lcd_display_string_pos('{0:0.1f}%'.format(humidity), 2, 2)
    time.sleep(3)
    mylcd.lcd_clear()

