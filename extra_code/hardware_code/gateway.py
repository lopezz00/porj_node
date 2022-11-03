#!/usr/bin/python3
# -*- coding: utf-8 -*-


#  ================== #
#      LLIBRERIES     #
#  ================== #

import json, requests, seguretat


#  ================== #
#      VARIABLES      #
#  ================== #

Server_Name = "https://epsemtechlab.ddns.net/"


#  ================== #
#      FUNCIONS       #
#  ================== #


def server_request():
    """
    Retorna una llista amb el nom de les màquines. En cas d'error retorna -1
    """

    try:
        http=requests.get(Server_Name+"/maquines/all") 
        msg=json.loads(http.content)
        return msg["maqs"]

    except Exception as e:
        return -1


def server_put(dades):
    """
    Insereix les dades encriptades al servidor. En cas d'error retorna -1
    """

    try:
        ssid = seguretat.encripta(dades[1]).decode("utf-8")
        pswd = seguretat.encripta(dades[2]).decode("utf-8")

        http=requests.put(Server_Name+"/config/maquina/"+dades[0]+"/"+ssid+"/"+pswd,data={})
        msg=json.loads(http.content)
        return msg["config"]

    except Exception as e:
        return -1
