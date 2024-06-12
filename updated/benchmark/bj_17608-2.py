(N, arr) = (int(input()), [])
arr += [int(input()) for _ in range(N)]
(finish, max_height, result) = (max(arr), 0, 0)
while arr:
    height = arr.pop()
    if height > max_height:
        result += 1
        max_height = height
    if height == finish:
        break
print(result)