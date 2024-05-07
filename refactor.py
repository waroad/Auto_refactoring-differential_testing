import ast
import argparse
import sys




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Measures coverage.')
    parser.add_argument('-t', '--target', required=True)
    parser.add_argument("remaining", nargs="*")
    args = parser.parse_args()
    target = args.target
    lines = open(target, "r").readlines()
    root = ast.parse("".join(lines), target)

    print(ast.unparse(root))