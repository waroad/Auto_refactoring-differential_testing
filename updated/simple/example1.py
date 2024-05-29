import time
(start_time, list_1, list_2, dict_1, set_1) = (time.time(), [], ['ha', 'haha'], {}, set())
list_1 += [i for i in range(100000)]
temp_dict_1 = {str(i): i for i in range(100000)}
dict_1.update(temp_dict_1)
set_1 |= {i for i in range(100000)}
print(list_1, 'sum:', sum(list_1))
print(dict_1)
print(set_1, 'sum:', sum(set_1))
end_time = time.time()
elapsed_time = end_time - start_time
print(f'Total execution time: {elapsed_time} seconds')