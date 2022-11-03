import hard_aux as hard
from machine import ADC,Pin
from math import sqrt
from time import sleep

rele = hard.Rele()
rele.on()


pot = ADC(Pin(39, Pin.IN))
pot.atten(ADC.ATTN_11DB)     #Atenuamos a 11DB, 0 - 3.3V
pot.width(ADC.WIDTH_12BIT)   #Mostreamos a 12bits



def read_current():
    
    PERIODES = 20
    WINDOWS_SIZE = 20
    y = 0
    sum_yn = 0
    offset = 1857
    
    for _ in range(PERIODES):                 
        for _ in range(WINDOWS_SIZE):
            pot_value = pot.read() - offset
            valor = pot_value * 3.3 / 4096
            sum_yn += (valor**2)
            sleep(0.001)
        
        y_n = sum_yn / WINDOWS_SIZE
        sum_yn = 0
        y+= y_n
        
    RESISTENCIA = 33
    Tensio_E = sqrt( y / PERIODES )
    Corrent = Tensio_E / RESISTENCIA
    Corrent_Real = 2000 * Corrent
    return Corrent_Real
    


while True:  
    print(read_current()*0.725*230)
    sleep(1)


