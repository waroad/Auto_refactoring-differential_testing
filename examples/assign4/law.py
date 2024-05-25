def bar1(a, b, c, d):
    if a <= b and c > d:
        print(1)
        return a
    elif a > b and c == d:
        print(2)
        return b
    elif a == b or c == d:
        print(3)
        return c
    else:
        print(4)
        return d

def bar2(a, b, c):
    if (a > b) | (b == c):
        return a
    if (a == c) & (b != c):
        return b
    if (a < b) & (b < c) | (a == c):
        return c
    return a + b