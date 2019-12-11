#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from triangle import triangle

class TestTriangle(unittest.TestCase):
    def test_triangle1(self):
        self.assertEqual(triangle(0, 0, 0), "错误")
    def test_triangle2(self):
        self.assertEqual(triangle(1, 1, 1), "等边")
    def test_triangle3(self):
        self.assertEqual(triangle(1, 3, 2), "错误")

if __name__ == "__main__":
    unittest.main()
