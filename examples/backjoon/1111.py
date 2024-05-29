def main(N, list1):
    a = 0
    b = 0
    if N == 1:
        print("A")
    elif N == 2:
        if list1[1] == list1[0]:
            print(list1[1])
        else:
            print("A")
    else:
        if (list1[0] - list1[1] == 0):
            a = 0
        else:
            a = (list1[1] - list1[2]) // (list1[0] - list1[1])
        b = list1[1] - a * list1[0]
        real = True
        for i in range(N):
            if list1[i] * a + b != list1[i+1]:
                real = False
                break
        if real:
            print(a * list1[-1] + b)
        else:
            print("B")