#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import turtle
import canvasvg

def curve(length, threshold):
    if length < threshold:
        turtle.forward(length)
        turtle.right(90)
        turtle.forward(length/2)
        turtle.right(90)
        turtle.forward(length)
        turtle.left(90)
        turtle.forward(length/2)
        turtle.left(90)
        turtle.forward(length)
    else:
        length = length / 3
        curve(length, threshold)
        turtle.left(90)
        for i in range(4):
            curve(length, threshold)
            turtle.right(90)
        turtle.right(180)
        for i in range(3):
            curve(length, threshold)
            turtle.left(90)
        turtle.left(180)
        curve(length, threshold)



length = 500
for i in range(4):
    turtle.forward(length)
    turtle.right(90)
curve(500, 30)
turtle.hideturtle()
ts = turtle.getscreen().getcanvas()
canvasvg.saveall("curve.svg", ts)
