#!/usr/bin/python3

import unittest
from secondLargest import secondLargest

class TestSecondLargest(unittest.TestCase):
    def test_1(self):
        self.assertIsNone(secondLargest([]))
    def test_2(self):
        self.assertIsNone(secondLargest([1]))
    def test_3(self):
        self.assertEqual(secondLargest([1,2]), 1)

