(x, num_list) = (int(input()), [])
num_list += [int(input()) for i in range(x)]
num_list1 = sorted(num_list)
for (i, item) in enumerate(num_list):
    print(num_list1[i])