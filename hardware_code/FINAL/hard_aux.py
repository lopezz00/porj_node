from machine import Pin, ADC
from time import sleep
from math import sqrt


class Hardware(object):
    """
    Classe contenedora d'altres instàncies
    """
    def __init__(self):
        self.rele = Rele()
        self.brunzidor = Brunzidor()
        self.led = Led()
        self.corrent = Sensor_Corrent()


class Rele(object):
    """
    Classe per controlar el Relé
    """
    def __init__(self):
        self.pin =  Pin(32, Pin.OUT)
        self.pin.off()

    def on(self):
        """
        Encén el relé
        """
        self.pin.on()

    def off (self):
        """
        Apaga el relé
        """
        self.pin.off()


class Brunzidor(object):
    """
    Classe per controlar el brunzidor
    """
    def __init__(self):
        self.pin = Pin(33,Pin.OUT,value=0)

    def sound(self):
        """
        Fa sonar el brunzidor un cop
        """
        self.pin.on()
        sleep(0.1)
        self.pin.off()
    
    def sound_more(self):
        """
        Fa sonar el brunzidor més d'un cop
        """
        for i in range(5):
            self.sound()
            sleep(0.02)


class Led (object):
    """
    Representa els leds de la placa
    """
    def __init__(self):

        self.vermell = Pin(25,Pin.OUT)
        self.verd =    Pin(26,Pin.OUT)
        self.blau =    Pin(27,Pin.OUT)
 

    def encen(self,color):
        """
        Encén el led especificat.En cas d'error retorna -1
        """

        if color=="Blau":
            self.vermell.value(1)
            self.blau.value(0)
            self.verd.value(1)
                
        elif color =="Verd":
            self.vermell.value(1)
            self.blau.value(1)
            self.verd.value(0)

        elif color == "Vermell":
            self.vermell.value(0)
            self.blau.value(1)
            self.verd.value(1)
            
        else:
            print("Color no definit")
            return -1


    def apaga(self,color):
        """
        Apaga el led especificat. Si posem 'Tots' apaga tots els leds. En cas d'error retorna -1
        """

        if color=="Blau":     
            self.blau.value(1)

        elif color =="Verd":
            self.verd.value(1)

        elif color == "Vermell":
            self.vermell.value(1)
        
        elif color == "Tots":
            self.vermell.value(1)
            self.blau.value(1)
            self.verd.value(1)

        else:
            print("Color no definit")
            return -1


class Sensor_Corrent(object):
    """
    Representa el sensor de corrent
    """
    def __init__(self,Factor_calibracio = 1):
        self.sensor = ADC(Pin(39, Pin.IN))
        self.offset = 1857
        self.factor_calibracio = Factor_calibracio
        self.setup()

    def setup(self):
        """
        # Inicialitza el ADC per llegir correctament. 
        # Atenuació a 11dB i un rang de 0 a 3.3V
        # Mostreig amb 12 bits
        """
        self.sensor.atten(ADC.ATTN_11DB)
        self.sensor.width(ADC.WIDTH_12BIT)

    def set_factor(self,factor):
        """
        Canvia el factor de calibracio
        """
        self.factor_calibracio = factor
 
    def read_current(self):
        """
        Retorna el valor de corrent real. S'aplica un filtre de 
        mitjana mòvil per reduïr el soroll del ADC. Es calcula la 
        tensió RMS i després el corrent que circula per la part secundària
        del transformador de corent. Posteriorment, s'aplica la relació de 
        transformacio del transformador.
        """

        PERIODES = 20
        WINDOWS_SIZE = 20
        y = 0
        sum_yn = 0
         
        for _ in range(PERIODES):                 
            for _ in range(WINDOWS_SIZE):
                sensor_value = self.sensor.read() - self.offset
                valor = sensor_value * 3.3 / 4096
                sum_yn += (valor**2)
                sleep(0.001)
                
            y_n = sum_yn / WINDOWS_SIZE
            sum_yn = 0
            y+= y_n
                
        RESISTENCIA = 33
        Tensio_E = sqrt( y / PERIODES )
        Corrent = Tensio_E / RESISTENCIA
        Corrent_Real = 2000 * Corrent
        return Corrent_Real*self.factor_calibracio


