def if_expression(a, b, c, d):
    if a <= b <= c:
        return "changed"
    elif a < b < c:
        return "changed"
    elif b < a and b < c:
        return "not changed"
    elif b >= c >= d:
        return "changed"
    else:
        return "ignore"