import importlib.util
ori_module_spec = importlib.util.spec_from_file_location('ori_module', '.\\examples\\simple\\diff_example11.py')
test_module_spec = importlib.util.spec_from_file_location('test_module', '.\\updated\\simple\\diff_example11.py')
ori_module = importlib.util.module_from_spec(ori_module_spec)
test_module = importlib.util.module_from_spec(test_module_spec)
ori_module_spec.loader.exec_module(ori_module)
test_module_spec.loader.exec_module(test_module)

def test_lst_append():
    assert ori_module.lst_append() == test_module.lst_append()
def test_lst_append():
    assert ori_module.lst_append() == test_module.lst_append()
def test_lst_append():
    assert ori_module.lst_append() == test_module.lst_append()
def test_lst_append():
    assert ori_module.lst_append() == test_module.lst_append()
def test_lst_append():
    assert ori_module.lst_append() == test_module.lst_append()
def test_lst_append():
    assert ori_module.lst_append() == test_module.lst_append()
def test_lst_append():
    assert ori_module.lst_append() == test_module.lst_append()
def test_lst_append():
    assert ori_module.lst_append() == test_module.lst_append()
