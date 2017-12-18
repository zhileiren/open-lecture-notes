#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest
import requests
import bs4

class TestSpider(unittest.TestCase):
    def testRequests(self):
        url = "http://oscar-lab.org/puzzle.html"
        req = requests.get(url)
        self.assertEqual(req.status_code, 200)

    def testBs4(self):
        url = "http://oscar-lab.org/puzzle.html"
        req = requests.get(url)
        soup = bs4.BeautifulSoup(req.text)
        self.assertIsNotNone(soup.table)

if __name__ == "__main__":
    unittest.main()
        

