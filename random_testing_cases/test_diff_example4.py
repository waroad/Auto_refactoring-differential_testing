import importlib.util
import pytest
from hypothesis import given, strategies as st, settings, HealthCheck

def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

ori_module = load_module('ori_module', './examples/simple/diff_example4.py')
test_module = load_module('test_module', './updated/simple/diff_example4.py')

@settings(max_examples=100, suppress_health_check=[HealthCheck.too_slow])
@given(st.integers(), st.integers(), st.integers())
def test_main_random(a, b, c):
    print(f"Testing with inputs: a={a}, b={b}, c={c}")
    ori_result = ori_module.main(a, b, c)
    test_result = test_module.main(a, b, c)

    assert ori_result == test_result