from machine import Pin
from time import sleep


class Led (object):

    def __init__(self):
        self.vermell = Pin(25,Pin.OUT,value= 0)
        self.verd = Pin(26,Pin.OUT,value= 0)
        self.blau = Pin(27,Pin.OUT,value= 0)
 

    def encen(self,color):

        try:
            if color=="Blau":
                self.vermell.off()
                self.blau.on()
                self.verd.off()
                
            elif color =="Verd":
                self.vermell.off()
                self.blau.off()
                self.verd.on()

            elif color == "Vermell":
                self.vermell.on()
                self.blau.off()
                self.verd.off()
        except:
            print("Color no definit")

    def apaga(self,color):

        try:
            if color=="Blau":     
                self.blau.off()
   
            elif color =="Verd":
                self.verd.off()

            elif color == "Vermell":
                self.vermell.off()

        except:
            print("Color no definit")

