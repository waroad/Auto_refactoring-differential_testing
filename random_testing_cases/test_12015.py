import subprocess
import sys
from hypothesis import given, settings, strategies as st

def execute_main(script_content, N, list1):
    wrapper_script = f"""
import sys
from {script_content} import main
N = int(sys.argv[1])
list1 = list(map(int, sys.argv[2].split(',')))
main(N, list1)
"""
    result = subprocess.run(
        [sys.executable, '-c', wrapper_script, str(N), ','.join(map(str, list1))],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    return result.stdout.strip()

original_script = "examples/backjoon/12015.py"
updated_script = "updated/backjoon/12015.py"

@settings(max_examples=100, deadline=None)
@given(N=st.integers(min_value=1, max_value=50),
       list1=st.lists(st.integers(min_value=1, max_value=1000), min_size=1, max_size=50))
def test_main(N, list1):
    if len(list1) != N:
        list1 = list1[:N]
    original_output = execute_main(original_script, N, list1)
    updated_output = execute_main(updated_script, N, list1)
    
    assert original_output == updated_output, f"Output differs for input: N={N}, list1={list1}"

if __name__ == "__main__":
    import pytest
    pytest.main()
