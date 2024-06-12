(n, arr) = (int(input()), [])
arr += [int(input()) for _ in range(n)]
arr.sort()
for i in arr:
    print(i)