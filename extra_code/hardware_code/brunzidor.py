from machine import Pin,PWM
from time import sleep

pwm = Pin(33,Pin.OUT,value=0)
pwm4 = PWM(pwm, freq=1000, duty=512) 
sleep(0.2)
pwm4.duty(0)