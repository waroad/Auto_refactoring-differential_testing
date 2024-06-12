import importlib.util
import pytest

# 모듈 로드 함수 정의
def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# 모듈 로드
ori_module = load_module('ori_module', './examples/simple/diff_example10.py')
test_module = load_module('test_module', './updated/simple/diff_example10.py')

def test_main():
    ori_result = ori_module.main()
    test_result = test_module.main()

    # 결과 비교
    assert ori_result == test_result