import importlib.util
ori_module_spec = importlib.util.spec_from_file_location('ori_module', '.\\examples\\assign4\\lazy.py')
test_module_spec = importlib.util.spec_from_file_location('test_module', '.\\updated\\assign4\\lazy.py')
ori_module = importlib.util.module_from_spec(ori_module_spec)
test_module = importlib.util.module_from_spec(test_module_spec)
ori_module_spec.loader.exec_module(ori_module)
test_module_spec.loader.exec_module(test_module)

def test_sort1():
    assert ori_module.sort1(None) == test_module.sort1(None)
def test_sort2():
    assert ori_module.sort2(None) == test_module.sort2(None)
    assert ori_module.sort2(None) == test_module.sort2(None)
def test_get_pivot():
    assert ori_module.get_pivot(None, None, None) == test_module.get_pivot(None, None, None)
    assert ori_module.get_pivot(None, None, None) == test_module.get_pivot(None, None, None)
    assert ori_module.get_pivot(None, None, None) == test_module.get_pivot(None, None, None)
def test_help_sort3():
    assert ori_module.help_sort3(None, None, None) == test_module.help_sort3(None, None, None)
    assert ori_module.help_sort3(None, None, None) == test_module.help_sort3(None, None, None)
    assert ori_module.help_sort3(None, None, None) == test_module.help_sort3(None, None, None)
    assert ori_module.help_sort3(None, None, None) == test_module.help_sort3(None, None, None)
def test_sort3():
    assert ori_module.sort3(None) == test_module.sort3(None)
    assert ori_module.sort3(None) == test_module.sort3(None)
    assert ori_module.sort3(None) == test_module.sort3(None)
    assert ori_module.sort3(None) == test_module.sort3(None)
    assert ori_module.sort3(None) == test_module.sort3(None)
def test_sort1():
    assert ori_module.sort1(None) == test_module.sort1(None)
def test_sort2():
    assert ori_module.sort2(None) == test_module.sort2(None)
    assert ori_module.sort2(None) == test_module.sort2(None)
def test_get_pivot():
    assert ori_module.get_pivot(None, None, None) == test_module.get_pivot(None, None, None)
    assert ori_module.get_pivot(None, None, None) == test_module.get_pivot(None, None, None)
    assert ori_module.get_pivot(None, None, None) == test_module.get_pivot(None, None, None)
def test_help_sort3():
    assert ori_module.help_sort3(None, None, None) == test_module.help_sort3(None, None, None)
    assert ori_module.help_sort3(None, None, None) == test_module.help_sort3(None, None, None)
    assert ori_module.help_sort3(None, None, None) == test_module.help_sort3(None, None, None)
    assert ori_module.help_sort3(None, None, None) == test_module.help_sort3(None, None, None)
def test_sort3():
    assert ori_module.sort3(None) == test_module.sort3(None)
    assert ori_module.sort3(None) == test_module.sort3(None)
    assert ori_module.sort3(None) == test_module.sort3(None)
    assert ori_module.sort3(None) == test_module.sort3(None)
    assert ori_module.sort3(None) == test_module.sort3(None)
def test_sort1():
    assert ori_module.sort1(None) == test_module.sort1(None)
def test_sort2():
    assert ori_module.sort2(None) == test_module.sort2(None)
    assert ori_module.sort2(None) == test_module.sort2(None)
def test_get_pivot():
    assert ori_module.get_pivot(None, None, None) == test_module.get_pivot(None, None, None)
    assert ori_module.get_pivot(None, None, None) == test_module.get_pivot(None, None, None)
    assert ori_module.get_pivot(None, None, None) == test_module.get_pivot(None, None, None)
def test_help_sort3():
    assert ori_module.help_sort3(None, None, None) == test_module.help_sort3(None, None, None)
    assert ori_module.help_sort3(None, None, None) == test_module.help_sort3(None, None, None)
    assert ori_module.help_sort3(None, None, None) == test_module.help_sort3(None, None, None)
    assert ori_module.help_sort3(None, None, None) == test_module.help_sort3(None, None, None)
def test_sort3():
    assert ori_module.sort3(None) == test_module.sort3(None)
    assert ori_module.sort3(None) == test_module.sort3(None)
    assert ori_module.sort3(None) == test_module.sort3(None)
    assert ori_module.sort3(None) == test_module.sort3(None)
    assert ori_module.sort3(None) == test_module.sort3(None)
def test_sort1():
    assert ori_module.sort1(None) == test_module.sort1(None)
def test_sort2():
    assert ori_module.sort2(None) == test_module.sort2(None)
    assert ori_module.sort2(None) == test_module.sort2(None)
def test_get_pivot():
    assert ori_module.get_pivot(None, None, None) == test_module.get_pivot(None, None, None)
    assert ori_module.get_pivot(None, None, None) == test_module.get_pivot(None, None, None)
    assert ori_module.get_pivot(None, None, None) == test_module.get_pivot(None, None, None)
def test_help_sort3():
    assert ori_module.help_sort3(None, None, None) == test_module.help_sort3(None, None, None)
    assert ori_module.help_sort3(None, None, None) == test_module.help_sort3(None, None, None)
    assert ori_module.help_sort3(None, None, None) == test_module.help_sort3(None, None, None)
    assert ori_module.help_sort3(None, None, None) == test_module.help_sort3(None, None, None)
def test_sort3():
    assert ori_module.sort3(None) == test_module.sort3(None)
    assert ori_module.sort3(None) == test_module.sort3(None)
    assert ori_module.sort3(None) == test_module.sort3(None)
    assert ori_module.sort3(None) == test_module.sort3(None)
    assert ori_module.sort3(None) == test_module.sort3(None)
def test_sort1():
    assert ori_module.sort1(None) == test_module.sort1(None)
def test_sort2():
    assert ori_module.sort2(None) == test_module.sort2(None)
    assert ori_module.sort2(None) == test_module.sort2(None)
def test_get_pivot():
    assert ori_module.get_pivot(None, None, None) == test_module.get_pivot(None, None, None)
    assert ori_module.get_pivot(None, None, None) == test_module.get_pivot(None, None, None)
    assert ori_module.get_pivot(None, None, None) == test_module.get_pivot(None, None, None)
def test_help_sort3():
    assert ori_module.help_sort3(None, None, None) == test_module.help_sort3(None, None, None)
    assert ori_module.help_sort3(None, None, None) == test_module.help_sort3(None, None, None)
    assert ori_module.help_sort3(None, None, None) == test_module.help_sort3(None, None, None)
    assert ori_module.help_sort3(None, 0, 1) == test_module.help_sort3(None, 0, 1)
    assert ori_module.help_sort3(None, 0, 0) == test_module.help_sort3(None, 0, 0)
def test_sort3():
    assert ori_module.sort3(None) == test_module.sort3(None)
    assert ori_module.sort3(None) == test_module.sort3(None)
    assert ori_module.sort3(None) == test_module.sort3(None)
    assert ori_module.sort3(None) == test_module.sort3(None)
    assert ori_module.sort3(None) == test_module.sort3(None)
    assert ori_module.sort3(None) == test_module.sort3(None)
def test_sort1():
    assert ori_module.sort1(None) == test_module.sort1(None)
def test_sort2():
    assert ori_module.sort2(None) == test_module.sort2(None)
    assert ori_module.sort2(None) == test_module.sort2(None)
def test_get_pivot():
    assert ori_module.get_pivot(None, None, None) == test_module.get_pivot(None, None, None)
    assert ori_module.get_pivot(None, None, None) == test_module.get_pivot(None, None, None)
    assert ori_module.get_pivot(None, None, None) == test_module.get_pivot(None, None, None)
def test_help_sort3():
    assert ori_module.help_sort3(None, None, None) == test_module.help_sort3(None, None, None)
    assert ori_module.help_sort3(None, None, None) == test_module.help_sort3(None, None, None)
    assert ori_module.help_sort3(None, None, None) == test_module.help_sort3(None, None, None)
    assert ori_module.help_sort3(None, 0, 1) == test_module.help_sort3(None, 0, 1)
    assert ori_module.help_sort3(None, 0, 0) == test_module.help_sort3(None, 0, 0)
def test_sort3():
    assert ori_module.sort3(None) == test_module.sort3(None)
    assert ori_module.sort3(None) == test_module.sort3(None)
    assert ori_module.sort3(None) == test_module.sort3(None)
    assert ori_module.sort3(None) == test_module.sort3(None)
    assert ori_module.sort3(None) == test_module.sort3(None)
    assert ori_module.sort3(None) == test_module.sort3(None)
def test_sort1():
    assert ori_module.sort1(None) == test_module.sort1(None)
def test_sort2():
    assert ori_module.sort2(None) == test_module.sort2(None)
    assert ori_module.sort2(None) == test_module.sort2(None)
def test_get_pivot():
    assert ori_module.get_pivot(None, None, None) == test_module.get_pivot(None, None, None)
    assert ori_module.get_pivot(None, None, None) == test_module.get_pivot(None, None, None)
    assert ori_module.get_pivot(None, None, None) == test_module.get_pivot(None, None, None)
def test_help_sort3():
    assert ori_module.help_sort3(None, None, None) == test_module.help_sort3(None, None, None)
    assert ori_module.help_sort3(None, None, None) == test_module.help_sort3(None, None, None)
    assert ori_module.help_sort3(None, None, None) == test_module.help_sort3(None, None, None)
    assert ori_module.help_sort3(None, 0, 1) == test_module.help_sort3(None, 0, 1)
    assert ori_module.help_sort3(None, 0, 0) == test_module.help_sort3(None, 0, 0)
def test_sort3():
    assert ori_module.sort3(None) == test_module.sort3(None)
    assert ori_module.sort3(None) == test_module.sort3(None)
    assert ori_module.sort3(None) == test_module.sort3(None)
    assert ori_module.sort3(None) == test_module.sort3(None)
    assert ori_module.sort3(None) == test_module.sort3(None)
    assert ori_module.sort3(None) == test_module.sort3(None)
def test_sort1():
    assert ori_module.sort1(None) == test_module.sort1(None)
def test_sort2():
    assert ori_module.sort2(None) == test_module.sort2(None)
    assert ori_module.sort2(None) == test_module.sort2(None)
def test_get_pivot():
    assert ori_module.get_pivot(None, None, None) == test_module.get_pivot(None, None, None)
    assert ori_module.get_pivot(None, None, None) == test_module.get_pivot(None, None, None)
    assert ori_module.get_pivot(None, None, None) == test_module.get_pivot(None, None, None)
def test_help_sort3():
    assert ori_module.help_sort3(None, None, None) == test_module.help_sort3(None, None, None)
    assert ori_module.help_sort3(None, None, None) == test_module.help_sort3(None, None, None)
    assert ori_module.help_sort3(None, None, None) == test_module.help_sort3(None, None, None)
    assert ori_module.help_sort3(None, 0, 1) == test_module.help_sort3(None, 0, 1)
    assert ori_module.help_sort3(None, 0, 0) == test_module.help_sort3(None, 0, 0)
def test_sort3():
    assert ori_module.sort3(None) == test_module.sort3(None)
    assert ori_module.sort3(None) == test_module.sort3(None)
    assert ori_module.sort3(None) == test_module.sort3(None)
    assert ori_module.sort3(None) == test_module.sort3(None)
    assert ori_module.sort3(None) == test_module.sort3(None)
    assert ori_module.sort3(None) == test_module.sort3(None)
def test_sort1():
    assert ori_module.sort1(None) == test_module.sort1(None)
def test_sort2():
    assert ori_module.sort2(None) == test_module.sort2(None)
    assert ori_module.sort2(None) == test_module.sort2(None)
def test_get_pivot():
    assert ori_module.get_pivot(None, None, None) == test_module.get_pivot(None, None, None)
    assert ori_module.get_pivot(None, None, None) == test_module.get_pivot(None, None, None)
    assert ori_module.get_pivot(None, None, None) == test_module.get_pivot(None, None, None)
def test_help_sort3():
    assert ori_module.help_sort3(None, None, None) == test_module.help_sort3(None, None, None)
    assert ori_module.help_sort3(None, None, None) == test_module.help_sort3(None, None, None)
    assert ori_module.help_sort3(None, None, None) == test_module.help_sort3(None, None, None)
    assert ori_module.help_sort3(None, 0, 1) == test_module.help_sort3(None, 0, 1)
    assert ori_module.help_sort3(None, 0, 0) == test_module.help_sort3(None, 0, 0)
def test_sort3():
    assert ori_module.sort3(None) == test_module.sort3(None)
    assert ori_module.sort3(None) == test_module.sort3(None)
    assert ori_module.sort3(None) == test_module.sort3(None)
    assert ori_module.sort3(None) == test_module.sort3(None)
    assert ori_module.sort3(None) == test_module.sort3(None)
    assert ori_module.sort3(None) == test_module.sort3(None)
def test_sort1():
    assert ori_module.sort1(None) == test_module.sort1(None)
def test_sort2():
    assert ori_module.sort2(None) == test_module.sort2(None)
    assert ori_module.sort2(None) == test_module.sort2(None)
def test_get_pivot():
    assert ori_module.get_pivot(None, None, None) == test_module.get_pivot(None, None, None)
    assert ori_module.get_pivot(None, None, None) == test_module.get_pivot(None, None, None)
    assert ori_module.get_pivot(None, None, None) == test_module.get_pivot(None, None, None)
def test_help_sort3():
    assert ori_module.help_sort3(None, None, None) == test_module.help_sort3(None, None, None)
    assert ori_module.help_sort3(None, None, None) == test_module.help_sort3(None, None, None)
    assert ori_module.help_sort3(None, None, None) == test_module.help_sort3(None, None, None)
    assert ori_module.help_sort3(None, 0, 1) == test_module.help_sort3(None, 0, 1)
    assert ori_module.help_sort3(None, 0, 0) == test_module.help_sort3(None, 0, 0)
def test_sort3():
    assert ori_module.sort3(None) == test_module.sort3(None)
    assert ori_module.sort3(None) == test_module.sort3(None)
    assert ori_module.sort3(None) == test_module.sort3(None)
    assert ori_module.sort3(None) == test_module.sort3(None)
    assert ori_module.sort3(None) == test_module.sort3(None)
    assert ori_module.sort3(None) == test_module.sort3(None)
def test_sort1():
    assert ori_module.sort1(None) == test_module.sort1(None)
def test_sort2():
    assert ori_module.sort2(None) == test_module.sort2(None)
    assert ori_module.sort2(None) == test_module.sort2(None)
def test_get_pivot():
    assert ori_module.get_pivot(None, None, None) == test_module.get_pivot(None, None, None)
    assert ori_module.get_pivot(None, None, None) == test_module.get_pivot(None, None, None)
    assert ori_module.get_pivot(None, None, None) == test_module.get_pivot(None, None, None)
def test_help_sort3():
    assert ori_module.help_sort3(None, None, None) == test_module.help_sort3(None, None, None)
    assert ori_module.help_sort3(None, None, None) == test_module.help_sort3(None, None, None)
    assert ori_module.help_sort3(None, None, None) == test_module.help_sort3(None, None, None)
    assert ori_module.help_sort3(None, None, None) == test_module.help_sort3(None, None, None)
def test_sort3():
    assert ori_module.sort3(None) == test_module.sort3(None)
    assert ori_module.sort3(None) == test_module.sort3(None)
    assert ori_module.sort3(None) == test_module.sort3(None)
    assert ori_module.sort3(None) == test_module.sort3(None)
    assert ori_module.sort3(None) == test_module.sort3(None)
def test_sort1():
    assert ori_module.sort1(None) == test_module.sort1(None)
def test_sort2():
    assert ori_module.sort2(None) == test_module.sort2(None)
    assert ori_module.sort2(None) == test_module.sort2(None)
def test_get_pivot():
    assert ori_module.get_pivot(None, None, None) == test_module.get_pivot(None, None, None)
    assert ori_module.get_pivot(None, None, None) == test_module.get_pivot(None, None, None)
    assert ori_module.get_pivot(None, None, None) == test_module.get_pivot(None, None, None)
def test_help_sort3():
    assert ori_module.help_sort3(None, None, None) == test_module.help_sort3(None, None, None)
    assert ori_module.help_sort3(None, None, None) == test_module.help_sort3(None, None, None)
    assert ori_module.help_sort3(None, None, None) == test_module.help_sort3(None, None, None)
    assert ori_module.help_sort3(None, None, None) == test_module.help_sort3(None, None, None)
def test_sort3():
    assert ori_module.sort3(None) == test_module.sort3(None)
    assert ori_module.sort3(None) == test_module.sort3(None)
    assert ori_module.sort3(None) == test_module.sort3(None)
    assert ori_module.sort3(None) == test_module.sort3(None)
    assert ori_module.sort3(None) == test_module.sort3(None)
def test_sort1():
    assert ori_module.sort1(None) == test_module.sort1(None)
def test_sort2():
    assert ori_module.sort2(None) == test_module.sort2(None)
    assert ori_module.sort2(None) == test_module.sort2(None)
def test_get_pivot():
    assert ori_module.get_pivot(None, None, None) == test_module.get_pivot(None, None, None)
    assert ori_module.get_pivot(None, None, None) == test_module.get_pivot(None, None, None)
    assert ori_module.get_pivot(None, None, None) == test_module.get_pivot(None, None, None)
def test_help_sort3():
    assert ori_module.help_sort3(None, None, None) == test_module.help_sort3(None, None, None)
    assert ori_module.help_sort3(None, None, None) == test_module.help_sort3(None, None, None)
    assert ori_module.help_sort3(None, None, None) == test_module.help_sort3(None, None, None)
    assert ori_module.help_sort3(None, None, None) == test_module.help_sort3(None, None, None)
def test_sort3():
    assert ori_module.sort3(None) == test_module.sort3(None)
    assert ori_module.sort3(None) == test_module.sort3(None)
    assert ori_module.sort3(None) == test_module.sort3(None)
    assert ori_module.sort3(None) == test_module.sort3(None)
    assert ori_module.sort3(None) == test_module.sort3(None)
def test_sort1():
    assert ori_module.sort1(None) == test_module.sort1(None)
def test_sort1():
    assert ori_module.sort1(None) == test_module.sort1(None)
def test_sort1():
    assert ori_module.sort1(None) == test_module.sort1(None)
def test_sort1():
    assert ori_module.sort1(None) == test_module.sort1(None)
def test_sort1():
    assert ori_module.sort1(None) == test_module.sort1(None)
def test_sort1():
    assert ori_module.sort1(None) == test_module.sort1(None)
def test_sort1():
    assert ori_module.sort1(None) == test_module.sort1(None)
def test_sort1():
    assert ori_module.sort1(None) == test_module.sort1(None)
def test_sort1():
    assert ori_module.sort1(None) == test_module.sort1(None)
