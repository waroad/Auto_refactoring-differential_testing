# NestedIf
A, B, C = 1, 2, 3
if A:
    if B:
        if C:
            print(2)

# changed
# A, B, C = 1, 2, 3
# if A and B and C:
#     print(2)