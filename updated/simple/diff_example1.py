def main():
    (list_1, list_2, dict_1, set_1) = ([], ['ha', 'haha'], {}, set())
    list_1 += [i for i in range(100000)]
    (dict_1, set_1) = ({str(i): i for i in range(100000)}, {i for i in range(100000)})
    return list_1, list_2, dict_1, set_1