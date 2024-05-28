def if_expression(a, b, c, d):
    if a <= b and b <= c:
        return "changed"
    elif b > a and c > b:
        return "changed"
    elif b < a and b < c:
        return "not changed"
    elif b >= c and d <= c:
        return "changed"
    else:
        return "ignore"