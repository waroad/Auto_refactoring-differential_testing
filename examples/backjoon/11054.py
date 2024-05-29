def main(N, list1):
    reversed_list = list1[::-1]
    increasing = [1 for _ in range(N)]
    decreasing = [1 for _ in range(N)]
    for i in range(N):
        for j in range(i):
            if list1[i] > list1[j]:
                increasing[i] = max(increasing[i], increasing[j] + 1)
    for i in range(N):
        for j in range(i):
            if reversed_list[i] > reversed_list[j]:
                decreasing[i] = max(decreasing[i], decreasing[j] + 1)

    res = []

    for i in range(len(increasing)):
        res.append(increasing[i] + decreasing[N-i-1])
    print(max(res) - 1)