# Truth Value Test
A, B = (1, 2), [1, 2]
if A==[]:
    print(1)
elif B!=():
    print(2)

# changed
A, B = ((1, 2), [1, 2])
if not A:
    print(1)
elif B:
    print(2)