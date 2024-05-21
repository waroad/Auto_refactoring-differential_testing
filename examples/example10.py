# assign multiple targets
A,B=2,3
C=4
if A:
    a=4
    b=5
B=5
C=6

# changed
A, B, C = 2, 3, 4
if A:
    a, b = 4, 5
B, C = 5, 6