import RPi.GPIO as GPIO
import RPi_I2C_driver
import sys
import time
import spidev

GPIO.setmode(GPIO.BCM)
GPIO.setup(26,GPIO.OUT)

spi = spidev.SpiDev()

spi.open(0,0)

mylcd = RPi_I2C_driver.lcd()

normal_word = [
        #hum
        # UL1
        [0x00,0x03,0x04,0x08,0x09,0x11,0x11,0x10],
        
        # LL1
        [0x10,0x10,0x0B,0x08,0x04,0x03,0x00,0x00],
        
        # UC1
        [0x1F,0x00,0x00,0x00,0x00,0x00,0x00,0x00],
        
        # LC1
        [0x00,0x00,0x1F,0x00,0x00,0x00,0x1F,0x00],
        
        # UR1
        [0x00,0x18,0x04,0x02,0x12,0x11,0x11,0x01],
        
        # LR1
        [0x01,0x01,0x1A,0x02,0x04,0x18,0x00,0x00],
                
]

smile_word = [
        #hum
        # UL1
        [0x00,0x03,0x04,0x08,0x09,0x12,0x12,0x10],
        
        # LL1
        [0x11,0x11,0x08,0x08,0x04,0x03,0x00,0x00],
        
        # UC1
        [0x1F,0x00,0x00,0x00,0x00,0x11,0x11,0x00],
        
        # LC1
        [0x1F,0x00,0x11,0x0E,0x00,0x00,0x1F,0x00],
        
        # UR1
        [0x00,0x18,0x04,0x02,0x12,0x09,0x09,0x01],
        
        # LR1
        [0x11,0x11,0x02,0x02,0x04,0x18,0x00,0x00],
                
]

sad_word = [
        # UL1
        [0x00,0x03,0x04,0x08,0x0A,0x11,0x12,0x10],
        
        # LL1
        [0x10,0x11,0x0A,0x08,0x04,0x03,0x00,0x00],
        
        # UC1
        [0x1F,0x00,0x00,0x00,0x11,0x00,0x11,0x00],
        
        # LC1
        [0x1F,0x00,0x00,0x00,0x00,0x00,0x1F,0x00],
        
        # UR1
        [0x00,0x18,0x04,0x02,0x0A,0x11,0x09,0x01],
        
        # LR1
        [0x01,0x11,0x0A,0x02,0x04,0x18,0x00,0x00],
                
]

def write_normal():
    mylcd.lcd_load_custom_chars(normal_word)
    mylcd.lcd_write(0x8B)
    mylcd.lcd_write_char(0)
    mylcd.lcd_write_char(2)
    mylcd.lcd_write_char(4)
    mylcd.lcd_write(0xCB)
    mylcd.lcd_write_char(1)
    mylcd.lcd_write_char(3)
    mylcd.lcd_write_char(5)
    
def write_smile():
    mylcd.lcd_load_custom_chars(smile_word)
    mylcd.lcd_write(0x8B)
    mylcd.lcd_write_char(0)
    mylcd.lcd_write_char(2)
    mylcd.lcd_write_char(4)
    mylcd.lcd_write(0xCB)
    mylcd.lcd_write_char(1)
    mylcd.lcd_write_char(3)
    mylcd.lcd_write_char(5)
    
def write_sad():
    mylcd.lcd_load_custom_chars(sad_word)
    mylcd.lcd_write(0x8B)
    mylcd.lcd_write_char(0)
    mylcd.lcd_write_char(2)
    mylcd.lcd_write_char(4)
    mylcd.lcd_write(0xCB)
    mylcd.lcd_write_char(1)
    mylcd.lcd_write_char(3)
    mylcd.lcd_write_char(5)

def  analog_read (channel):
    
    r = spi.xfer2 ([1, (8 + channel) << 4, 0])

    adc_out = ((r [1] & 3) << 8) + r [2]

    return  adc_out
        

def dust():
    
        reading = analog_read (0)
        #convert analog value to voltage
        voltage = reading * 5.0 / 1024.0
        
        #initial voltage value defined as (maximum voltage output at no dust(in datasheet))
        dustDensity = (voltage-1.1)/0.5
        mylcd.lcd_clear()
        mylcd.lcd_display_string('Dust:', 1)
        mylcd.lcd_display_string('{0:0.1f}ug/m^3'.format(dustDensity), 2)
        if dustDensity>5 :
        #printangry
        #turnonLED            
            write_sad()
            GPIO.output(26,True)
        elif dustDensity>2 and dustDensity<=5 :
            write_normal()
            GPIO.output(26,False)
        #printSOSO
        else:
            write_smile()
            GPIO.output(26,False)
        #turnoffLED
        #printsmile
        time.sleep(3)
        mylcd.lcd_clear()

 