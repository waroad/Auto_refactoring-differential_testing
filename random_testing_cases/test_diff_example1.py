import importlib.util
import pytest

ori_module_spec = importlib.util.spec_from_file_location('ori_module', './examples/simple/diff_example1.py')
test_module_spec = importlib.util.spec_from_file_location('test_module', './updated/simple/diff_example1.py')
ori_module = importlib.util.module_from_spec(ori_module_spec)
test_module = importlib.util.module_from_spec(test_module_spec)
ori_module_spec.loader.exec_module(ori_module)
test_module_spec.loader.exec_module(test_module)

def test_main():
    ori_list_1, ori_list_2, ori_dict_1, ori_set_1 = ori_module.main()
    test_list_1, test_list_2, test_dict_1, test_set_1 = test_module.main()

    assert len(ori_list_1) == len(test_list_1)
    assert len(ori_list_2) == len(test_list_2)
    assert len(ori_dict_1) == len(test_dict_1)
    assert len(ori_set_1) == len(test_set_1)

    assert ori_list_1 == test_list_1
    assert ori_list_2 == test_list_2
    assert ori_dict_1 == test_dict_1
    assert ori_set_1 == test_set_1