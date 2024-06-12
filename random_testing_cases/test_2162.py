import subprocess
import sys
from hypothesis import given, settings, strategies as st

def execute_script_content(module_path, func_name, *args):
    module_name = module_path.replace('/', '.').replace('.py', '')
    wrapper_script = f"""
import sys
sys.path.append('examples/backjoon')
sys.path.append('updated/backjoon')
from {module_name} import {func_name}, Point, Line
args = [int(arg) if arg.isdigit() else arg for arg in sys.argv[1:]]
if '{func_name}' in ['direction', 'intersection']:
    args = [Point(*map(int, args[i:i+2])) for i in range(0, len(args), 2)]
    if '{func_name}' == 'intersection':
        args = [Line(args[0], args[1]), Line(args[2], args[3])]
print({func_name}(*args))
"""
    result = subprocess.run(
        [sys.executable, '-c', wrapper_script] + list(map(str, args)),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    return result.stdout.strip(), result.stderr.strip()

def compare_outputs(original_output, updated_output):
    return original_output == updated_output

original_script = "examples/backjoon/2162.py"
updated_script = "updated/backjoon/2162.py"

@settings(max_examples=100, deadline=None)
@given(parent=st.lists(st.integers(min_value=0, max_value=10), min_size=11, max_size=11, unique=True),
       x=st.integers(min_value=0, max_value=10),
       a=st.integers(min_value=0, max_value=10),
       b=st.integers(min_value=0, max_value=10),
       coords=st.tuples(
           st.tuples(st.integers(min_value=-1000, max_value=1000), st.integers(min_value=-1000, max_value=1000)),
           st.tuples(st.integers(min_value=-1000, max_value=1000), st.integers(min_value=-1000, max_value=1000)),
           st.tuples(st.integers(min_value=-1000, max_value=1000), st.integers(min_value=-1000, max_value=1000)),
           st.tuples(st.integers(min_value=-1000, max_value=1000), st.integers(min_value=-1000, max_value=1000))
       ))
def test_all_functions(parent, x, a, b, coords):
    functions = ['find', 'union', 'direction', 'intersection']
    parent_str = ','.join(map(str, parent))
    arguments = {
        'find': [parent_str, x],
        'union': [parent_str, a, b],
        'direction': [*coords[0], *coords[1], *coords[2]],
        'intersection': [*coords[0], *coords[1], *coords[2], *coords[3]]
    }

    for func in functions:
        original_stdout, original_stderr = execute_script_content(original_script, func, *arguments[func])
        updated_stdout, updated_stderr = execute_script_content(updated_script, func, *arguments[func])
        assert compare_outputs(original_stdout, updated_stdout), f"{func} stdout differs for input: {arguments[func]}"
        assert compare_outputs(original_stderr, updated_stderr), f"{func} stderr differs for input: {arguments[func]}"

if __name__ == "__main__":
    import pytest
    pytest.main()
