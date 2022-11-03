import hard_aux as hard
from time import sleep
import nfc
from machine import Pin,I2C
import ssd1306
import network
import usocket as socket
import ujson
import time
import request as urequests


def connect (red, password):
    
     global WiFi
     WiFi = network.WLAN(network.STA_IF)
     WiFi.active(False)                
     if not WiFi.isconnected():              #Si no está conectado…
         WiFi.active(True)                   #activa la interface
         WiFi.connect(red, password)         #Intenta conectar con la red
         print('Conectant a la xarxa', red +"…")
         timeout = time.time ()
         while not WiFi.isconnected():           #Mientras no se conecte..
             if (time.ticks_diff (time.time (), timeout) > 15):
                 return False
     return True
    
    
def request_http(ServerName, ROUTE,METHOD):
    """
    Fa una petició a un servidor per http. Retorna el que t'envia el servidor.
    En cas d'error retorna -1
    """   
    url = ServerName+ROUTE
    try:
        msgHTTP = urequests.request(METHOD, url)
        responseHTTP = msgHTTP.text
        fromServer= ujson.loads(responseHTTP)
        return fromServer

    except Exception as e:
        return -1


def configDisplay():
    global Pantalla
    
    cs = Pin(0,Pin.OUT, value=0)
    dc = Pin(4,Pin.OUT, value=0)
    reset = Pin(2,Pin.OUT,value=1)
    i2c = I2C(sda=Pin(21), scl=Pin(22))
    Pantalla = ssd1306.SSD1306_I2C(128, 64, i2c)


def canviaWifi(ssid,password):
    
    global SSID_Wifi, Password_Wifi, SSID_Wifi_antic, Password_Wifi_antic, WiFi,EstatWiFi, Pantalla, FlagWifi, Flag_Reserva, Estat
    
    WiFi.disconnect()
    configDisplay()
    Pantalla.text("MAQUINA OFF",20,0)
    Pantalla.text("WIFI RECONNECT",10,30)
    Pantalla.show()
    EstatWiFi = connect(ssid,password)
    
    if not(EstatWiFi):
        EstatWiFi = connect(SSID_Wifi_antic, Password_Wifi_antic)
        while not (EstatWiFi):
            Pantalla.poweroff()
            configDisplay()
            Pantalla.text("MAQUINA OFF",20,0)
            Pantalla.text("WIFI CONNECT",15,30)
            Pantalla.show()
            sleep(1)
        FlagWifi = 1
        SSID_Wifi = SSID_Wifi_antic
        Password_Wifi = Password_Wifi_antic
        
    else:
        SSID_Wifi_antic = SSID_Wifi
        Password_Wifi_antic = Password_Wifi
        SSID_Wifi = ssid
        Password_Wifi = password
        
    if Estat == "Estat2":
        Pantalla.poweroff()
        Flag_Reserva = False
    
    elif Estat == "Estat3":
        Pantalla.poweroff()
        configDisplay()
        Pantalla.text("MAQUINA OFF",20,0)
        Pantalla.text("ESPERANT NFC",17,30)
        Pantalla.show()
    
    elif Estat == "Estat5":
        Flag_Finalitzar = False
        Pantalla.poweroff()
        configDisplay()
        Pantalla.text("MAQUINA ON",20,0)
        Pantalla.show()
        
        
def Estat0():

    global Estat, Estat_anterior, WiFi, Hardware, SSID_Wifi, Password_Wifi, Pantalla, EstatWiFi, FlagWifi

    if not(FlagWifi):
        configDisplay()
        Pantalla.text("MAQUINA OFF",20,0)
        Pantalla.text("CONNECTANT...",15,30)
        Pantalla.show()
        sleep(1)
        Hardware = hard.Hardware()
        Hardware.led.encen("Vermell")
        Hardware.rele.off()
        EstatWiFi = connect(SSID_Wifi,Password_Wifi)
        
    if not(EstatWiFi):
        Estat_anterior = "Estat0"
        Estat = "Emergencia"
    else:
        configDisplay()
        Pantalla.text("MAQUINA OFF",20,0)
        Pantalla.text("WIFI CONNECT",15,30)
        Pantalla.show()
        sleep(1)
        Estat_anterior = "Estat0"
        Estat = "Estat1"


def Estat1():

    global Estat, Estat_anterior, ServerName, ID_Maquina, Hardware,SSID_Wifi

    response = request_http(ServerName,"handshaking/maquina/"+ID_Maquina,"GET")
    FlagWifi = 0
    
    if response == -1:
        Estat_anterior = "Estat1"
        Estat = "Emergencia"
        
    elif response["msg"] == "ACK handshaking":
        Hardware.corrent.set_factor(float(response["factor_calibracio"]))
        Estat = "Estat2"
        Estat_anterior = "Estat1"
    
    else:
        sleep(1)


def Estat2():

    global Estat, Estat_anterior, ID_Maquina, ServerName, NFC_correcte, Hardware,Pantalla, Flag_Reserva, FlagWifi, FlagChangeWifi, SSID_Wifi
    

    response = request_http(ServerName,"reserves/maquina/"+ID_Maquina+'/'+str(FlagWifi),"GET")

    if response == -1:
        Estat_anterior = "Estat2"
        Estat = "Emergencia"
 
    if response["ssid_wifi"] != SSID_Wifi:
        canviaWifi(response["ssid_wifi"],response["password_wifi"])

    if FlagWifi and not(FlagChangeWifi):
        FlagChangeWifi = True
       
    elif FlagChangeWifi:
        FlagChangeWifi = False
        FlagWifi = 0

    if response["msg"] == "noReserva" and not(Flag_Reserva):
        Pantalla.poweroff()
        configDisplay()
        Pantalla.text("MAQUINA OFF",20,0)
        Pantalla.text("SENSE RESERVES",10,30)
        Pantalla.show()
        Flag_Reserva = True
    
    elif response["msg"] == "nextReserva":
        NFC_correcte = response["usr"]
        Estat = "Estat3"
        Estat_anterior = "Estat2"
        Pantalla.poweroff()
        configDisplay()
        Pantalla.text("MAQUINA OFF",20,0)
        Pantalla.text("ESPERANT NFC",17,30)
        Pantalla.show()
            
    sleep(1)


def Estat3():

    global Estat, Estat_anterior, ID_Maquina, ServerName, NFC_correcte, Hardware, Flag_Reserva, Pantalla, FlagWifi, FlagChangeWifi, SSID_Wifi
    
    response = request_http(ServerName,"reserves/maquina/"+ID_Maquina+'/'+str(FlagWifi),"GET")
    nfc.config_NFC()
    if response == -1:
        Estat_anterior = "Estat3"
        Estat = "Emergencia"
        Flag_Reserva = False
        
    if response["ssid_wifi"] != SSID_Wifi:
        canviaWifi(response["ssid_wifi"],response["password_wifi"])

    if FlagWifi and not(FlagChangeWifi):
        FlagChangeWifi = True
       
    elif FlagChangeWifi:
        FlagChangeWifi = False
        FlagWifi = 0

        
    if response["msg"] == "noReserva":
        Estat = "Estat2"
        Pantalla.poweroff()
        configDisplay()
        Pantalla.text("MAQUINA OFF",20,0)
        Pantalla.text("SENSE RESERVES",10,30)
        Pantalla.show()
        Estat_anterior = "Estat1"
    
    elif response["msg"] == "nextReserva":
        NFC_correcte = response["usr"]
        uid = nfc.read_nfc()
        if uid == NFC_correcte:
            Hardware.brunzidor.sound()
            Pantalla.poweroff()
            configDisplay()
            Pantalla.text("MAQUINA OFF",20,0)
            Pantalla.text("USUARI ACCEPTAT",5,30)
            Pantalla.show()
            sleep(1)
            Pantalla.poweroff()
            Estat = "Estat4"
            Estat_anterior = "Estat3"
            
        elif uid != -1:
            Hardware.brunzidor.sound()
            Pantalla.poweroff()
            configDisplay()
            Pantalla.text("MAQUINA OFF",20,0)
            Pantalla.text("INCORRECTE",25,30)
            Pantalla.show()
            sleep(1)
            Pantalla.poweroff()
            configDisplay()
            Pantalla.text("MAQUINA OFF",20,0)
            Pantalla.text("ESPERANT NFC",17,30)
            Pantalla.show()
               
    
def Estat4():

    global Estat, Estat_anterior, Hardware, ServerName, Estat_actuador, ID_Maquina, Pantalla, FlagWifi, FlagChangeWifi, SSID_Wifi

    response = request_http(ServerName,"nfc-in/maquina/"+ID_Maquina+'/'+str(FlagWifi),"PUT")
    
    if response == -1: 
        Estat_anterior = "Estat4"
        Estat = "Emergencia"
        
    if response["ssid_wifi"] != SSID_Wifi:
        canviaWifi(response["ssid_wifi"],response["password_wifi"])

    if FlagWifi and not(FlagChangeWifi):
        FlagChangeWifi = True
       
    elif FlagChangeWifi:
        FlagChangeWifi = False
        FlagWifi = 0
        
    if response["msg"] == "ok":
        Hardware.led.encen("Verd")
        Hardware.rele.on()
        Estat_actuador = "ON"
        Pantalla.poweroff()
        configDisplay()
        Pantalla.text("MAQUINA ON",20,0)
        Pantalla.show()
        Estat = "Estat5"
        Estat_anterior = "Estat4"
    


def EstatActuador():

    global Estat_actuador, Hardware

    if Estat_actuador == "ON":
        Hardware.rele.on()
    else:
        Hardware.rele.off()


def Estat5():

    global Estat, Estat_anterior, NFC_correcte, Hardware, ID_Maquina, ServerName,Estat_actuador, Pantalla, Flag_Finalitzar, FlagWifi, FlagChangeWifi, SSID_Wifi
    

    uid = nfc.read_nfc()
    if uid == NFC_correcte:
        response = request_http(ServerName,"nfc-out/maquina/"+ID_Maquina,"PUT")
        if response == -1:
            Estat = "Emergencia"
            Estat_anterior = "Estat5"
        
        elif response["msg"] == "apaga":
            Hardware.brunzidor.sound()
            Pantalla.poweroff()
            configDisplay()
            Pantalla.text("MAQUINA ON",20,0)
            Pantalla.text("SORTINT...",25,30)
            Pantalla.show()
            sleep(2)
            Estat = "Estat6"
            Estat_anterior = "Estat5"

    else:
        if Estat_actuador == "OFF":
            consum = 0
        else:
            consum = Hardware.corrent.read_current()
    
        response = request_http(ServerName,"maquina/"+ID_Maquina+"/estat/"+Estat_actuador+"/consum/"+str(consum)+'/'+str(FlagWifi),"PUT")

        if response == -1:
            Estat = "Emergencia"
            Estat_anterior = "Estat5"
            
        if response["ssid_wifi"] != SSID_Wifi:
            canviaWifi(response["ssid_wifi"],response["password_wifi"])

        if FlagWifi and not(FlagChangeWifi):
            FlagChangeWifi = True
           
        elif FlagChangeWifi:
            FlagChangeWifi = False
            FlagWifi = 0
            
        if response["msg"] == "ACK":
            if response["ssid_wifi"] != SSID_Wifi:
                canviaWifi(response["ssid_wifi"],response["password_wifi"])
            Estat_actuador = response["estat-actuador"]
            EstatActuador()
            
        elif response["msg"] == "FINALITZANT":
            if not(Flag_Finalitzar):
                Pantalla.poweroff()
                configDisplay()
                Pantalla.text("MAQUINA ON",20,0)
                Pantalla.text("FINALITZANT...",15,30)
                Pantalla.show()
                Flag_Finalitzar = True
                
        elif response["msg"] == "apaga":
            Hardware.brunzidor.sound()
            Pantalla.poweroff()
            configDisplay()
            Pantalla.text("MAQUINA ON",20,0)
            Pantalla.text("SORTINT...",25,30)
            Pantalla.show()
            sleep(2)
            Estat = "Estat6"
            Estat_anterior = "Estat5"
            
        elif response == -1:
            Estat = "Emergencia"
            Estat_anterior = "Estat5"
        


def Estat6():

    global Estat, Estat_anterior, Hardware, NFC_correcte, Estat_actuador,Flag_Reserva, Flag_Finalitzar
    Estat_actuador = "OFF"
    Hardware.rele.off()
    Hardware.led.encen("Vermell")
    NFC_correcte = "undefined"
    Estat = "Estat2"
    Estat_anterior = "Estat1"
    Flag_Reserva  = False
    Flag_Finalitzar = False
    Flag_Emergencia = False


def Emergencia():

    global Estat, Estat_anterior, WiFi, Hardware, SSID_Wifi, Password_Wifi, Pantalla, Flag_Reserva, Flag_Emergencia, Flag_Finalitzar, EstatWiFi, Reconnectar, FlagWifi,SSID_Wifi_antic,Password_Wifi_antic  

    Hardware.led.encen("Blau")
    if not(Flag_Emergencia):
        Hardware.brunzidor.sound_more()
        Flag_Emergencia = True
        
    if not(EstatWiFi):
        configDisplay()
        Pantalla.text("EMERGENCIA",25,0)
        Pantalla.text("ERROR WIFI",25,30)
        Pantalla.show()
        EstatWiFi = connect( SSID_Wifi_antic,Password_Wifi_antic)
        if EstatWiFi:
            configDisplay()
            Pantalla.text("MAQUINA OFF",20,0)
            Pantalla.text("WIFI RECONNECT",10,30)
            Pantalla.show()
            sleep(2)
        Estat = Estat_anterior
        FlagWifi = 1
        sleep(1)

    else:
        Pantalla.poweroff()
        configDisplay()
        Pantalla.text("EMERGENCIA",25,0)
        Pantalla.text("ERROR SERVIDOR",10,30)
        Pantalla.show()
        sleep(1)

    Flag_Reserva = False
    Estat = Estat_anterior
    
    if Estat_anterior == "Estat1" or Estat_anterior =="Estat2" or Estat=="Estat3":
        Hardware.led.encen("Vermell")
    
    else:
        Hardware.led.encen("Verd")
        
    if Estat_anterior == "Estat3":
        configDisplay()
        Pantalla.text("MAQUINA OFF",20,0)
        Pantalla.text("ESPERANT NFC",17,30)
        Pantalla.show()
    
    elif Estat_anterior == "Estat5":
        if  Flag_Finalitzar:
            Pantalla.poweroff()
            configDisplay()
            Pantalla.text("MAQUINA ON",20,0)
            Pantalla.text("FINALITZANT...",15,30)
            Pantalla.show()
        else:        
            Pantalla.poweroff()
            configDisplay()
            Pantalla.text("MAQUINA ON",20,0)
            Pantalla.show()


def maquina_Estats():
    
    global Estat
    
    if Estat ==   "Estat0":  # Setup
        Estat0()       

    elif Estat == "Estat1": # Handshaking
        Estat1()

    elif Estat == "Estat2": # Proxima reserva
        Estat2()

    elif Estat == "Estat3": # Espera targeta i mira reserves
        Estat3()

    elif Estat == "Estat4": # Encen màquina
        Estat4()

    elif Estat == "Estat5": # Llegeix valors de potencia i els envia al servidor
        Estat5()

    elif Estat == "Estat6": # Apaga la maquina i torna a l'estat de demanar reserva
        Estat6()

    elif Estat == "Emergencia": # Emergencia
        Emergencia()



if __name__ == '__main__':

    ID_Maquina = "Maquina1" 
    Estat_actuador = "OFF"
    Estat = "Estat0"
    Estat_anterior = "Estat0"
    SSID_Wifi = "Prieto"
    Password_Wifi = "12345678"
    SSID_Wifi_antic = "Prieto"
    Password_Wifi_antic = "12345678"
    
    ServerName = "http://192.168.121.163:5000/"
    NFC_correcte ="undefined"
    Hardware = "undefined"
    WiFi = "undefined" 
    Pantalla = "undefined"
    Flag_Reserva = False
    Flag_Emergencia = False
    Flag_Finalitzar = False
    FlagWifi = 0
    FlagChangeWifi = False
    
    
    while True:
        maquina_Estats()



