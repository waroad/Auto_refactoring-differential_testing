list_1 = []
list_2 = ["ha", "haha"]
dict_1={}
set_1=set()
temp=2
for j in range(10):
    dict_1[str(j)]=j
    set_1.add(j)
    list_1.append(j*temp)

print(list_1, "sum:",sum(list_1))
print(dict_1)
print(set_1, "sum:",sum(set_1))

# 변환 후
# 
# list_1 = []
# list_2 = ['ha', 'haha']
# dict_1 = {}
# set_1 = set()
# temp = 2
# temp_dict_1 = {str(j): j for j in range(10)}
# dict_1.update(temp_dict_1)
# set_1 |= {j for j in range(10)}
# list_1 += [j * temp for j in range(10)]
# print(list_1, 'sum:', sum(list_1))
# print(dict_1)
# print(set_1, 'sum:', sum(set_1))
