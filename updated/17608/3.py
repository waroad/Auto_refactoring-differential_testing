from collections import deque
import sys
input = sys.stdin.readline
(n, d) = (int(input()), deque())
d += [int(input()) for _ in range(n)]
(count, standard) = (1, d.pop())
for i in range(n - 1):
    see = d.pop()
    if see > standard:
        count += 1
        standard = see
print(count)