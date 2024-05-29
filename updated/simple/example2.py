(a, b, c, d, e) = (2, 3, 5, 7, 1)
if a <= b <= c:
    print('changed')
elif c > b > a:
    print('changed')
elif a > b < c:
    print('not changed')
else:
    print('changed' if (e > c and a > b >= c >= d or d > e > 10) and c > 1 > 0 else 'ignore')