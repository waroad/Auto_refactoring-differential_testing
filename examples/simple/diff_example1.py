import time
start_time = time.time()

list_1 = []
list_2 = ["ha", "haha"]
dict_1={}
set_1=set()
for i in range(100000):
    list_1.append(i)
    dict_1[str(i)]=i
    set_1.add(i)

print(list_1, "sum:",sum(list_1))
print(dict_1)
print(set_1, "sum:",sum(set_1))
end_time = time.time()

elapsed_time = end_time - start_time
print(f"Total execution time: {elapsed_time} seconds")