# https://www.acmicpc.net/source/79341931

N = int(input())
arr = []

for _ in range(N):
    arr.append(int(input()))

finish = max(arr)
max_height = 0
result = 0
while arr:
    height = arr.pop()

    if height > max_height:
        result += 1
        max_height = height
    if height == finish:
        break

print(result)