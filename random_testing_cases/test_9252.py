import subprocess
import sys
from hypothesis import given, settings, strategies as st

def execute_main(script_content, l1, l2):
    wrapper_script = f"""
import sys
from {script_content} import main
l1 = sys.argv[1].split(',')
l2 = sys.argv[2].split(',')
main(l1, l2)
"""
    result = subprocess.run(
        [sys.executable, '-c', wrapper_script, ','.join(l1), ','.join(l2)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    return result.stdout.strip()

original_script = "examples/backjoon/9252.py"
updated_script = "updated/backjoon/9252.py"

@settings(max_examples=100, deadline=None)
@given(l1=st.lists(st.characters(min_codepoint=65, max_codepoint=90), min_size=1, max_size=10, unique=False),
       l2=st.lists(st.characters(min_codepoint=65, max_codepoint=90), min_size=1, max_size=10, unique=False))
def test_main(l1, l2):
    original_output = execute_main(original_script, l1, l2)
    updated_output = execute_main(updated_script, l1, l2)
    
    assert original_output == updated_output, f"Output differs for input: l1={l1}, l2={l2}"

if __name__ == "__main__":
    import pytest
    pytest.main()
