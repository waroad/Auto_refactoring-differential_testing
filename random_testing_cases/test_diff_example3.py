import importlib.util
import pytest
from hypothesis import given, strategies as st

# 모듈 로드
ori_module_spec = importlib.util.spec_from_file_location('ori_module', './examples/simple/diff_example3.py')
test_module_spec = importlib.util.spec_from_file_location('test_module', './updated/simple/diff_example3.py')
ori_module = importlib.util.module_from_spec(ori_module_spec)
test_module = importlib.util.module_from_spec(test_module_spec)
ori_module_spec.loader.exec_module(ori_module)
test_module_spec.loader.exec_module(test_module)

# Composite strategy to generate exactly 100 unique integers
@given(st.lists(st.integers(min_value=-100, max_value=100), min_size=100, max_size=100, unique=True))
def test_ber_random(names):
    for name in names:
        assert ori_module.ber(name) == test_module.ber(name)