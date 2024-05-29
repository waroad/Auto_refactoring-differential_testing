import os
import contextlib
from proxies import *
from z3 import *
import path_list

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
        self.length = 5

    def get_proxy(self, other):
        if isinstance(other, (int, IntegerProxy)):
            return IntegerProxy(Int(self.name)), other
        elif isinstance(other, (float, FloatProxy)):
            return FloatProxy(Real(self.name)), other
        elif isinstance(other, (str, StringProxy)):
            return StringProxy(String(self.name)), other
        elif isinstance(other, (bool, BoolProxy)):
            return BoolProxy(Int(self.name) != 0), other
        elif isinstance(other, (list, ListProxy)):
            self.length = len(other)
            path_list.__typedict__[self.name] = list
            return ListProxy(IntVector(self.name, self.length), self.name), other
        elif isinstance(other, AnyProxy):
            other = IntegerProxy(Int(other.name))
            return IntegerProxy(Int(self.name)), other
        elif isinstance(other, (tuple, TupleProxy)):
            self.length = len(other)
            path_list.__typedict__[self.name] = tuple
            return TupleProxy(IntVector(self.name, self.length), self.name), other
        elif isinstance(other, (set, SetProxy)):
            self.length = len(other)
            path_list.__typedict__[self.name] = set
            return SetProxy(SetSort(IntSort())), other
        else:
            raise TypeError(f"Unsupported type {type(other)}")
    
    def __neg__(self):
        return IntegerProxy(Int(self.name)).__neg__()
    
    def __add__(self, other):
        s, o = self.get_proxy(other)
        return s.__add__(o)
    def __radd__(self, other):
        return self.__add__(other)
    def __sub__(self, other):
        s, o = self.get_proxy(other)
        return s.__sub__(o)
    def __rsub__(self, other):
        return self.__sub__(other)
    def __mul__(self, other):
        s, o = self.get_proxy(other)
        return s.__mul__(o)
    def __rmul__(self, other):
        return self.__mul__(other)
    def __div__(self, other):
        s, o = self.get_proxy(other)
        return s.__div__(o)
    def __rdiv__(self, other):
        return self.__div__(other)
    def __truediv__(self, other):
        s, o = self.get_proxy(other)
        return s.__truediv__(o)
    def __rtruediv__(self, other):
        return self.__truediv__(other)
    def __divmod__(self, other):
        s, o = self.get_proxy(other)
        return s.__rdivmod__(o)
    def __rdivmod__(self, other):
        return self.__divmod__(other)
    
    def __pow__(self, other):
        s, o = self.get_proxy(other)
        return s.__pow__(o)
    def __rpow__(self, other):
        return self.__pow__(other)
    def __mod__(self, other):
        s, o = self.get_proxy(other)
        return s.__mod__(o)
    def __rmod__(self, other):
        return self.__mod__(other)
    
    def __len__(self):
        path_list.__typedict__[self.name] = list
        return ListProxy(IntVector(self.name, self.length), self.name).__len__()
    
    def __getitem__(self, index):
        if isinstance(index, AnyProxy):
            index = IntegerProxy(Int(index.name))
        return ListProxy(IntVector(self.name, self.length), self.name).__getitem__(index)

    def __index__(self):
        return IntegerProxy(Int(self.name)).__index__()
    
    def __eq__(self, other):
        if callable(other):
            pass
        else:
            s, o = self.get_proxy(other)
            return s.__eq__(o)
    def __ne__(self, other):
        s, o = self.get_proxy(other)
        return s.__ne__(o)
    def __gt__(self, other):
        s, o = self.get_proxy(other)
        return s.__gt__(o)
    def __ge__(self, other):
        s, o = self.get_proxy(other)
        return s.__ge__(o)
    def __lt__(self, other):
        s, o = self.get_proxy(other)
        return s.__lt__(o)
    def __le__(self, other):
        s, o = self.get_proxy(other)
        return s.__le__(o)
    def __and__(self, other):
        s, o = self.get_proxy(other)
        if isinstance(s, IntegerProxy):
            s = BoolProxy(s.term != 0)
        if isinstance(o, IntegerProxy):
            o = BoolProxy(o.term != 0)
        
        return BoolProxy(And(s.formula, o.formula))

    def __or__(self, other):
        s, o = self.get_proxy(other)
        if isinstance(s, IntegerProxy):
            s = BoolProxy(s.term != 0)
        if isinstance(o, IntegerProxy):
            o = BoolProxy(o.term != 0)
        
        return BoolProxy(Or(s.formula, o.formula))

    def __bool__(self):
        return IntegerProxy(Int(self.name)).__bool__()

    def __setitem__(self, index, value):
        if isinstance(index, AnyProxy):
            index = IntegerProxy(Int(index.name))
        return ListProxy(IntVector(self.name, self.length), self.name).__setitem__(index, value)
    
    def _convert(self, other):
        pass