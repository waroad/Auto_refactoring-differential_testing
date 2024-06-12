# https://www.acmicpc.net/source/23719790
b=[]; a=int(input())
for i in range(a): b.append(int(input()))
b.sort()
for i in range(a): print(b[i])