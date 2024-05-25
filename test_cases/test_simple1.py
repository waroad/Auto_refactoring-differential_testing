import importlib.util
ori_module_spec = importlib.util.spec_from_file_location('ori_module', '.\\examples\\assign4\\simple1.py')
test_module_spec = importlib.util.spec_from_file_location('test_module', '.\\updated\\assign4\\simple1.py')
ori_module = importlib.util.module_from_spec(ori_module_spec)
test_module = importlib.util.module_from_spec(test_module_spec)
ori_module_spec.loader.exec_module(ori_module)
test_module_spec.loader.exec_module(test_module)

def test_bar1():
    assert ori_module.bar1() == test_module.bar1()
def test_bar2():
    assert ori_module.bar2() == test_module.bar2()
    assert ori_module.bar2() == test_module.bar2()
def test_bar3():
    assert ori_module.bar3(None, None, None) == test_module.bar3(None, None, None)
    assert ori_module.bar3(None, None, None) == test_module.bar3(None, None, None)
    assert ori_module.bar3(None, None, None) == test_module.bar3(None, None, None)
def test_bar4():
    assert ori_module.bar4(None, None) == test_module.bar4(None, None)
    assert ori_module.bar4(None, None) == test_module.bar4(None, None)
    assert ori_module.bar4(None, None) == test_module.bar4(None, None)
    assert ori_module.bar4(1, 0) == test_module.bar4(1, 0)
    assert ori_module.bar4(0, 0) == test_module.bar4(0, 0)
    assert ori_module.bar4(0, 1) == test_module.bar4(0, 1)
def test_bar5():
    assert ori_module.bar5(None) == test_module.bar5(None)
    assert ori_module.bar5(None) == test_module.bar5(None)
    assert ori_module.bar5(None) == test_module.bar5(None)
    assert ori_module.bar5(1) == test_module.bar5(1)
    assert ori_module.bar5(0) == test_module.bar5(0)
    assert ori_module.bar5(0) == test_module.bar5(0)
    assert ori_module.bar5(None) == test_module.bar5(None)
def test_bar6():
    assert ori_module.bar6() == test_module.bar6()
    assert ori_module.bar6() == test_module.bar6()
    assert ori_module.bar6() == test_module.bar6()
    assert ori_module.bar6() == test_module.bar6()
    assert ori_module.bar6() == test_module.bar6()
    assert ori_module.bar6() == test_module.bar6()
    assert ori_module.bar6() == test_module.bar6()
    assert ori_module.bar6() == test_module.bar6()
def test_bar7():
    assert ori_module.bar7(None, None, None) == test_module.bar7(None, None, None)
    assert ori_module.bar7(None, None, None) == test_module.bar7(None, None, None)
    assert ori_module.bar7(None, None, None) == test_module.bar7(None, None, None)
    assert ori_module.bar7(1, 0, None) == test_module.bar7(1, 0, None)
    assert ori_module.bar7(0, 0, None) == test_module.bar7(0, 0, None)
    assert ori_module.bar7(0, 1, None) == test_module.bar7(0, 1, None)
    assert ori_module.bar7(None, None, None) == test_module.bar7(None, None, None)
    assert ori_module.bar7(None, None, None) == test_module.bar7(None, None, None)
    assert ori_module.bar7(1, 0, None) == test_module.bar7(1, 0, None)
    assert ori_module.bar7(0, 0, None) == test_module.bar7(0, 0, None)
