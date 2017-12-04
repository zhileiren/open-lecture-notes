#!/usr/bin/python3

import requests, re, bs4
import subprocess
import glob

prefix = "https://lkml.org"
seed = "%s/lkml/last100/" % prefix

req = requests.get(seed)

soup = bs4.BeautifulSoup(req.text, "lxml")
interested = soup.find_all(class_="mh")
assert(len(interested)) == 1

hrefid = 0
for tr in interested[0].find_all("tr"):
    class_ = tr.get("class")
    if class_ == None or ("c0" not in class_ and "c1" not in class_):
        continue
    tds = tr.find_all('td')
    assert(len(tds) == 3)
    href = tds[1].a['href']
    target = "%d.html" % hrefid
    #subprocess.call(['wget', "%s/%s" % (prefix, href), "-O", target])
    tds[1].a['href'] = target
    tds[2].a['href'] = target
    hrefid += 1

#modify css location
css = soup.find(href=r'/css/message.css')
assert(css != None)
css['href'] = "." + css['href']


handle = open("index.html", "w")
handle.write(soup.prettify())
handle.close()

for html in glob.glob("*.html"):
    handle = open(html)
    soup = bs4.BeautifulSoup(handle.read())
    for script in soup.find_all("script"):
        script.decompose()
    handle.close()
    handle = open(html, "w")
    handle.write(soup.prettify())
    handle.close()
