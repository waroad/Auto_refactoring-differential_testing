#  https://www.acmicpc.net/source/79280739
from collections import deque
import sys
input = sys.stdin.readline
# ----------------------------------------------------------------
n = int(input())
d = deque()
for _ in range(n):
    d.append(int(input()))


# ----------------------------------------------------------------
count = 1
standard = d.pop()
for i in range(n-1):
    see = d.pop()
    if see > standard:
        count += 1
        standard = see

# ----------------------------------------------------------------
print(count)