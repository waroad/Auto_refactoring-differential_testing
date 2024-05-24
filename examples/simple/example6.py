# NestedIf
A, B = [1, 2], (1, 2)
if A:
    if B:
        print(2)

# changed
A, B = ([1, 2], (1, 2))
if A and B:
    print(2)