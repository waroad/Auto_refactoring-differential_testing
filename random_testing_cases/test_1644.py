import subprocess
import sys
from hypothesis import given, settings, strategies as st

def execute_script_content(script_content, func_name, *args):
    wrapped_script = f"""
import sys
from {script_content} import {func_name}

if __name__ == '__main__':
    args = [int(arg) if arg.isdigit() else arg for arg in sys.argv[1:]]
    result = {func_name}(*args)
    print(result)
"""
    # Execute the wrapped script and capture stdout and stderr
    result = subprocess.run(
        [sys.executable, '-c', wrapped_script] + [str(arg) for arg in args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    return result.stdout.strip(), result.stderr.strip()

def compare_outputs(original_output, updated_output):
    return original_output == updated_output

# Read script content
def read_script_content(script_path):
    with open(script_path, 'r') as file:
        return file.read()

original_script = "examples/backjoon/1644.py"
updated_script = "updated/backjoon/1644.py"

# Test for prime_numbers function
@settings(max_examples=100, deadline=None)
@given(st.integers(min_value=1, max_value=1000))
def test_prime_numbers(n):
    original_output, _ = execute_script_content(original_script, 'prime_numbers', n)
    updated_output, _ = execute_script_content(updated_script, 'prime_numbers', n)
    
    assert compare_outputs(original_output, updated_output), f"prime_numbers differs for input: n={n}"

# Test for main function
@settings(max_examples=100, deadline=None)
@given(st.integers(min_value=1, max_value=1000))
def test_main(N):
    original_output, _ = execute_script_content(original_script, 'main', N)
    updated_output, _ = execute_script_content(updated_script, 'main', N)
    
    assert compare_outputs(original_output, updated_output), f"stdout differs for input: N={N}"

if __name__ == "__main__":
    import pytest
    pytest.main()
