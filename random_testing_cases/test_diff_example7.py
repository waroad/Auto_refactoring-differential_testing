import importlib.util
import pytest
from hypothesis import given, strategies as st, settings, HealthCheck

# 모듈 로드
ori_module_spec = importlib.util.spec_from_file_location('ori_module', './examples/simple/diff_example7.py')
test_module_spec = importlib.util.spec_from_file_location('test_module', './updated/simple/diff_example7.py')
ori_module = importlib.util.module_from_spec(ori_module_spec)
test_module = importlib.util.module_from_spec(test_module_spec)
ori_module_spec.loader.exec_module(ori_module)
test_module_spec.loader.exec_module(test_module)

# 랜덤 테스트 케이스 생성 및 테스트 함수 정의
@settings(max_examples=100, suppress_health_check=[HealthCheck.too_slow])
@given(st.integers(min_value=-100, max_value=100))
def test_if_expression_random(x):
    # 각 입력을 출력합니다.
    print(f"Testing with input: x={x}")
    assert ori_module.if_expression(x) == test_module.if_expression(x)