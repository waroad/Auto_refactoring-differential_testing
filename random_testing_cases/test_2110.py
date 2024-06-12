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

def read_script_content(script_path):
    with open(script_path, 'r') as file:
        return file.read()

original_script_content = read_script_content("examples/backjoon/2110.py")
updated_script_content = read_script_content("updated/backjoon/2110.py")

@settings(max_examples=100, deadline=None)
@given(
    st.integers(min_value=1, max_value=1000),  
    st.integers(min_value=1, max_value=1000),  
    st.integers(min_value=1, max_value=10)     
)
def test_main(house1, house2, C):
    if house1 == house2:
        return 
    
    original_stdout, original_stderr = execute_script("examples/backjoon/2110.py", house1, house2, C)
    updated_stdout, updated_stderr = execute_script("updated/backjoon/2110.py", house1, house2, C)
    
    assert compare_outputs(original_stdout, updated_stdout), f"stdout differs for inputs: house1={house1}, house2={house2}, C={C}"
    assert compare_outputs(original_stderr, updated_stderr), f"stderr differs for inputs: house1={house1}, house2={house2}, C={C}"

if __name__ == "__main__":
    import pytest
    pytest.main()
