#!/usr/bin/python3

import requests
import bs4
import sys

def tree(node, prefix, last):
    if not isinstance(node, bs4.element.Tag):
        pass
    else:
        print(prefix +  last + node.name)
        children = [c for c in node.children if isinstance(c, bs4.element.Tag)]
        if children:
            for child in children[:-1]:
                tree(child, prefix + ' |', '--')
            tree(children[-1], prefix + '  ', '`-')

if __name__ == "__main__":
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = "http://oscar-lab.org/people/~zren/crawlme.html"
    res = requests.get(url)
    res.encoding = res.apparent_encoding
    doc = bs4.BeautifulSoup(res.text)
    tree(doc, "", "")
    print(doc.prettify())
