import importlib.util
ori_module_spec = importlib.util.spec_from_file_location('ori_module', '.\\examples\\simple\\diff_example6.py')
test_module_spec = importlib.util.spec_from_file_location('test_module', '.\\updated\\simple\\diff_example6.py')
ori_module = importlib.util.module_from_spec(ori_module_spec)
test_module = importlib.util.module_from_spec(test_module_spec)
ori_module_spec.loader.exec_module(ori_module)
test_module_spec.loader.exec_module(test_module)

def test_nested_if():
    assert ori_module.nested_if(1, 1) == test_module.nested_if(1, 1)
    assert ori_module.nested_if(1, 0) == test_module.nested_if(1, 0)
    assert ori_module.nested_if(0, None) == test_module.nested_if(0, None)
def test_nested_if():
    assert ori_module.nested_if(1, 1) == test_module.nested_if(1, 1)
    assert ori_module.nested_if(1, 0) == test_module.nested_if(1, 0)
    assert ori_module.nested_if(0, None) == test_module.nested_if(0, None)
def test_nested_if():
    assert ori_module.nested_if(1, 1) == test_module.nested_if(1, 1)
    assert ori_module.nested_if(1, 0) == test_module.nested_if(1, 0)
    assert ori_module.nested_if(0, None) == test_module.nested_if(0, None)
def test_nested_if():
    assert ori_module.nested_if(1, 1) == test_module.nested_if(1, 1)
    assert ori_module.nested_if(1, 0) == test_module.nested_if(1, 0)
    assert ori_module.nested_if(0, None) == test_module.nested_if(0, None)
def test_nested_if():
    assert ori_module.nested_if(1, 1) == test_module.nested_if(1, 1)
    assert ori_module.nested_if(1, 0) == test_module.nested_if(1, 0)
    assert ori_module.nested_if(0, None) == test_module.nested_if(0, None)
def test_nested_if():
    assert ori_module.nested_if(1, 1) == test_module.nested_if(1, 1)
    assert ori_module.nested_if(1, 0) == test_module.nested_if(1, 0)
    assert ori_module.nested_if(0, None) == test_module.nested_if(0, None)
def test_nested_if():
    assert ori_module.nested_if(1, 1) == test_module.nested_if(1, 1)
    assert ori_module.nested_if(1, 0) == test_module.nested_if(1, 0)
    assert ori_module.nested_if(0, None) == test_module.nested_if(0, None)
def test_nested_if():
    assert ori_module.nested_if(1, 1) == test_module.nested_if(1, 1)
    assert ori_module.nested_if(1, 0) == test_module.nested_if(1, 0)
    assert ori_module.nested_if(0, None) == test_module.nested_if(0, None)
