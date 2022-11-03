from machine import Pin,I2C
import ssd1306
from time import sleep

# using default address 0x3C
cs = Pin(0,Pin.OUT, value=0)
dc = Pin(4,Pin.OUT, value=0)
reset = Pin(2,Pin.OUT,value=1)
i2c = I2C(sda=Pin(21), scl=Pin(22))
display = ssd1306.SSD1306_I2C(128, 64, i2c)

"""
display.text('Hello, World!', 0, 0, 1)
display.show()
display.text('Manu', 0, 10, 1)
display.show()
sleep(3)
display.poweroff()
sleep(2)
display = ssd1306.SSD1306_I2C(128, 64, i2c)
print("Manu ara")
display.text('Manu', 0, 0, 1)
display.show()
sleep(3)
print("apaga")
display = ssd1306.SSD1306_I2C(128, 64, i2c)
display.poweroff()
"""


