# https://www.acmicpc.net/source/79532435
n = int(input())
arr = []
for _ in range(n):
    arr.append(int(input()))

arr.sort()

for i  in arr:
    print(i)