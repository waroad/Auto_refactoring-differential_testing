import os
import contextlib
from proxies import *
from z3 import *

class ExecutionContext(contextlib.ContextDecorator):
    def __init__(self):
        self.backup_files = {}

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        for file_path, backup_path in self.backup_files.items():
            if os.path.exists(backup_path):
                with open(backup_path, 'rb') as backup_file:
                    with open(file_path, 'wb') as original_file:
                        original_file.write(backup_file.read())
                os.remove(backup_path)

class SafeFile:
    def __init__(self, file_path, mode, context):
        self.file_path = file_path
        self.mode = mode
        self.context = context
        self.backup_path = file_path + ".bak"
        if os.path.exists(file_path):
            with open(file_path, 'rb') as original_file:
                with open(self.backup_path, 'wb') as backup_file:
                    backup_file.write(original_file.read())
        context.backup_files[file_path] = self.backup_path

    def __enter__(self):
        return open(self.file_path, self.mode)

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.remove(self.file_path)
        os.rename(self.backup_path, self.file_path)

def safe_open(file_path, mode='r', context=None):
    return SafeFile(file_path, mode, context)

class AnyProxy:
    def __init__(self, name):
        self.name = name

    def get_proxy(self, other):
        if isinstance(other, (int, IntegerProxy)):
            return IntegerProxy(Int(self.name))
        elif isinstance(other, (float, FloatProxy)):
            return FloatProxy(Real(self.name))
        elif isinstance(other, (str, StringProxy)):
            return StringProxy(String(self.name))
        # elif isinstance(other, AnyProxy):
        #     return self.get_proxy(other)
        else:
            raise TypeError("Unsupported type")
    
    def __eq__(self, other):
        if callable(other):
            # other이 callable로 평가되지 않고 바로 evaluate되어서 이 부분을 사용할 수 없는 상태
            # python function defer 하는 방법을 참고해서 수정해야 할 듯
            # file write를 포기하면 이 부분을 안 해도 됨
            pass
        else:
            # if type(other) == int:
            #     return IntegerProxy(Int(self.name)).__eq__(other)
            # elif type(other) == float:
            #     return FloatProxy(Real(self.name)).__eq__(other)
            # elif type(other) == str:
            #     return StringProxy(String(self.name)).__eq__(other)
            # elif type(other) == list:
            #     return ListProxy().__eq__(other)
            return self.get_proxy(other).__eq__(other)
        
    def __ne__(self, other):
        return not self.__eq__(other)
    def __gt__(self, other):
        return self.get_proxy(other).__gt__(other)
    def __ge__(self, other):
        return self.get_proxy(other).__ge__(other)
    def __lt__(self, other):
        return self.get_proxy(other).__lt__(other)
    def __le__(self, other):
        return self.get_proxy(other).__le__(other)

    def _convert(self, other):
        pass