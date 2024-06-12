import importlib.util
import pytest
from hypothesis import given, strategies as st, settings, HealthCheck

# 모듈 로드 함수 정의
def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# 모듈 로드
ori_module = load_module('ori_module', './examples/simple/diff_example9.py')
test_module = load_module('test_module', './updated/simple/diff_example9.py')

# 랜덤 테스트 케이스 생성 및 테스트 함수 정의
@settings(max_examples=2, suppress_health_check=[HealthCheck.too_slow])
@given(st.booleans())
def test_return_bool_random(A):
    # 각 입력을 출력합니다.
    print(f"Testing with input: A={A}")
    ori_result = ori_module.return_bool(A)
    test_result = test_module.return_bool(A)

    # 결과 비교
    assert ori_result == test_result