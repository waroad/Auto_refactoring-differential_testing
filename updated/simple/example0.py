(list_1, list_2, temp) = ([], [], 14)
list_2.append(3)
for i in range(12):
    list_2.append(i * temp)
    list_1.append(i)
    print('hi')
    temp += 1
list_2.append(3)
list_1 += [i for i in range(4)]
print(list_1)
list1 = []
list1 += [i for i in range(5)]
list_2 += [5 for i in range(5)]
list1 += [i * i for i in range(3)]
print(list_1, list1, list_2)
list3 = []
list3 += [j + temp for j in range(4)]