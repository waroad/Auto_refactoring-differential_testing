def main(N, list1):
    (a, b) = (0, 0)
    if N == 1:
        print('A')
    elif N == 2:
        print(list1[1] if list1[1] == list1[0] else 'A')
    else:
        a = 0 if not list1[0] - list1[1] else (list1[1] - list1[2]) // (list1[0] - list1[1])
        b = list1[1] - a * list1[0]
        real = True
        for i in range(N):
            if list1[i] * a + b != list1[i + 1]:
                real = False
                break
        print(a * list1[-1] + b if real else 'B')