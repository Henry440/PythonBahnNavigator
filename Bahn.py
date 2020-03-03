import json
import requests

def station_search():
    search = raw_input("Suche : ")
    search = str(search)
    #url = "https://marudor.de/api/hafas/v1/station/" + search
    url = "https://marudor.de/api/station/v1/search/" + search

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

    auswahl = int(raw_input("Station Waehlen : "))
    auswahl = auswahl - 1
    print(stations[auswahl])
    return auswahl

def abfahrten(eva):
    url = "https://marudor.de/api/iris/v1/abfahrten/" + eva
    print(eva)
    param = dict()
    resp = requests.get(url = url, params=param)
    data = resp.json()
    fahrten = data["departures"]
    for x in fahrten:
        try:
            print(x["arrival"])
        except Exception:
            print(x)

data = station_search()
auswahl = selectStation(data)
auswahl = int(auswahl)
abfahrten(data[1][auswahl])
