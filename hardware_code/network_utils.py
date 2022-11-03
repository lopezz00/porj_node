import network
import usocket as socket
import urequests
import ujson



class Wifi(object):
    """
    Instància Wi-Fi per a la connexió. Estableix la connexió amb el punt d'accés i comprova la connexió
    """
    def __init__(self,SSID,PASSWORD):
       self.ssid = SSID
       self.password = PASSWORD
       self.sta_if = None

    def set_ssid(self,ssid):
        """
        Canvia el ssid de la xarxa
        """
        self.ssid = ssid

    def set_password(self,password):
        """
        Canvia el password de la xarxa
        """
        self.password = password
        
    def get_ssid(self):
        """
        Retorna l'ssid de la xarxa
        """
        return self.ssid

    def get_password(self):
        """
        Retorna el password de la xarxa
        """
        return self.password

    def disconnect(self):
        """
        Desconnecta de la xarxa
        """
        self.sta_if.disconnect()

    def connect(self):
        """"
        Funció per a establir la connexió WiFi
        """

        self.sta_if = network.WLAN(network.STA_IF)

        if not self.sta_if.isconnected():   
            self.sta_if.active(True)  
            self.sta_if.connect(self.ssid,self.password)
            print("Conectant a la xarxa",self.ssid,"...")
            while not self.sta_if.isconnected():
                pass

        print("Conexió establerta amb exit!")
        print("Configuració de xarxa (IP/netmask/gw/DNS):",self.sta_if.ifconfig())


    def isconnected(self):
        """
        Retorna l'estat de la connexió
        """

        return self.sta_if.isconnected()

