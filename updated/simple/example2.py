a, b, c, d, e = (2, 3, 5, 7, 1)
print('changed' if a <= b <= c else 'changed' if c > b > a else 'not changed' if a > b < c else 'changed' if (e > c and a > b >= c >= d or d > e > 10) and c > 1 > 0 else 'ignore')