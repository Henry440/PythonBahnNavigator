import json
import requests

search = input("Suche : ")

url = "https://marudor.de/api/hafas/v1/station/" + search
param = dict()

resp = requests.get(url=url, params=param)
data = resp.json()

count = 0
for x in data:
    count = count + 1

for x in range(count):
    print(data[x]["id"] + " - " + data[x]["title"])
