import argparse
import sys

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
    # def __invert__(self):

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
        if isinstance(other, IntegerProxy):
            return BoolProxy(self.term > other.term)
        elif isinstance(other, int):
            return BoolProxy(self.term > other)
    def __ge__(self, other):
        if isinstance(other, IntegerProxy):
            return BoolProxy(self.term >= other.term)
        elif isinstance(other, int):
            return BoolProxy(self.term >= other)
    def __lt__(self, other):
        if isinstance(other, IntegerProxy):
            return BoolProxy(self.term < other.term)
        elif isinstance(other, int):
            return BoolProxy(self.term < other)
    def __le__(self, other):
        if isinstance(other, IntegerProxy):
            return BoolProxy(self.term <= other.term)
        elif isinstance(other, int):
            return BoolProxy(self.term <= other)
    def __eq__(self, other):
        if isinstance(other, IntegerProxy):
            return BoolProxy(self.term == other.term)
        elif isinstance(other, int):
            return BoolProxy(self.term == other)
    def __ne__(self, other):
        if isinstance(other, IntegerProxy):
            return BoolProxy(self.term != other.term)
        elif isinstance(other, int):
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
    # def __invert__(self):

    def __bool__(self):
        if self.__eq__(self.term, Real(0)):
            return BoolProxy(True)
        else:
            return BoolProxy(False)

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
        elif isinstance(other, int):
            return BoolProxy(self.term > other)
    def __ge__(self, other):
        if isinstance(other, (IntegerProxy, FloatProxy)):
            return BoolProxy(self.term >= other.term)
        elif isinstance(other, int):
            return BoolProxy(self.term >= other)
    def __lt__(self, other):
        if isinstance(other, (IntegerProxy, FloatProxy)):
            return BoolProxy(self.term < other.term)
        elif isinstance(other, int):
            return BoolProxy(self.term < other)
    def __le__(self, other):
        if isinstance(other, (IntegerProxy, FloatProxy)):
            return BoolProxy(self.term <= other.term)
        elif isinstance(other, int):
            return BoolProxy(self.term <= other)
    def __eq__(self, other):
        if isinstance(other, (IntegerProxy, FloatProxy)):
            return BoolProxy(self.term == other.term)
        elif isinstance(other, int):
            return BoolProxy(self.term == other)
    def __ne__(self, other):
        if isinstance(other, (IntegerProxy, FloatProxy)):
            return BoolProxy(self.term != other.term)
        elif isinstance(other, int):
            return BoolProxy(self.term != other)

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
        global __path__, __pathcondition__
        s_true = Solver()
        s_true.add(__pathcondition__ + [self.formula])
        s_false = Solver()
        s_false.add(__pathcondition__ + [Not(self.formula)])

        true_cond = True if s_true.check() == sat else False
        false_cond = True if s_false.check() == sat else False

        if true_cond and not false_cond: return True
        if false_cond and not true_cond: 
            return False

        if len(__path__) > len(__pathcondition__):
            branch = __path__[len(__pathcondition__)]
            __pathcondition__.append(self.formula if branch else Not(self.formula))
            return branch
        
        __path__.append(True)
        __pathcondition__.append(self.formula)
        return True

print((Int))

print(math.floor(3))