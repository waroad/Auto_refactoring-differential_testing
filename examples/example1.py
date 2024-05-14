list_1 = []
list_2 = ["ha", "haha"]
dict_1={}
set_1=set()
temp=14
for j in range(9):
    dict_1[str(j)]=j
for k in range(8):
    set_1.add(k)
    list_1.append(k*temp)
    dict_1["kk"]=10
    print("h")
for i in range(12):
    list_2.append(i*temp)

print(list_1, "sum:",sum(list_1))
print(dict_1)
print(set_1, "sum:",sum(set_1))
