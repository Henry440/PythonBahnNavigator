import json
import requests
from datetime import datetime

import ZugDaten as train

def station_search():
    search = ""
    try:
        search = raw_input("Suche : ") #Fehler Bei Windows
    except Exception:
        search = input("Suche : ")
    search = str(search)
    #url = "https://marudor.de/api/hafas/v1/station/" + search
    url = "https://marudor.de/api/station/v1/search/" + search
    #print(url)
    param = dict()
    resp = requests.get(url = url, params=param)
    data = resp.json()
    stations = [""]
    evaID = [""]

    count = 0
    for x in data:
        count = count + 1
    for x in range(count):
        stations.append(data[x]["title"])
        evaID.append(data[x]["id"])
    stations.remove("")
    evaID.remove("")
    return (stations, evaID)

def selectStation(data):
    stations = data[0]
    evaID = data[1]
    i = 1
    for st in stations:
        print(str(i) + ") " + st)
        i = i + 1
    auswahl = 1
    try:
        auswahl = int(raw_input("Station Waehlen : "))
    except Exception:
        auswahl = int(input("Station Waehlen : "))
    auswahl = auswahl - 1
    return auswahl

def printAnkunft(datas):
    fahrten = datas["departures"]
    for x in fahrten:
        try:
            zug = x["train"]["name"]
            if(x["arrival"]["cancelled"] == False):
                print(zug + "\t nach : " + x["destination"] + "\t Ankunft Plan : " + timestamp_to_time(x["arrival"]["scheduledTime"]) + "\t Ankunft Real : " + timestamp_to_time(x["arrival"]["time"]))
            else:
                print(zug + " Faellt aus !")
        except Exception as Zugdatene:
            pass

def abfahrten(eva):
    print("Abfahrten")
    url = "https://marudor.de/api/iris/v1/abfahrten/" + eva
    print(url)
    param = dict()
    resp = requests.get(url = url, params=param)
    data = resp.json()
    return data

def timestamp_to_time(timestamp):
    time = int(timestamp / 1000)
    dt_object = datetime.fromtimestamp(time)
    timestring = dt_object.strftime("%X")
    return timestring


data = station_search()
auswahl = int(selectStation(data))
zugdaten = abfahrten(data[1][auswahl])
printAnkunft(zugdaten)

workdata = train.Zug(zugdaten)
workdata.test()
z = workdata.getAnkunft()
for t in z:
        print(t)
