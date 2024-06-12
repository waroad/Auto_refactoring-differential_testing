import importlib.util
import pytest
from hypothesis import given, strategies as st

# 모듈 로드
ori_module_spec = importlib.util.spec_from_file_location('ori_module', './examples/simple/diff_example2.py')
test_module_spec = importlib.util.spec_from_file_location('test_module', './updated/simple/diff_example2.py')
ori_module = importlib.util.module_from_spec(ori_module_spec)
test_module = importlib.util.module_from_spec(test_module_spec)
ori_module_spec.loader.exec_module(ori_module)
test_module_spec.loader.exec_module(test_module)

# 랜덤 테스트 케이스 생성 및 테스트 함수 정의
@given(st.lists(st.tuples(st.integers(), st.integers(), st.integers(), st.integers()), min_size=100, max_size=100, unique=True))
def test_if_expression_random(inputs):
    for a, b, c, d in inputs:
        assert ori_module.if_expression(a, b, c, d) == test_module.if_expression(a, b, c, d)