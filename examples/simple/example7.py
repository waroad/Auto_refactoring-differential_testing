# IfExp
A=[1, 2]
if A:
    x=1
else:
    x=2
if A:
    print(1)
else:
    print(2)

# changed
A = [1, 2]
x = 1 if A else 2
print(1 if A else 2)