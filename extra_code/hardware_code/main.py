from machine import Pin, SPI,PWM,I2C
from time import sleep
import network
import usocket as socket
import urequests
import ujson

import ssd1306
import random
import framebuf
import logos
import leds,nfc


def request_http(ROUTE,METHOD):
    global Estat
    url = ServerName+ROUTE
    try:
        msgHTTP = urequests.request(METHOD, url)
        responseHTTP = msgHTTP.text
        fromServer= ujson.loads(responseHTTP)
        return fromServer

    except Exception as e:
        
        Estat = "Emergencia"
        
        
def wifi_connect(SSID,PASSWORD):
    """"
    Funció per a establir la connexió WiFi
    """

    global sta_if
    sta_if = network.WLAN(network.STA_IF)

    if not sta_if.isconnected():   
        sta_if.active(True)  # Activa la interfaz STA del ESP32
        sta_if.connect(SSID,PASSWORD)
        print("Conectant a la xarxa",SSID,"...")
        while not sta_if.isconnected():
            pass

    print("Conexió establerta amb exit!")
    print("Configuració de xarxa (IP/netmask/gw/DNS):",sta_if.ifconfig())



def config_display():
    global display
    
    cs = Pin(0,Pin.OUT, value=0)
    dc = Pin(4,Pin.OUT, value=0)
    reset = Pin(2,Pin.OUT,value=1)
    i2c = I2C(sda=Pin(21), scl=Pin(22))
    display = ssd1306.SSD1306_I2C(128, 64, i2c)



def Estat0():
    
    global Estat,spi_dev,pn532,display,Led_Vermell,Led_Verd,Led_Blau,brunzidor, Rele,Estat_anterior
    

    Led_Vermell = Pin(25,Pin.OUT,value=1)
    Led_Vermell.value(0)
    Led_Verd = Pin(26,Pin.OUT)
    Led_Verd.value(1)
    
    config_NFC()
    Rele = Pin(32, Pin.OUT)
    Rele.off()
    brunzidor = Pin(33,Pin.OUT,value=0)
    config_display()
  
    Estat_anterior = "Estat0"
    Estat = "Estat1"

def Estat1():
    global Estat,Estat_anterior
    
    wifi_connect(SSID_Wifi,Password_Wifi)
    Estat_anterior = "Estat1"
    Estat = "Estat2"
    
def Estat2():
    global Estat,spi_dev,pn532,display,Estat_anterior
    logo = logos.wifi_connected()
    config_display()
    buffer = bytearray(logo)
    fb = framebuf.FrameBuffer(buffer,130,95,framebuf.MONO_HLSB)
    display.fill(0)
    display.blit(fb,5,-20)
    display.show()
    sleep(3)
    display.poweroff()
    if Estat == "Estat2":
        Estat_anterior = "Estat2"
        Estat = "Estat3"

def Estat3():
    global Estat,ID_Maquina,display,Estat_anterior
    
    try:
        fromServer= request_http("handshaking/maquina/"+ID_Maquina,"GET")
        if fromServer["msg"] == "handshaking OK":
            Estat_anterior = "Estat3"
            Estat = "Estat4"
    except:
        Estat_anterior = "Estat3"
        Estat = "Emergencia"

def Estat4():
    global Estat,spi_dev,pn532,display,NFC_correcte,ID_Maquina,Estat_anterior,NFC_logo,NO_Reserva
    
    try: 
        fromServer=request_http("reserves/maquina/"+ID_Maquina,"GET")
        if fromServer["msg"] == "noReserva":
            if not(NO_Reserva):
                NO_Reserva = True
                config_display()
                display.text('NO RESERVADA', 15, 25, 1)      
                display.show()
            sleep(2)
     
        elif fromServer["msg"] == "nextReserva":
            if not(NFC_logo):
                NFC_logo = True
                logo = logos.wait_nfc()
                config_display()
                buffer = bytearray(logo)
                fb = framebuf.FrameBuffer(buffer,130,100,framebuf.MONO_HLSB)
                display.fill(0)
                display.blit(fb,5,-15)
                display.show()
                
            config_NFC()
            NFC_correcte = fromServer["usr"]
            uid_targeta = read_nfc(pn532,500)
            if uid_targeta != -1:
                sound()
                if uid_targeta == NFC_correcte:
                    print("Targeta correcte")
                    config_display()
                    logo = logos.correcte()
                    buffer = bytearray(logo)
                    fb = framebuf.FrameBuffer(buffer,110,73,framebuf.MONO_HLSB)
                    display.fill(0)
                    display.blit(fb,5,0)
                    display.show()
                    sleep(1.5)
                    config_display()
                    logo = logos.maquina_on()
                    config_display()
                    buffer = bytearray(logo)
                    fb = framebuf.FrameBuffer(buffer,120,120,framebuf.MONO_HLSB)
                    display.fill(0)
                    display.blit(fb,5,-25)
                    display.show()
                    sleep(2)
                    display.poweroff()
                    Estat_anterior = "Estat4"
                    print("canvia")
                    Estat = "Estat4.1"
                else:
                    print("Targeta incorrecte")
                    logo = logos.incorrecto()
                    config_display()
                    buffer = bytearray(logo)
                    fb = framebuf.FrameBuffer(buffer,130,124,framebuf.MONO_HLSB)
                    display.fill(0)
                    display.blit(fb,0,-30)
                    display.show()
                    sleep(2)
                    logo = logos.wait_nfc()
                    config_display()
                    buffer = bytearray(logo)
                    fb = framebuf.FrameBuffer(buffer,130,100,framebuf.MONO_HLSB)
                    display.fill(0)
                    display.blit(fb,5,-15)
                    display.show()

            else:
                sleep(1)
    except:
        Estat_anterior = "Estat4"
        Estat = "Emergencia"

def Estat4_1():
    global Estat, Estat_actuador, ID_Maquina, Led_Vermell,Led_Verd,Rele,Estat_anterior
    
    print("canviat")
    print("ENCENDER RELE")
    Rele.on()
    Estat_actuador = "ON"
    #Led_Vermell.off()
    Led_Vermell.value(1)
    Led_Verd.value(0)
    try:
        fromServer= request_http("nfc-in/maquina/"+ID_Maquina,"PUT")
        if fromServer["msg"] == "ok":
            Estat_anterior = "Estat4.1"
            Estat = "Estat5"
            sleep(1)
    except:
        Estat_anterior = "Estat4.1"
        Estat = "Emergencia"
          
def Estat5():
    global Estat
    print("ENCENDER DETECTOR CORRIENTE")
    Estat = "Estat6"

def Estat6():
    global Estat,Estat_actuador,ID_Maquina,NFC_correcte,Estat_anterior
    
    try:
        uid_targeta = read_nfc(pn532,500)
        if uid_targeta == -1: # Targeta no llegida
            corriente = random.randint(0,100)
            fromServer=request_http("maquina/"+ID_Maquina+"/estat/"+Estat_actuador+"/consum/"+str(corriente),"PUT")
            if fromServer["msg"] == "ACK":
                Estat_Actuador = fromServer["estat-actuador"]
                if Estat_Actuador == "ON":
                    Rele.on()
                else:
                    Rele.off()
                print(Estat_Actuador)
                sleep(1)
                
            elif fromServer["msg"] == "apaga":
                Estat_anterior = "  Estat6"
                Estat = "Estat7"
                
        elif uid_targeta !=-1 and uid_targeta == NFC_correcte: # Si llegim targeta i es correcte
            sound()
            fromServer=request_http("nfc-out/maquina/"+ID_Maquina,"PUT")
            if fromServer["msg"] == "apaga":
                Estat_anterior = "Estat6"
                Estat = "Estat7"
    except:
        Estat_anterior = "Estat6"
        Estat = "Emergencia"
                
def Estat7():
    global Estat,Estat_actuador,NFC_correcte, Led_Vermell, Led_Verd,Rele,display,NFC_logo
    
    
    logo = logos.maquina_off()
    config_display()
    buffer = bytearray(logo)
    fb = framebuf.FrameBuffer(buffer,100,100,framebuf.MONO_HLSB)
    display.fill(0)
    display.blit(fb,5,-17)
    display.show()
    

    print("ESTAT 7")
    print("APAGANT MAQUINA ...")
    #print("RELE OFF")
    Estat_actuador ="OFF"
    Rele.off()
    NFC_logo = False
    NO_Reserva = False
    Estat = "Estat4"
    NFC_correcte = ""
    sleep(2)
    Led_Vermell.value(0)
    Led.Verd.value(1)
    display.poweroff()
    
def Emergencia(state):
    
    global Estat,display,sta_if,Estat_anterior,NFC_logo,NO_Reserva
    
    if sta_if.isconnected(): #Wifi connectat pero no val el servidor
        for i in range(5):
            sound()
            sleep(0.02)
        sleep(0.5)
        config_display()
        display.text('   NO CONNEXIO', 0, 10, 1)
        display.text('AMB EL SERVIDOR',0,35,1)
        display.show()
        sleep(2)
        display.poweroff()
        if Estat_anterior == "Estat3":
            Estat = "Estat3"
        elif Estat_anterior == "Estat4":
            NFC_logo = False
            NO_Reserva = False
            Estat = "Estat4"
        elif Estat_anterior == "Estat4.1":
            Estat = "Estat4.1"
        elif Estat_anterior == "Estat6":
            Estat = "Estat6"
        else:
            pass
        
    else:                              #S'ha perdut la connexió Wifi
        config_display()
        display.text('   NO CONNEXIO', 0, 10, 1)
        display.text('    WIFI',0,35,1)
        display.show()
        sleep(2)
        display.poweroff()
        for i in range(5):
            sound()
            sleep(0.02)
        sleep(3)
        Estat = "Estat1"
    

def maquina_Estats():
    
    global Estat
    
    if Estat ==   "Estat0":  #Setup
        Estat0()       
    elif Estat == "Estat1": #Init Wifi
        Estat1()    
    elif Estat == "Estat2": #Setup pantalla
        Estat2()        
    elif Estat == "Estat3": #Handshaking amb el server
        Estat3()        
    elif Estat == "Estat4": #Analitza prox reserva i llegeix targeta
        Estat4()        
    elif Estat == "Estat4.1": #Estat intermig per detectar targeta llegida
        Estat4_1()        
    elif Estat == "Estat5": #Switch on del sistema
        Estat5()        
    elif Estat == "Estat6": #Funcionament normal
        Estat6()            
    elif Estat == "Estat7": #Apagar màquina
        Estat7()
    elif Estat == "Emergencia": # Emergencia
        Emergencia(0)
    else:
        pass


def sound():
    """
    global brunzidor
    
    brunzidor.on()
    sleep(0.1)
    brunzidor.off()
    """
    pass


if __name__ == '__main__':

    Estat = "Estat0"
    ServerName = "http://192.168.1.117:5000/"
    NFC_correcte =""
    Estat_actuador = "OFF"
    sta_if = ""
    ID_Maquina = "Maquina1"
    SSID_Wifi = "manu"
    Password_Wifi = "manuelangel"
    Estat_anterior = ""
    NFC_logo = False
    NO_Reserva = False
    spi_dev = ""
    pn532 = ""
    display =""
    brunzidor = ""
  
    Rele = ""
    while True:
        maquina_Estats()









