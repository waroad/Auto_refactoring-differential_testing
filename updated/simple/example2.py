a, b, c, d = (2, 3, 5, 7)
if a <= b <= c:
    print('changed')
elif a < b < c:
    print('changed')
elif a > b < c:
    print('not changed')
else:
    print('changed' if b >= c >= d else 'ignore')