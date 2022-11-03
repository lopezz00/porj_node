import threading
from time import sleep


def TestThread():
    i = 0
    while i<=3:
        print("Hola")
        sleep(1)
        i+=1
    global x
    x = "hola"
    print("AHORA")
    
    
def prova():
    i = 0
    while i<=3:
        #print("Hola")
        sleep(1)
        i+=1
    global x
    x = "adios"
    print("AHORA de nevo")
    
t1 = threading.Thread(target=TestThread)
t1.start()
x = 0
i = 0

while i<=5 or True:
    if i==5:
        t2 = threading.Thread(target=prova)
        t2.start()
    print(x)
    sleep(1)
    i+=1
