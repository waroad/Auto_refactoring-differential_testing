import sys
(input, (stk, cnt)) = (sys.stdin.readline, ([], 1))
N = int(input())
stk += [int(input()) for _ in range(N)]
last = stk[-1]
for i in reversed(range(N)):
    if stk[i] > last:
        cnt += 1
        last = stk[i]
print(cnt)