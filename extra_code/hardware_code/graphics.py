#!/usr/bin/python3 python3


#  ================== #
#      LLIBRERIES     #
#  ================== #

import tkinter, gateway 
from tkinter import *
from tkinter import messagebox
from tkinter import font
from tkinter import ttk
from tkinter.constants import Y


#  ================== #
#        CODI         #
#  ================== #

app = tkinter.Tk()
app.title("Configuració màquines")
app.geometry("500x300")

title = tkinter.LabelFrame(app, text="Configuració general de la màquina", font="Sans-Serif 20")
title.grid(row = 0, column = 0, padx = 8,pady = 20,sticky=S+E+N+W)

lnom = tkinter.Label(title, text="Nom màquina:", font="Sans-Serif 14 bold", bg="deep sky blue",justify=CENTER)
lnom.grid(row=2,column=0,padx=7,pady=7)
nomMaq=tkinter.StringVar()
noms = gateway.server_request()
nom = ttk.Combobox(title, values = noms, font="Sans-Serif", textvariable=nomMaq) #Id maquina
nom.grid(row=2,column=1)

lwifi = tkinter.Label(title, text="SSID Wifi:", font="Sans-Serif 14 bold", bg="deep sky blue", justify=CENTER)
lwifi.grid(row=3,column=0,ipadx=25,padx=6,pady=6)
wifi = tkinter.Entry(title, font="Sans-Serif") #SSID wifi
wifi.grid(row=3, column=1)

lpswd = tkinter.Label(title, text="Password Wifi:", font="Sans-Serif 14 bold", bg="deep sky blue", justify=CENTER)
lpswd.grid(row=4,column=0,padx=7,pady=7)
pswd = tkinter.Entry(title, font="Sans-Serif", show="*") #Password wifi
pswd.grid(row=4,column=1)

def EnviaDades():
    """
    Comprova les dades que entren per la pantalla i envia els valors al servidor. En cas d'errors, els mostra
    """

    if nom.get() and wifi.get() and pswd.get():
        dades = (nom.get(), wifi.get(), pswd.get())

        if gateway.server_put(dades) == "OK":
            app.destroy()
        else:
            tkinter.messagebox.showwarning(title="Error", message="No s'han enviat les dades correctament")


    else:
        if not nom.get() or not wifi.get() or not pswd.get():
            tkinter.messagebox.showwarning(title="Error", message="Tots els camps són obligatoris")
        else:
            pass
        
        pswd.focus_set()


conf = tkinter.Button(title, text="Configurar", bg="deep sky blue", font="Sans-Serif", command=EnviaDades)
conf.grid(row=6,column=1,pady=10)

if noms == -1:
    tkinter.messagebox.showwarning(title="Error", message="No hi ha connexió amb el servidor. Comprova la teva connexió")
    app.mainloop()

else:
    app.mainloop()

