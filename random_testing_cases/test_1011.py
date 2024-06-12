import subprocess
import sys
import warnings
from hypothesis import given, settings, strategies as st
from pytest import PytestAssertRewriteWarning

warnings.filterwarnings("ignore", category=PytestAssertRewriteWarning)

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
@given(st.integers(min_value=1, max_value=100), st.integers(min_value=1, max_value=100))
def test_main(x, y):
    if x > y:
        x, y = y, x 

    original_file = "examples/backjoon/1011.py"
    updated_file = "updated/backjoon/1011.py" 
    
    original_stdout, original_stderr = execute_script(original_file, x, y)
    updated_stdout, updated_stderr = execute_script(updated_file, x, y)
    
    assert compare_outputs(original_stdout, updated_stdout), f"stdout differs for inputs: x={x}, y={y}"
    assert compare_outputs(original_stderr, updated_stderr), f"stderr differs for inputs: x={x}, y={y}"

if __name__ == "__main__":
    import pytest
    pytest.main()
