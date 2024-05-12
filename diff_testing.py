import argparse
import ast

def test_case_generate():
    pass

def test_refactored_code():
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Difference test with two files.')
    parser.add_argument('-t1', '--target1', required=True)
    parser.add_argument('-t2', '--target2', required=True)
    args = parser.parse_args()
    original_code = args.target1
    refactored_code = args.target2

    original_lines = open(original_code, "r").readlines()
    refactored_lines = open(refactored_code, "r").readlines()