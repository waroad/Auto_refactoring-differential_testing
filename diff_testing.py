import argparse
import z3
import path_list
from any_proxy import AnyProxy
import os
import subprocess
import traceback
import re
import types
import shutil

def test_case_generate(test_cases_path, original_path, test_path, params, test_inputs, func_name):
    ori_file_name = os.path.basename(original_path)[:-3]
    test_file_name = os.path.basename(test_path)[:-3]

    test_case_file = os.path.join(test_cases_path, f"test_{ori_file_name}.py")

    if not os.path.exists(test_case_file):
        with open(test_case_file, "w") as f:
            f.write("import importlib.util\n")
            f.write("ori_module_spec = importlib.util.spec_from_file_location('ori_module', '" + original_path.replace('\\', '\\\\') + "')\n")
            f.write("test_module_spec = importlib.util.spec_from_file_location('test_module', '" + test_path.replace('\\', '\\\\') + "')\n")
            f.write("ori_module = importlib.util.module_from_spec(ori_module_spec)\n")
            f.write("test_module = importlib.util.module_from_spec(test_module_spec)\n")
            f.write("ori_module_spec.loader.exec_module(ori_module)\n")
            f.write("test_module_spec.loader.exec_module(test_module)\n\n")

    with open(test_case_file, "a") as f:
        f.write(f"def test_{func_name}():\n")
        for input_dict in test_inputs:
            for key, val in path_list.__typedict__.items():
                if val == list:
                    list1 = []
                    for input_key, input_val in input_dict.items():
                        if input_key == key + "_length":
                            while len(list1) < input_val.as_long():
                                list1.append(0)
                        if input_key.startswith(key + "__"):
                            index = int(input_key.split("__")[1])
                            while len(list1) <= index:
                                list1.append(0)
                            list1[index] = input_val
                    input_dict[key] = list1
                elif val == tuple:
                    tuple1 = []
                    for input_key, input_val in input_dict.items():
                        if input_key == key + "_length":
                            while len(tuple1) < input_val.as_long():
                                tuple1.append(0)
                        if input_key.startswith(key + "__"):
                            index = int(input_key.split("__")[1])
                            while len(tuple1) <= index:
                                tuple1.append(0)
                            tuple1[index] = input_val
                    input_dict[key] = tuple(tuple1)
                elif val == set:
                    set1 = []
                    for input_key, input_val in input_dict.items():
                        if input_key == key + "_length":
                            while len(set1) < input_val.as_long():
                                set1.append(0)
                        if input_key.startswith(key + "__"):
                            index = int(input_key.split("__")[1])
                            while len(set1) <= index:
                                set1.append(0)
                            set1[index] = input_val
                    input_dict[key] = set(set1)
        
            input_list = [input_dict.get(name, 0) for name in params]
            input_list_str = map(str, input_list)
            input_str = ', '.join(input_list_str)
            f.write("    try:\n")
            f.write(f"        ori_result = ori_module.{func_name}({input_str})\n")
            f.write(f"    except Exception as e:\n")
            f.write(f"        ori_result = str(e)\n")
            f.write("    try:\n")
            f.write(f"        test_result = test_module.{func_name}({input_str})\n")
            f.write(f"    except Exception as e:\n")
            f.write(f"        test_result = str(e)\n")
            f.write(f"    assert ori_result == test_result\n")


def test_refactored_code(original_path, test_path):
    cur_dir = os.getcwd()
    test_case_path = os.path.dirname(original_path)
    ori_file_name = os.path.basename(original_path)
    test_file_name = os.path.basename(test_path)
    os.chdir(test_case_path)
    cmd1 = ['python', ori_file_name]
    result1 = subprocess.run(cmd1, capture_output=True, text=True)
    cmd2 = ['python', test_file_name]
    result2 = subprocess.run(cmd2, capture_output=True, text=True)

    os.chdir(cur_dir)
    try:
        assert result1.stdout == result2.stdout
        assert result1.stderr == result2.stderr
    except Exception as e:
        print("Error while testing stdout and stderr", e)

def test(f, name, *args):
    global test_inputs
    path_list.__path__ = []
    while True:
        path_list.__pathcondition__ = []
        try:
            result = f(*args)
        except IndexError:
            pass
        except Exception as e:
            print(f"error in test {name}", e)
            traceback.print_exc()
        solver = z3.Solver()
        solver.add(path_list.__pathcondition__)
        solver.check()
        model = solver.model()
        
        temp_dict = {}
        for d in model.decls():
            temp_dict[d.name()] = model[d]
        test_inputs.append(temp_dict)
        # print(path_list.__path__, path_list.__pathcondition__)
        while len(path_list.__path__) > 0 and not path_list.__path__[-1]:
            path_list.__path__.pop()
        if path_list.__path__ == []:
            return
        path_list.__path__[-1] = False

def main(original_folder, refactored_folder):
    global test_inputs
    original_files = []
    refactored_files = []
    if original_folder.endswith(".py"):
        original_files.append(original_folder)
    else:
        for root, dirs, files in os.walk(original_folder):
            for file in files:
                original_files.append(os.path.join(root, file))
    
    if refactored_folder.endswith(".py"):
        refactored_files.append(refactored_folder)
    else:
        for root, dirs, files in os.walk(refactored_folder):
            for file in files:
                refactored_files.append(os.path.join(root, file))
    
    original_files.sort()
    refactored_files.sort()

    test_cases_path = os.path.join(os.getcwd(), 'test_cases')
    if os.path.exists(test_cases_path):
        shutil.rmtree(test_cases_path)
    os.makedirs(test_cases_path, exist_ok=True)

    for original_file in original_files:
        basename = os.path.basename(original_file)
        refactored_file = next((f for f in refactored_files if os.path.basename(f) == basename), None)
        if refactored_file and original_file.endswith('.py'):
            with open(original_file, "r", encoding="utf-8") as f:
                original_code = f.read()
                original_code = re.sub(r'\bwhile\b', 'if', original_code)
            
            test_inputs = []
            functions = {}
            global_env = {}
            try:
                exec(original_code, global_env)
            except Exception as e:
                print(f"{e}, {original_file}")

            for name, func in global_env.items():
                if isinstance(func, types.FunctionType):
                    args = func.__code__.co_varnames[:func.__code__.co_argcount]
                    anyproxy_args = [AnyProxy(arg) for arg in args]

                    try:
                        test(func, original_file, *anyproxy_args)
                    except Exception as e:
                        print(f"Error while executing {original_file}", e)

                    test_case_generate(test_cases_path, original_file, refactored_file, args, test_inputs, func.__name__)
                
            test_refactored_code(original_file, refactored_file)
    
    result = subprocess.run(['pytest', test_cases_path], capture_output=True, text=True)
    print(result.stdout)
    print(result.stderr)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Difference test with two folders.')
    parser.add_argument('-t1', '--target1', required=True)
    parser.add_argument('-t2', '--target2', required=True)
    parse_args = parser.parse_args()
    original_folder = parse_args.target1
    refactored_folder = parse_args.target2
    main(original_folder, refactored_folder)
