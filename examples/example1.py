list_1 = []
dict_1={}
set_1=set()
for i in range(10):
    list_1.append(i)
    dict_1[str(i)]=i
    set_1.add(i)

print(list_1, "sum:",sum(list_1))
print(dict_1)
print(set_1, "sum:",sum(set_1))