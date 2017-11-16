#!/usr/bin/python3

import turtle
import canvasvg

def tree(len, n):
    if n <= 0:
        return
    else:
        turtle.forward(len)
        turtle.left(45)
        tree(len * 0.5, n - 1)
        turtle.right(90)
        tree(len * 0.5, n - 1)
        turtle.left(45)
        turtle.backward(len)

turtle.speed(0)
tree(200, 9)
turtle.hideturtle()
ts = turtle.getscreen().getcanvas()
canvasvg.saveall("tree.svg", ts)
