#!/usr/bin/env python
# -*- coding: utf-8 -*-
import turtle
import canvasvg

def triangle(length, threshold):
    if length < threshold:
        return
    else:
        for i in range(3):
            turtle.forward(length)
            triangle(length/2, threshold)
            turtle.backward(length)
            turtle.left(120)


if __name__ == "__main__":
    turtle.clearscreen()
    turtle.speed(0)
    triangle(100, 1)
    turtle.hideturtle()
    ts = turtle.getscreen().getcanvas()
    canvasvg.saveall("triangle.svg", ts)
