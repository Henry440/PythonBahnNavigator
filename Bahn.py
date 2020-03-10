import json
import requests
import sys
from datetime import datetime
from time import sleep

import ZugDaten as train

def station_search():
    search = ""
    try:
        search = raw_input("Stationssuche : ") #Fehler Bei Windows
    except Exception:
        search = input("Stationssuche : ")
    search = str(search)
    #url = "https://marudor.de/api/hafas/v1/station/" + search
    url = "https://marudor.de/api/station/v1/search/" + search
    print(url)
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

def monitoring():
    stationen = station_search()
    auswahl = int(selectStation(stationen))
    delay = 0
    zyklen = 0
    try:
        delay = raw_input("Monitoring Warten [Minuten] : ")
        zyklen = raw_input("Monitoring Zyklen : ")
    except Exception:
        delay = input("Monitoring Warten [Minuten] : ")
        zyklen = raw_input("Monitoring Zyklen : ")

    for i in range(1, int(zyklen)):
        daten = bahnhofsdaten(stationen[1][auswahl])
        current = daten["departures"]
        for line in current:

            zug = line["train"]["name"]
            von = line["route"][0]["name"]
            nach = line["destination"]
            try:
                an = line["arrival"]["time"]
            except Exception as e:
                an = "N.A."
            ab = line["departure"]["time"]
            try:
                delayAn = line["arrival"]["delay"]
            except Exception as e:
                delayAn = "N.A."
            try:
                delayAb = line["departure"]["delay"]
            except Exception as e:
                delayAb = "N.A."
            gleisPlan = line["arrival"]["scheduledPlatform"]
            gleis = line["arrival"]["platform"]
            try:
                ausfallAn = line["arrival"]["cancelled"]
            except Exception as e:
                ausfallAn = "N.A."
            try:
                ausfallAb = line["departure"]["cancelled"]
            except Exception as e:
                ausfallAb = "N.A."

            print(zug + " | " + von + " --> " + nach + " | An : " + str(timestamp_to_time(an)) + " Ab : " + str(timestamp_to_time(ab)) + " | Gleis : " + gleis + " | Delay : " + str(delayAn))

        print("---Log : " + str(i) + "-------------------------------------------------")
        sleep(int(delay) * 60)


    #departure
def printAbfahrt(datas):
    fahrten = datas["departures"]
    for x in fahrten:
        try:
            zug = x["train"]["name"]
            if(x["departure"]["cancelled"] == False):
                print(zug + "\t nach : " + x["destination"] + "\t Abfahrt : " + timestamp_to_time(x["departure"]["time"]))
            else:
                print(zug + " Faellt aus !")
        except Exception as Zugdatene:
            pass

def printAnkunft(datas):
    fahrten = datas["departures"]
    for x in fahrten:
        try:
            zug = x["train"]["name"]
            if(x["arrival"]["cancelled"] == False):
                print(zug + "\t nach : " + x["destination"] + "\t Ankunft : " + timestamp_to_time(x["arrival"]["time"]))
            else:
                print(zug + " Faellt aus !")
        except Exception as Zugdatene:
            pass

def printDelay(datas):
    fahrten = datas["departures"]
    for x in fahrten:
        try:
            zug = x["train"]["name"]
            if(x["arrival"]["cancelled"] == False):
                print(zug + "\t nach : " + x["destination"] + "\t Ankunft Verspaetung : " + str(x["arrival"]["delay"]) + "\tAbfahrt Verspaetung : " + str(x["departure"]["delay"]) )
            else:
                print(zug + " Faellt aus !")
        except Exception as e:
            pass


def bahnhofsdaten(eva):
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

while True:
    print("Auswahl : ")
    print("Ankuenfte [1] | Abfahrten [2] | Verspaetung [3]")
    print("Monitoring [4]")
    print("Beenden [99]")

    choice = 1
    try:
        choice = int(raw_input("Auswahl : "))
    except Exception:
        choice = int(input("Auswahl : "))

    if(choice <= 3):
        data = station_search()                         #Inhalt alle Stationen der Suchanfrage (Station[], EvaID[])
        auswahl = int(selectStation(data))              #Integer fuer Stationsauswahl
        zugdaten = bahnhofsdaten(data[1][auswahl])      #Liefert alle Bahnhofsdaten fuer die gewaehlte Station JSON  Alles
        workdata = train.Zug(zugdaten)                  #Schreibt daten in Ein Objekt fuer leichteres Arbeiten

        if(choice == 1):
            printAnkunft(zugdaten)
        elif(choice == 2):
            printAbfahrt(zugdaten)
        elif(choice == 3):
            printDelay(zugdaten)
        else:
            print("Fehler ungueltige Aktion")
            sys.exit()
    elif(choice == 4):
        monitoring();
    elif(choice == 99):
        print("Beende")
        sys.exit()
    else:
        print("Fehlerhafte eingabe !")
        continue
