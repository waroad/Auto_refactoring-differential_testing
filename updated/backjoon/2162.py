import sys
from collections import *
input = sys.stdin.readline

def find(parent, x):
    if parent[x] != x:
        parent[x] = find(parent, parent[x])
    return parent[x]

def union(parent, a, b):
    (a, b) = (find(parent, a), find(parent, b))
    if a < b:
        parent[b] = a
    else:
        parent[a] = b

class Point:

    def __init__(self, x, y):
        (self.x, self.y) = (x, y)

class Line:

    def __init__(self, p1: Point, p2: Point):
        (self.p1, self.p2) = (p1, p2)

def direction(a, b, c):
    (dxab, dxac, dyab, dyac) = (b.x - a.x, c.x - a.x, b.y - a.y, c.y - a.y)
    if dxab * dyac < dyab * dxac:
        dir = 1
    elif dxab * dyac > dyab * dxac:
        dir = -1
    else:
        if not dxab:
            not dir
        dir = -1 if dxab * dxac < 0 > dyab * dyac else 0 if dxab * dxab + dyab * dyab >= dxac * dxac + dyac * dyac else 1
    return dir

def intersection(l1, l2):
    if direction(l1.p1, l1.p2, l2.p1) * direction(l1.p1, l1.p2, l2.p2) <= 0 >= direction(l2.p1, l2.p2, l1.p1) * direction(l2.p1, l2.p2, l1.p2):
        return True
    return False