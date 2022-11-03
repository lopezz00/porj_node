import network
import usocket as socket
from time import sleep
import urequests
import ujson

def wifi_connect(SSID,PASSWORD):
    """"
    Funció per a establir la connexió WiFi
    """

    global sta_if
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():   
        sta_if.active(True)  # Activa la interfaz STA del ESP32
        sta_if.connect(SSID,PASSWORD)
        print("Conectant a la xarxa",SSID,"....")
        while not sta_if.isconnected():
            pass
    print("Conexió establerta amb exit!")
    print("Configuració de xarxa (IP/netmask/gw/DNS):",sta_if.ifconfig())

#sta_if.active(False) #Quan no es necesita el wifi


"""
def json_dumps(d):
    new = ""
    for i in d:
        new+=str(i)+' '+d[i]+' '
    return new

"""

wifi_connect("MiFibra-5DFC","EzytZZp7")
#url = "https://makeblock-micropython-api.readthedocs.io/en/latest/public_library/Third-party-libraries/urequests.html"
#url1= "https://medium.com/geekculture/implementing-http-from-socket-89d20a1f8f43"
url="http://192.168.1.117:5000/prova"
res = urequests.request("GET", url)
msg = res.text
mensaje = ujson.loads(msg)
print(mensaje["VALOR"])



