#!/usr/bin/python3

def foo(a, b, x):
    if a > 1 and b == 0:
        x = x / a
    else:
        x = x * a
    if a == 2 or x > 1:
        x = x + 1

if __name__ == "__main__":
    foo(0, 0, 4)
