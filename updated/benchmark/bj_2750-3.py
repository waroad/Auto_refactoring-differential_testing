(b, a) = ([], int(input()))
b += [int(input()) for i in range(a)]
b.sort()
for i in range(a):
    print(b[i])