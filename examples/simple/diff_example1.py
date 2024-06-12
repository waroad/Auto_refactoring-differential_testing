def main():
    list_1 = []
    list_2 = ["ha", "haha"]
    dict_1={}
    set_1=set()
    for i in range(100000):
        list_1.append(i)
        dict_1[str(i)]=i
        set_1.add(i)
    return list_1, list_2, dict_1, set_1