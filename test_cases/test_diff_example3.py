import importlib.util
ori_module_spec = importlib.util.spec_from_file_location('ori_module', '.\\examples\\simple\\diff_example3.py')
test_module_spec = importlib.util.spec_from_file_location('test_module', '.\\updated\\simple\\diff_example3.py')
ori_module = importlib.util.module_from_spec(ori_module_spec)
test_module = importlib.util.module_from_spec(test_module_spec)
ori_module_spec.loader.exec_module(ori_module)
test_module_spec.loader.exec_module(test_module)

def test_ber():
    assert ori_module.ber(1) == test_module.ber(1)
    assert ori_module.ber(2) == test_module.ber(2)
    assert ori_module.ber(3) == test_module.ber(3)
    assert ori_module.ber(4) == test_module.ber(4)
