import importlib.util
import pytest
from hypothesis import given, strategies as st, settings, HealthCheck

# 모듈 로드
ori_module_spec = importlib.util.spec_from_file_location('ori_module', './examples/simple/diff_example5.py')
test_module_spec = importlib.util.spec_from_file_location('test_module', './updated/simple/diff_example5.py')
ori_module = importlib.util.module_from_spec(ori_module_spec)
test_module = importlib.util.module_from_spec(test_module_spec)
ori_module_spec.loader.exec_module(ori_module)
test_module_spec.loader.exec_module(test_module)

# 리스트와 튜플을 생성하는 전략 정의
lists_strategy = st.lists(st.integers(), min_size=0, max_size=5)
tuples_strategy = st.one_of(
    st.tuples(),
    st.tuples(st.integers(min_value=-100, max_value=100), st.integers(min_value=-100, max_value=100), st.integers(min_value=-100, max_value=100)),
)

# 랜덤 테스트 케이스 생성 및 테스트 함수 정의
@settings(max_examples=10, suppress_health_check=[HealthCheck.too_slow])
@given(st.lists(st.tuples(lists_strategy, tuples_strategy), min_size=10, max_size=10))
def test_truth_value_random(inputs):
    for lst, tpl in inputs:
        # 각 입력을 출력합니다.
        print(f"Testing with inputs: list={lst}, tuple={tpl}")
        assert ori_module.truth_value(lst, tpl) == test_module.truth_value(lst, tpl)