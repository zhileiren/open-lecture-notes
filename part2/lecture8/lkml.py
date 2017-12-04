#!/usr/bin/python3

import requests, re, bs4
import subprocess

seed = "https://lkml.org/lkml/last100/"

req = requests.get(seed)

soup = bs4.BeautifulSoup(req.text, "lxml")
interested = soup.find_all(class_="mh")
assert(len(interested)) == 1

for tr in interested[0].find_all("tr"):
    class_ = tr.get("class")
    if class_ == None or ("c0" not in class_ and "c0" not in class_):
        continue
    print(tr.text)
    tds = tr.find_all('td')
    print(len(tds))
    assert(len(tds) == 3)
    print(tds[1].a.get("href"))

print(soup.prettify())




