import importlib.util
ori_module_spec = importlib.util.spec_from_file_location('ori_module', '.\\examples\\simple\\diff_example7.py')
test_module_spec = importlib.util.spec_from_file_location('test_module', '.\\updated\\simple\\diff_example7.py')
ori_module = importlib.util.module_from_spec(ori_module_spec)
test_module = importlib.util.module_from_spec(test_module_spec)
ori_module_spec.loader.exec_module(ori_module)
test_module_spec.loader.exec_module(test_module)

def test_if_expression():
    assert ori_module.if_expression(1) == test_module.if_expression(1)
    assert ori_module.if_expression(0) == test_module.if_expression(0)
