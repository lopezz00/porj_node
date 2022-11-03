import library_nfc as nfc
from machine import Pin, SPI


spi_dev = None
pn532 = None



def config_NFC():
    """
    Configuració general del NFC per SPI
    """

    global spi_dev, pn532
    
    spi_dev = SPI(2, baudrate=1000000, sck=Pin(18), mosi=Pin(23), miso=Pin(19))
    cs = Pin(5, Pin.OUT)
    cs.on()
    pn532 = nfc.PN532(spi_dev,cs)
    ic, ver, rev, support = pn532.get_firmware_version()
    pn532.SAM_configuration()


def read_nfc():
    """
    Llegeix una targeta NFC en un temps(ms). Si no troba cap retorna -1.
    """
    global pn532
    
    dev = pn532
    tmot = 500
    uid = pn532.read_passive_target(timeout=tmot)

    if uid is None:
        return -1
    else:
        uid_targeta = ""
        for i in uid:
            uid_targeta+= str(hex(i))[2:]

        print('Found card with UID:',uid_targeta)
        return uid_targeta


