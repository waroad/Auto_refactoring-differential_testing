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
ori_module = load_module('ori_module', './examples/simple/diff_example8.py')
test_module = load_module('test_module', './updated/simple/diff_example8.py')

# 랜덤 테스트 케이스 생성 및 테스트 함수 정의
@settings(max_examples=100, suppress_health_check=[HealthCheck.too_slow])
@given(st.lists(st.integers(), min_size=1, max_size=10))
def test_main_random(players):
    # 각 입력을 출력합니다.
    print(f"Testing with input: players={players}")
    ori_result = ori_module.main(players[:])  # 리스트 복사를 통해 원본 유지
    test_result = test_module.main(players[:])

    # 결과 비교
    assert ori_result == test_result