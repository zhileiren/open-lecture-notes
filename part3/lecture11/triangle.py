#!/usr/bin/python3
# coding: utf-8

def triangle(a, b, c):
    # a, b, c = sorted([a, b, c])
    if a + b <= c:
        return "错误"
    triangle_type = ""
    if a == b == c:
        triangle_type = "等边"
    elif a == b or b == c or a == c:
        triangle_type = "等腰"
    else:
        triangle_type = "一般"

    if a ** 2 + b ** 2 == c ** 2:
        triangle_type += "直角"
    return triangle_type

if __name__ == "__main__":
    print(triangle(1, 1, 1))
    print(triangle(1, 2, 3))
    print(triangle(3, 3, 3))
    print(triangle(3, 4, 5))
