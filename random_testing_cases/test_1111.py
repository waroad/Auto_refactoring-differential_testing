import subprocess
import sys
from hypothesis import given, settings, strategies as st

def execute_script(script_path, *args):
    result = subprocess.run(
        [sys.executable, script_path] + [str(arg) for arg in args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.stdout.decode(), result.stderr.decode()

def compare_outputs(original_output, updated_output):
    return original_output == updated_output

@settings(max_examples=100, deadline=None)
@given(
    st.integers(min_value=1, max_value=20),  # 리스트의 길이
    st.lists(st.integers(min_value=-100, max_value=100), min_size=1, max_size=20)  # 리스트 요소들
)
def test_main(N, list1):
    if len(list1) < N:
        list1.extend([0] * (N - len(list1)))  # 길이를 N으로 맞추기
    
    list1_str = ' '.join(map(str, list1[:N]))

    original_file = "examples/backjoon/1111.py"  # Original file path
    updated_file = "updated/backjoon/1111.py"  # Updated file path
    
    original_stdout, original_stderr = execute_script(original_file, N, *list1[:N])
    updated_stdout, updated_stderr = execute_script(updated_file, N, *list1[:N])
    
    assert compare_outputs(original_stdout, updated_stdout), f"stdout differs for inputs: N={N}, list1={list1[:N]}"
    assert compare_outputs(original_stderr, updated_stderr), f"stderr differs for inputs: N={N}, list1={list1[:N]}"

if __name__ == "__main__":
    import pytest
    pytest.main()
