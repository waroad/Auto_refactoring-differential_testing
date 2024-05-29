def main(l1, l2):
    list1 = [""] + l1
    list2 = [""] + l2

    res = [[""] * len(list2) for _ in range(len(list1))]

    for i in range(1, len(list1)):
        for j in range(1, len(list2)):
            if list1[i] == list2[j]:
                res[i][j] = res[i-1][j-1] + list1[i]
            else:
                if len(res[i-1][j]) >= len(res[i][j-1]):
                    res[i][j] = res[i-1][j]
                else:
                    res[i][j] = res[i][j-1]

    result = res[-1][-1]
    print(len(result), result, sep="\n")