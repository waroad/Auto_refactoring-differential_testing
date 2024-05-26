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
            return IntegerProxy(Int(self.name)), other
        elif isinstance(other, (float, FloatProxy)):
            return FloatProxy(Real(self.name)), other
        elif isinstance(other, (str, StringProxy)):
            return StringProxy(String(self.name)), other
        elif isinstance(other, (list, ListProxy)):
            return ListProxy([]), other
        elif isinstance(other, AnyProxy):
            other = IntegerProxy(Int(other.name))
            return IntegerProxy(Int(self.name)), other
        else:
            raise TypeError("Unsupported type")
    
    def __add__(self, other):
        s, o = self.get_proxy(other)
        return s.__add__(o)
    def __radd__(self, other):
        return self.__add__(other)
    def __sub__(self, other):
        if isinstance(other, (int, IntegerProxy, float, FloatProxy)):
            s, o = self.get_proxy(other)
            return s.__sub__(o)
        return TypeError("Unsupported type")
    def __rsub__(self, other):
        return self.__sub__(other)
    def __mul__(self, other):
        if isinstance(other, (int, IntegerProxy, float, FloatProxy)):
            s, o = self.get_proxy(other)
            return s.__mul__(o)
        return TypeError("Unsupported type")
    def __rmul__(self, other):
        return self.__mul__(other)
    def __div__(self, other):
        if isinstance(other, (int, IntegerProxy, float, FloatProxy)):
            s, o = self.get_proxy(other)
            return s.__div__(o)
        return TypeError("Unsupported type")
    def __rdiv__(self, other):
        return self.__div__(other)
    def __truediv__(self, other):
        if isinstance(other, (int, IntegerProxy, float, FloatProxy)):
            s, o = self.get_proxy(other)
            return s.__truediv__(o)
        return TypeError("Unsupported type")
    def __rtruediv__(self, other):
        return self.__truediv__(other)
    def __divmod__(self, other):
        if isinstance(other, (int, IntegerProxy, float, FloatProxy)):
            s, o = self.get_proxy(other)
            return s.__rdivmod__(o)
        return TypeError("Unsupported type")
    def __rdivmod__(self, other):
        return self.__divmod__(other)
    
    def __pow__(self, other):
        if isinstance(other, (int, IntegerProxy, float, FloatProxy)):
            s, o = self.get_proxy(other)
            return s.__pow__(o)
        return TypeError("Unsupported type")
    def __rpow__(self, other):
        return self.__pow__(other)
    def __mod__(self, other):
        if isinstance(other, (int, IntegerProxy, float, FloatProxy)):
            s, o = self.get_proxy(other)
            return s.__mod__(o)
        return TypeError("Unsupported type")
    def __rmod__(self, other):
        return self.__mod__(other)
    
    def __len__(self):
        return len(ListProxy([]))
    
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
    
    def __bool__(self):
        return IntegerProxy(Int(self.name)).__bool__()

    def _convert(self, other):
        pass