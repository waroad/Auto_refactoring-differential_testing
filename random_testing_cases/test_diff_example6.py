import importlib.util
import pytest
from hypothesis import given, strategies as st, settings, HealthCheck

# 모듈 로드
ori_module_spec = importlib.util.spec_from_file_location('ori_module', './examples/simple/diff_example6.py')
test_module_spec = importlib.util.spec_from_file_location('test_module', './updated/simple/diff_example6.py')
ori_module = importlib.util.module_from_spec(ori_module_spec)
test_module = importlib.util.module_from_spec(test_module_spec)
ori_module_spec.loader.exec_module(ori_module)
test_module_spec.loader.exec_module(test_module)

# 랜덤 테스트 케이스 생성 및 테스트 함수 정의
@settings(max_examples=100, suppress_health_check=[HealthCheck.too_slow])
@given(st.integers(), st.integers())
def test_nested_if_random(x, y):
    # 각 입력을 출력합니다.
    print(f"Testing with inputs: x={x}, y={y}")
    assert ori_module.nested_if(x, y) == test_module.nested_if(x, y)