#!/usr/bin/python3

import requests, bs4, sqlite3

url = "https://bugs.debian.org/release-critical/debian/all.html"
req = requests.get(url)

soup = bs4.BeautifulSoup(req.text)
content = soup.find(attrs={"id": "content"})


con = sqlite3.connect("rcbugs.db")
cursor = con.cursor()
cursor.execute("create table rcbugs (id integer primary key, package text, maintainer text, bugs text)")

for pkg in content.find_all(class_="package"):
    alist = pkg.find_all(attrs={"href": True})
    assert len(alist) >= 3
    print("%s\n%s\n%s" % (alist[0].text, alist[1].text, alist[2].text))
    atexts = [x.text for x in alist]
    #atexts[0], atexts[1], ";".join(atexts[2:])
    package = atexts[0]
    maintainer = atexts[1]
    bugs = ";".join(atexts[2:])
    cursor.execute("insert into rcbugs (package, maintainer, bugs) values (?, ?, ?)", (package, maintainer, bugs))

con.commit()
con.close()


