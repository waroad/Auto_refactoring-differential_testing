import refactor
import diff_testing
import argparse

def main(t1, t2):
    refactor.main(t1, t2)
    print("Refactoring done")
    diff_testing.main(t1, t2)
    print("Differential testing done")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Difference test with two folders.')
    parser.add_argument('-t1', '--target1', required=True)
    parser.add_argument('-t2', '--target2', required=True)
    parse_args = parser.parse_args()
    t1 = parse_args.target1
    t2 = parse_args.target2
    main(t1, t2)