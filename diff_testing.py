import argparse
import ast
import z3
import path_list
from any_proxy import AnyProxy
import pytest
import os

def test_case_generate(original_path, test_path, params, test_inputs, func_name):
    o_path_list = original_path.split("\\")
    # original_path = os.path.join("..", original_path)
    # with open(f"./testcases/test_{func_name}.py", "w") as f:
    #     f.write(f"import {original_path}/{func_name}")
    # print(original_path, test_path, params, test_inputs, func_name)

def test_refactored_code():
    pass

def test(f, *args):
    global test_inputs
    path_list.__path__ = []
    while True:
        path_list.__pathcondition__ = []
        try:
            result = f(*args)
        except Exception as e:
            print("error in test", e)
        #####################
        solver = z3.Solver()
        solver.add(path_list.__pathcondition__)
        solver.check()
        model = solver.model()
        
        temp_dict = {}
        for d in model.decls():
            temp_dict[d.name()] = model[d]
        test_inputs.append(temp_dict)
        #####################
        while len(path_list.__path__) > 0 and not path_list.__path__[-1]:
            path_list.__path__.pop()
        
        if path_list.__path__ == []:
            return
        path_list.__path__[-1] = False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Difference test with two files.')
    parser.add_argument('-t1', '--target1', required=True)
    parser.add_argument('-t2', '--target2', required=True)
    parse_args = parser.parse_args()
    original_code = parse_args.target1
    refactored_code = parse_args.target2

    original_lines = open(original_code, "r").read()
    refactored_lines = open(refactored_code, "r").read()

    ### symbolic execution으로 function test의 input 얻기 ###


    test_inputs = []
    functions = {}
    global_env = {}
    exec(original_lines, global_env)

    for name, func in global_env.items():
        if callable(func):
            args = func.__code__.co_varnames[:func.__code__.co_argcount]
            anyproxy_args = [AnyProxy(arg) for arg in args]
            
            try:
                test(func, *anyproxy_args)
            except Exception as e:
                print(f"Error while executing ", e)
            
            test_case_generate(parse_args.target1, parse_args.target2, args, test_inputs, func.__name__)
        ### test input으로 만든 pytest 실행 ###
        ### subprocess로 실행해서 print 결과 확인 ###