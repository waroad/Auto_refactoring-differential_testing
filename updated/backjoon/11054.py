def main(N, list1):
    (reversed_list, increasing, decreasing) = (list1[::-1], [1 for _ in range(N)], [1 for _ in range(N)])
    for i in range(N):
        for j in range(i):
            if list1[i] > list1[j]:
                increasing[i] = max(increasing[i], increasing[j] + 1)
    for i in range(N):
        for j in range(i):
            if reversed_list[i] > reversed_list[j]:
                decreasing[i] = max(decreasing[i], decreasing[j] + 1)
    res = []
    res += [item + decreasing[N - i - 1] for (i, item) in enumerate(increasing)]
    print(max(res) - 1)