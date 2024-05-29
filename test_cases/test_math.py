import importlib.util
ori_module_spec = importlib.util.spec_from_file_location('ori_module', '.\\examples\\assign4\\math.py')
test_module_spec = importlib.util.spec_from_file_location('test_module', '.\\updated\\assign4\\math.py')
ori_module = importlib.util.module_from_spec(ori_module_spec)
test_module = importlib.util.module_from_spec(test_module_spec)
ori_module_spec.loader.exec_module(ori_module)
test_module_spec.loader.exec_module(test_module)

def test_foo1():
    assert ori_module.foo1(0, 1, 0, 0) == test_module.foo1(0, 1, 0, 0)
    assert ori_module.foo1(0, 0, 0, 0) == test_module.foo1(0, 0, 0, 0)
def test_foo2():
    assert ori_module.foo2(0, 1, 0) == test_module.foo2(0, 1, 0)
    assert ori_module.foo2(0, 0, 0) == test_module.foo2(0, 0, 0)
    assert ori_module.foo2(1, 0, 0) == test_module.foo2(1, 0, 0)
    assert ori_module.foo2(0, 0, 0) == test_module.foo2(0, 0, 0)
def test_foo3():
    assert ori_module.foo3(0, 1, 0, 0) == test_module.foo3(0, 1, 0, 0)
    assert ori_module.foo3(0, 0, 0, 0) == test_module.foo3(0, 0, 0, 0)
    assert ori_module.foo3(1, 0, 0, 0) == test_module.foo3(1, 0, 0, 0)
    assert ori_module.foo3(0, 0, 0, 0) == test_module.foo3(0, 0, 0, 0)
    assert ori_module.foo3(1, 0, 0, 0) == test_module.foo3(1, 0, 0, 0)
    assert ori_module.foo3(0, 1, 0, 1) == test_module.foo3(0, 1, 0, 1)
    assert ori_module.foo3(0, 1, 1, 1) == test_module.foo3(0, 1, 1, 1)
    assert ori_module.foo3(0, 2, 1, 1) == test_module.foo3(0, 2, 1, 1)
    assert ori_module.foo3(0, 1, 0, 0) == test_module.foo3(0, 1, 0, 0)
    assert ori_module.foo3(0, 0, 0, 1) == test_module.foo3(0, 0, 0, 1)
    assert ori_module.foo3(0, 0, 1, 2) == test_module.foo3(0, 0, 1, 2)
    assert ori_module.foo3(0, 0, -1, 0) == test_module.foo3(0, 0, -1, 0)
