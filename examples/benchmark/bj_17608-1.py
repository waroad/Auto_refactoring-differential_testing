# https://www.acmicpc.net/source/79493123

import sys

input = sys.stdin.readline
stk, cnt, = [], 1
N = int(input())
for _ in range(N):
    stk.append(int(input()))
last = stk[-1]

for i in reversed(range(N)):
    if stk[i] > last :
        cnt +=1
        last = stk[i]
print(cnt)
