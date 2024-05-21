import argparse
import sys
import path_list
from z3 import *

# 1. Implement peer lightweight symbolic execution engine
class IntegerProxy:
    def __init__(self, term):
        self.term = term
    
    def __pos__(self):
        return IntegerProxy(+ self.term)
    def __neg__(self):
        return IntegerProxy(- self.term)
    def __abs__(self):
        return IntegerProxy(Abs(self.term))
    
    def __bool__(self):
        if self.__eq__(self.term, Int(0)):
            return BoolProxy(True)
        else:
            return BoolProxy(False)

    def __add__(self, other):
        if isinstance(other, IntegerProxy):
            return IntegerProxy(self.term + other.term)
        elif isinstance(other, int):
            return IntegerProxy(self.term + other)
    def __radd__(self, other):
        return self.__add__(other)
    def __sub__(self, other):
        if isinstance(other, IntegerProxy):
            return IntegerProxy(self.term - other.term)
        elif isinstance(other, int):
            return IntegerProxy(self.term - other)
    def __rsub__(self, other):
        return self.__sub__(other)
    def __mul__(self, other):
        if isinstance(other, IntegerProxy):
            return IntegerProxy(self.term * other.term)
        elif isinstance(other, int):
            return IntegerProxy(self.term * other)
    def __rmul__(self, other):
        return self.__mul__(other)
    def __div__(self, other):
        if isinstance(other, IntegerProxy):
            return FloatProxy(self.term / other.term)
        elif isinstance(other, int):
            return FloatProxy(self.term / other)
    def __rdiv__(self, other):
        return self.__div__(other)
    def __truediv__(self, other):
        if isinstance(other, IntegerProxy):
            return IntegerProxy(self.term / other.term)
        elif isinstance(other, int):
            return IntegerProxy(self.term / other)
    def __rtruediv__(self, other):
        return self.__truediv__(other)

    def __divmod__(self, other):
        if isinstance(other, IntegerProxy):
            return IntegerProxy(self.term / other.term), IntegerProxy(self.term % other.term)
        elif isinstance(other, int):
            return IntegerProxy(self.term / other), IntegerProxy(self.term % other)
    def __rdivmod__(self, other):
        return self.__divmod__(other)
    
    def __pow__(self, other):
        if isinstance(other, IntegerProxy):
            return IntegerProxy(self.term ** other.term)
        elif isinstance(other, int):
            return IntegerProxy(self.term ** other)
    def __rpow__(self, other):
        return self.__pow__(other)
    def __mod__(self, other):
        if isinstance(other, IntegerProxy):
            return IntegerProxy(self.term % other.term)
        elif isinstance(other, int):
            return IntegerProxy(self.term % other)
    def __rmod__(self, other):
        return self.__mod__(other)
    def __gt__(self, other):
        if isinstance(other, (IntegerProxy, FloatProxy)):
            return BoolProxy(self.term > other.term)
        elif isinstance(other, (int, float)):
            return BoolProxy(self.term > other)
    def __ge__(self, other):
        if isinstance(other, (IntegerProxy, FloatProxy)):
            return BoolProxy(self.term >= other.term)
        elif isinstance(other, (int, float)):
            return BoolProxy(self.term >= other)
    def __lt__(self, other):
        if isinstance(other, (IntegerProxy, FloatProxy)):
            return BoolProxy(self.term < other.term)
        elif isinstance(other, (int, float)):
            return BoolProxy(self.term < other)
    def __le__(self, other):
        if isinstance(other, (IntegerProxy, FloatProxy)):
            return BoolProxy(self.term <= other.term)
        elif isinstance(other, (int, float)):
            return BoolProxy(self.term <= other)
    def __eq__(self, other):
        if isinstance(other, (IntegerProxy, FloatProxy)):
            return BoolProxy(self.term == other.term)
        elif isinstance(other, (int, float)):
            return BoolProxy(self.term == other)
    def __ne__(self, other):
        if isinstance(other, (IntegerProxy, FloatProxy)):
            return BoolProxy(self.term != other.term)
        elif isinstance(other, (int, float)):
            return BoolProxy(self.term != other)

class FloatProxy:
    def __init__(self, term):
        self.term = term
    
    def __pos__(self):
        return FloatProxy(+ self.term)
    def __neg__(self):
        return FloatProxy(- self.term)
    def __abs__(self):
        return FloatProxy(Abs(self.term))

    def __bool__(self):
        return BoolProxy(self.term == Real(0))

    def __add__(self, other):
        if isinstance(other, (IntegerProxy, FloatProxy)):
            return FloatProxy(self.term + other.term)
        elif isinstance(other, (int, float)):
            return FloatProxy(self.term + other)
    def __radd__(self, other):
        return self.__add__(other)
    def __sub__(self, other):
        if isinstance(other, (IntegerProxy, FloatProxy)):
            return FloatProxy(self.term - other.term)
        elif isinstance(other, (int, float)):
            return FloatProxy(self.term - other)
    def __rsub__(self, other):
        return self.__sub__(other)
    def __mul__(self, other):
        if isinstance(other, (IntegerProxy, FloatProxy)):
            return FloatProxy(self.term * other.term)
        elif isinstance(other, (int, float)):
            return FloatProxy(self.term * other)
    def __rmul__(self, other):
        return self.__mul__(other)
    def __div__(self, other):
        if isinstance(other, (IntegerProxy, FloatProxy)):
            return FloatProxy(self.term / other.term)
        elif isinstance(other, (int, float)):
            return FloatProxy(self.term / other)
    def __rdiv__(self, other):
        return self.__div__(other)
    def __truediv__(self, other):
        if isinstance(other, (IntegerProxy, FloatProxy)):
            return FloatProxy(self.term / other.term)
        elif isinstance(other, (int, float)):
            return FloatProxy(self.term / other)
    def __rtruediv__(self, other):
        return self.__truediv__(other)

    def __divmod__(self, other):
        if isinstance(other, (IntegerProxy, FloatProxy)):
            return FloatProxy(self.term / other.term), FloatProxy(self.term % other.term)
        elif isinstance(other, int):
            return FloatProxy(self.term / other), FloatProxy(self.term % other)
    def __rdivmod__(self, other):
        return self.__divmod__(other)
    
    def __pow__(self, other):
        if isinstance(other, (IntegerProxy, FloatProxy)):
            return FloatProxy(self.term ** other.term)
        elif isinstance(other, int):
            return FloatProxy(self.term ** other)
    def __rpow__(self, other):
        return self.__pow__(other)
    def __mod__(self, other):
        if isinstance(other, (IntegerProxy, FloatProxy)):
            return FloatProxy(self.term % other.term)
        elif isinstance(other, int):
            return FloatProxy(self.term % other)
    def __rmod__(self, other):
        return self.__mod__(other)
    def __gt__(self, other):
        if isinstance(other, (IntegerProxy, FloatProxy)):
            return BoolProxy(self.term > other.term)
        elif isinstance(other, (int, float)):
            return BoolProxy(self.term > other)
    def __ge__(self, other):
        if isinstance(other, (IntegerProxy, FloatProxy)):
            return BoolProxy(self.term >= other.term)
        elif isinstance(other, (int, float)):
            return BoolProxy(self.term >= other)
    def __lt__(self, other):
        if isinstance(other, (IntegerProxy, FloatProxy)):
            return BoolProxy(self.term < other.term)
        elif isinstance(other, (int, float)):
            return BoolProxy(self.term < other)
    def __le__(self, other):
        if isinstance(other, (IntegerProxy, FloatProxy)):
            return BoolProxy(self.term <= other.term)
        elif isinstance(other, (int, float)):
            return BoolProxy(self.term <= other)
    def __eq__(self, other):
        if isinstance(other, (IntegerProxy, FloatProxy)):
            return BoolProxy(self.term == other.term)
        elif isinstance(other, (int, float)):
            return BoolProxy(self.term == other)
    def __ne__(self, other):
        if isinstance(other, (IntegerProxy, FloatProxy)):
            return BoolProxy(self.term != other.term)
        elif isinstance(other, (int, float)):
            return BoolProxy(self.term != other)
        
class StringProxy:
    def __init__(self, term):
        self.term = term
    def __add__(self, other):
        if isinstance(other, StringProxy):
            return StringProxy(self.term + other.term)
        elif isinstance(other, str):
            return StringProxy(self.term + other)
        else:
            raise TypeError(0)
    def __gt__(self, other):
        if isinstance(other, StringProxy):
            return BoolProxy(self.term > other.term)
        elif isinstance(other, str):
            return BoolProxy(self.term > other)
    def __ge__(self, other):
        if isinstance(other, StringProxy):
            return BoolProxy(self.term >= other.term)
        elif isinstance(other, str):
            return BoolProxy(self.term >= other)
    def __lt__(self, other):
        if isinstance(other, StringProxy):
            return BoolProxy(self.term < other.term)
        elif isinstance(other, str):
            return BoolProxy(self.term < other)
    def __le__(self, other):
        if isinstance(other, StringProxy):
            return BoolProxy(self.term <= other.term)
        elif isinstance(other, str):
            return BoolProxy(self.term <= other)
    def __eq__(self, other):
        if isinstance(other, StringProxy):
            return BoolProxy(self.term == other.term)
        elif isinstance(other, str):
            return BoolProxy(self.term == other)
        else:
            return BoolProxy(False)
    def __contains__(self, other):
        if isinstance(other, StringProxy):
            return BoolProxy(Contains(self.term, other.term))
        elif isinstance(other, str):
            return BoolProxy(Contains(self.term, other))
        else:
            return BoolProxy(False)
        
    def startswith(self, other):
        if isinstance(other, StringProxy):
            return BoolProxy(PrefixOf(other.term, self.term))
        elif isinstance(other, str):
            return BoolProxy(PrefixOf(other, self.term))
        else:
            raise TypeError('startswith first arg must be str or a tuple of str, not int')
    def endswith(self, other):
        if isinstance(other, StringProxy):
            return BoolProxy(SuffixOf(other.term, self.term))
        elif isinstance(other, str):
            return BoolProxy(SuffixOf(other, self.term))
        else:
            raise TypeError('endswith first arg must be str or a tuple of str, not int')
    
    def __len__(self):
        return IntegerProxy(Length(self.term))

class ListProxy:
    def __init__(self, type):
        self.lst = []
        self.type = type
    def __eq__(self, other):
        if isinstance(other, ListProxy):
            if len(self.lst) != len(other.lst):
                return BoolProxy(False)
            for i in range(len(self.lst)):
                if self.lst[i] != other.lst[i]:
                    return BoolProxy(False)
            return BoolProxy(True)
        elif isinstance(other, list):
            if len(self.lst) != len(other):
                return BoolProxy(False)
            for i in range(len(self.lst)):
                if self.lst[i] != other[i]:
                    return BoolProxy(False)
            return BoolProxy(True)
    def __getitem__(self, index):
        return self.lst[index]


class BoolProxy:
    def __init__(self, formula):
        self.formula = formula
    def __and__(self, other):
        if isinstance(other, BoolProxy):
            return BoolProxy(And(self.formula, other.formula))
        elif isinstance(other, bool):
            return BoolProxy(And(self.formula, other))
    def __or__(self, other):
        if isinstance(other, BoolProxy):
            return BoolProxy(Or(self.formula, other.formula))
        elif isinstance(other, bool):
            return BoolProxy(Or(self.formula, other))
    def __not__(self):
        return BoolProxy(Not(self.formula))
    def __bool__(self):
        s_true = Solver()
        s_true.add(path_list.__pathcondition__ + [self.formula])
        s_false = Solver()
        s_false.add(path_list.__pathcondition__ + [Not(self.formula)])

        true_cond = True if s_true.check() == sat else False
        false_cond = True if s_false.check() == sat else False

        if true_cond and not false_cond: return True
        if false_cond and not true_cond: 
            return False

        if len(path_list.__path__) > len(path_list.__pathcondition__):
            branch = path_list.__path__[len(path_list.__pathcondition__)]
            path_list.__pathcondition__.append(self.formula if branch else Not(self.formula))
            return branch
        path_list.__path__.append(True)
        path_list.__pathcondition__.append(self.formula)
        return True

print(dir(list))

# print(math.floor(3))

x = String('x')
# y = String('y')
solve(x[0] == StringVal('a'))