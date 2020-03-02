import json
import requests

def station_search():
    search = input("Suche : ")
    url = "https://marudor.de/api/hafas/v1/station/" + search
    param = dict()
    resp = requests.get(url=url, params=param)
    data = resp.json()

    stations = [""]
    evaID = [""]

    count = 0
    for x in data:
        count = count + 1
    for x in range(count):
        print(data[x]["id"] + " - " + data[x]["title"])
        stations.append(data[x]["title"])
        evaID.append(data[x]["id"])
    return (stations, evaID)

station = station_search()
print(station[0][0])
