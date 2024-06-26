import argparse
import sys
import path_list
from z3 import *

# 1. Implement peer lightweight symbolic execution engine
class IntegerProxy:
    def __init__(self, term):
        self.term = term
        path_list.__typedict__[term.decl().name()] = int
    
    def __pos__(self):
        return IntegerProxy(+ self.term)
    def __neg__(self):
        return IntegerProxy(- self.term)
    def __abs__(self):
        return IntegerProxy(Abs(self.term))
    def __int__(self):
        solver = Solver()
        solver.add(path_list.__pathcondition__)
        solver.add(self.term >= 0)
        if solver.check() == sat:
            model = solver.model()
            return model.evaluate(self.term).as_long()
        else:
            raise ValueError("The term cannot be evaluated as an integer")

    def __bool__(self):
        return BoolProxy(self.term != 0).__bool__()

    def __add__(self, other):
        if isinstance(other, (IntegerProxy, FloatProxy)):
            return IntegerProxy(self.term + other.term)
        elif isinstance(other, (int, float)):
            return IntegerProxy(self.term + other)
        else:
            other = IntegerProxy(Int(other.name))
            return IntegerProxy(self.term + other.term)

    def __radd__(self, other):
        return self.__add__(other)
    def __sub__(self, other):
        if isinstance(other, (IntegerProxy, FloatProxy)):
            return IntegerProxy(self.term - other.term)
        elif isinstance(other, (int, float)):
            return IntegerProxy(self.term - other)
        else:
            other = IntegerProxy(Int(other.name))
            return IntegerProxy(self.term - other.term)
    def __rsub__(self, other):
        return self.__sub__(other)
    def __mul__(self, other):
        if isinstance(other, (IntegerProxy, FloatProxy)):
            return IntegerProxy(self.term * other.term)
        elif isinstance(other, (int, float)):
            return IntegerProxy(self.term * other)
        else:
            other = IntegerProxy(Int(other.name))
            return IntegerProxy(self.term * other.term)
    def __floordiv__(self, other):
        if isinstance(other, (IntegerProxy, FloatProxy)):
            return IntegerProxy(self.term / other.term)
        elif isinstance(other, (int, float)):
            return IntegerProxy(self.term / other)
        else:
            other = IntegerProxy(Int(other.name))
            return IntegerProxy(self.term / other.term)
    def __rmul__(self, other):
        return self.__mul__(other)
    def __div__(self, other):
        if isinstance(other, (IntegerProxy, FloatProxy)):
            return FloatProxy(self.term / other.term)
        elif isinstance(other, (int, float)):
            return FloatProxy(self.term / other)
        else:
            other = FloatProxy(Int(other.name))
            return FloatProxy(self.term / other.term)
    def __rdiv__(self, other):
        return self.__div__(other)
    def __truediv__(self, other):
        if isinstance(other, (IntegerProxy, FloatProxy)):
            return FloatProxy(self.term / other.term)
        elif isinstance(other, (int, float)):
            return FloatProxy(self.term / other)
        else:
            other = FloatProxy(Int(other.name))
            return FloatProxy(self.term / other.term)
    def __rtruediv__(self, other):
        return self.__truediv__(other)

    def __divmod__(self, other):
        if isinstance(other, IntegerProxy):
            return IntegerProxy(self.term / other.term), IntegerProxy(self.term % other.term)
        elif isinstance(other, int):
            return IntegerProxy(self.term / other), IntegerProxy(self.term % other)
        else:
            raise TypeError("divmod anyproxy")
    def __rdivmod__(self, other):
        return self.__divmod__(other)
    
    def __pow__(self, other):
        if isinstance(other, IntegerProxy):
            return IntegerProxy(self.term ** other.term)
        elif isinstance(other, int):
            return IntegerProxy(self.term ** other)
        else:
            raise TypeError("divmod anyproxy")
    def __rpow__(self, other):
        return self.__pow__(other)
    def __mod__(self, other):
        if isinstance(other, IntegerProxy):
            return IntegerProxy(self.term % other.term)
        elif isinstance(other, int):
            return IntegerProxy(self.term % other)
        else:
            raise TypeError("divmod anyproxy")
    def __rmod__(self, other):
        return self.__mod__(other)
    def __gt__(self, other):
        if isinstance(other, (IntegerProxy, FloatProxy)):
            return BoolProxy(self.term > other.term)
        elif isinstance(other, (int, float)):
            return BoolProxy(self.term > other)
        elif isinstance(other, str):
            return BoolProxy(self.term > int(other))
        else:
            raise TypeError("divmod anyproxy")
    def __ge__(self, other):
        if isinstance(other, (IntegerProxy, FloatProxy)):
            return BoolProxy(self.term >= other.term)
        elif isinstance(other, (int, float)):
            return BoolProxy(self.term >= other)
        else:
            raise TypeError("divmod anyproxy")
    def __lt__(self, other):
        if isinstance(other, (IntegerProxy, FloatProxy)):
            return BoolProxy(self.term < other.term)
        elif isinstance(other, (int, float)):
            return BoolProxy(self.term < other)
        else:
            raise TypeError("divmod anyproxy")
    def __le__(self, other):
        if isinstance(other, (IntegerProxy, FloatProxy)):
            return BoolProxy(self.term <= other.term)
        elif isinstance(other, (int, float)):
            return BoolProxy(self.term <= other)
        else:
            raise TypeError("divmod anyproxy")
    def __eq__(self, other):
        if isinstance(other, (IntegerProxy, FloatProxy)):
            return BoolProxy(self.term == other.term)
        elif isinstance(other, (int, float)):
            return BoolProxy(self.term == other)
        else:
            raise TypeError("divmod anyproxy")
    def __ne__(self, other):
        if isinstance(other, (IntegerProxy, FloatProxy)):
            return BoolProxy(self.term != other.term)
        elif isinstance(other, (int, float)):
            return BoolProxy(self.term != other)
        else:
            raise TypeError("divmod anyproxy")
    
    def __index__(self):
        solver = Solver()
        solver.add(path_list.__pathcondition__ + [self.term > 0])
        if solver.check() == sat:
            m = solver.model()
            # Evaluate the term with the model values
            return self.evaluate_term(m, self.term)
        else:
            raise ValueError("Solver could not find a solution that satisfies the conditions.")
    
    def evaluate_term(self, model, term):
        # print(term.decl().kind(), term)
        # return term.decl().kind(), [arg for arg in term.children()]
        if term.decl().kind() == Z3_OP_ADD:
            return sum(self.evaluate_term(model, arg) for arg in term.children())
        elif term.decl().kind() == Z3_OP_SUB:
            return self.evaluate_term(model, term.arg(0)) - self.evaluate_term(model, term.arg(1))
        elif term.decl().kind() == Z3_OP_MUL:
            return self.evaluate_term(model, term.arg(0)) * self.evaluate_term(model, term.arg(1))
        elif term.decl().kind() == Z3_OP_DIV:
            return self.evaluate_term(model, term.arg(0)) // self.evaluate_term(model, term.arg(1))
        elif term.decl().kind() == Z3_OP_IDIV:
            return self.evaluate_term(model, term.arg(0)) / self.evaluate_term(model, term.arg(1))
        elif term.decl().kind() == Z3_OP_UNINTERPRETED:
            return model[term].as_long()
        elif term.decl().kind() == Z3_OP_ANUM:
            return int(term.as_long())
        elif term.decl().kind() == Z3_OP_GE:  # Greater than or equal
            return self.evaluate_term(model, term.arg(0)) >= self.evaluate_term(model, term.arg(1))
        elif term.decl().kind() == Z3_OP_GT:  # Greater than
            return self.evaluate_term(model, term.arg(0)) > self.evaluate_term(model, term.arg(1))
        elif term.decl().kind() == Z3_OP_LE:  # Less than or equal
            return self.evaluate_term(model, term.arg(0)) <= self.evaluate_term(model, term.arg(1))
        elif term.decl().kind() == Z3_OP_LT:  # Less than
            return self.evaluate_term(model, term.arg(0)) < self.evaluate_term(model, term.arg(1))
        else:
            raise NotImplementedError(f"Unsupported operation: {term.decl().kind()}")

class FloatProxy:
    def __init__(self, term):
        self.term = term
        path_list.__typedict__[term.decl().name()] = float
    
    def __pos__(self):
        return FloatProxy(+ self.term)
    def __neg__(self):
        return FloatProxy(- self.term)
    def __abs__(self):
        return FloatProxy(Abs(self.term))
    def __bool__(self):
        return BoolProxy(self.term == Real(0))
    def __int__(self):
        solver = Solver()
        solver.add(path_list.__pathcondition__)
        solver.add(self.term >= 0)
        if solver.check() == sat:
            model = solver.model()
            return model.evaluate(self.term).as_long()
        else:
            raise ValueError("The term cannot be evaluated as an integer")
    def __add__(self, other):
        if isinstance(other, (IntegerProxy, FloatProxy)):
            return FloatProxy(self.term + other.term)
        elif isinstance(other, (int, float)):
            return FloatProxy(self.term + other)
        else:
            raise TypeError("divmod anyproxy")
    def __radd__(self, other):
        return self.__add__(other)
    def __sub__(self, other):
        if isinstance(other, (IntegerProxy, FloatProxy)):
            return FloatProxy(self.term - other.term)
        elif isinstance(other, (int, float)):
            return FloatProxy(self.term - other)
        else:
            raise TypeError("divmod anyproxy")
    def __rsub__(self, other):
        return self.__sub__(other)
    def __mul__(self, other):
        if isinstance(other, (IntegerProxy, FloatProxy)):
            return FloatProxy(self.term * other.term)
        elif isinstance(other, (int, float)):
            return FloatProxy(self.term * other)
        else:
            raise TypeError("divmod anyproxy")
    def __rmul__(self, other):
        return self.__mul__(other)
    def __div__(self, other):
        if isinstance(other, (IntegerProxy, FloatProxy)):
            return FloatProxy(self.term / other.term)
        elif isinstance(other, (int, float)):
            return FloatProxy(self.term / other)
        else:
            raise TypeError("divmod anyproxy")
    def __rdiv__(self, other):
        return self.__div__(other)
    def __truediv__(self, other):
        if isinstance(other, (IntegerProxy, FloatProxy)):
            return FloatProxy(self.term / other.term)
        elif isinstance(other, (int, float)):
            return FloatProxy(self.term / other)
        else:
            raise TypeError("divmod anyproxy")
    def __rtruediv__(self, other):
        return self.__truediv__(other)

    def __divmod__(self, other):
        if isinstance(other, (IntegerProxy, FloatProxy)):
            return FloatProxy(self.term / other.term), FloatProxy(self.term % other.term)
        elif isinstance(other, int):
            return FloatProxy(self.term / other), FloatProxy(self.term % other)
        else:
            raise TypeError("divmod anyproxy")
    def __rdivmod__(self, other):
        return self.__divmod__(other)
    
    def __pow__(self, other):
        if isinstance(other, (IntegerProxy, FloatProxy)):
            return FloatProxy(self.term ** other.term)
        elif isinstance(other, int):
            return FloatProxy(self.term ** other)
        else:
            raise TypeError("divmod anyproxy")
    def __rpow__(self, other):
        return self.__pow__(other)
    def __mod__(self, other):
        if isinstance(other, (IntegerProxy, FloatProxy)):
            return FloatProxy(self.term % other.term)
        elif isinstance(other, int):
            return FloatProxy(self.term % other)
        else:
            raise TypeError("divmod anyproxy")
    def __rmod__(self, other):
        return self.__mod__(other)
    def __gt__(self, other):
        if isinstance(other, (IntegerProxy, FloatProxy)):
            return BoolProxy(self.term > other.term)
        elif isinstance(other, (int, float)):
            return BoolProxy(self.term > other)
        else:
            raise TypeError("divmod anyproxy")
    def __ge__(self, other):
        if isinstance(other, (IntegerProxy, FloatProxy)):
            return BoolProxy(self.term >= other.term)
        elif isinstance(other, (int, float)):
            return BoolProxy(self.term >= other)
        else:
            raise TypeError("divmod anyproxy")
    def __lt__(self, other):
        if isinstance(other, (IntegerProxy, FloatProxy)):
            return BoolProxy(self.term < other.term)
        elif isinstance(other, (int, float)):
            return BoolProxy(self.term < other)
        else:
            raise TypeError("divmod anyproxy")
    def __le__(self, other):
        if isinstance(other, (IntegerProxy, FloatProxy)):
            return BoolProxy(self.term <= other.term)
        elif isinstance(other, (int, float)):
            return BoolProxy(self.term <= other)
        else:
            raise TypeError("divmod anyproxy")
    def __eq__(self, other):
        if isinstance(other, (IntegerProxy, FloatProxy)):
            return BoolProxy(self.term == other.term)
        elif isinstance(other, (int, float)):
            return BoolProxy(self.term == other)
        else:
            raise TypeError("divmod anyproxy")
    def __ne__(self, other):
        if isinstance(other, (IntegerProxy, FloatProxy)):
            return BoolProxy(self.term != other.term)
        elif isinstance(other, (int, float)):
            return BoolProxy(self.term != other)
        else:
            raise TypeError("divmod anyproxy")
        
class StringProxy:
    def __init__(self, term):
        self.term = term
        path_list.__typedict__[term.decl().name()] = str

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
        else:
            raise TypeError("divmod anyproxy")
    def __ge__(self, other):
        if isinstance(other, StringProxy):
            return BoolProxy(self.term >= other.term)
        elif isinstance(other, str):
            return BoolProxy(self.term >= other)
        else:
            raise TypeError("divmod anyproxy")
    def __lt__(self, other):
        if isinstance(other, StringProxy):
            return BoolProxy(self.term < other.term)
        elif isinstance(other, str):
            return BoolProxy(self.term < other)
        else:
            raise TypeError("divmod anyproxy")
    def __le__(self, other):
        if isinstance(other, StringProxy):
            return BoolProxy(self.term <= other.term)
        elif isinstance(other, str):
            return BoolProxy(self.term <= other)
        else:
            raise TypeError("divmod anyproxy")
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
    def __getitem__(self, index):
        if isinstance(index, int):
            return self.term[index]
        elif isinstance(index, slice):
            return StringProxy(self.term[index])
        else:
            raise TypeError("Invalid index type")
        
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
    def __init__(self, term, name):
        self.term = term
        self.name = name
    def __len__(self):
        return len(self.term)
    def __eq__(self, other):
        if isinstance(other, ListProxy):
            condition_list = [len(self.term) == len(other.term)]
            for i in range(len(self.term)):
                condition_list.append(self.term[i] == other.term[i])
            return BoolProxy(And(*condition_list))
        elif isinstance(other, list):
            condition_list = [Int(f'{self.name}_length') == len(other)]
            for i in range(len(self.term)):
                condition_list.append(self.term[i] == other[i])
            return BoolProxy(And(*condition_list))
        else:
            return BoolProxy(False)
    def __ne__(self, other):
        return not self.__eq__(other)
    def __getitem__(self, index):
        if isinstance(index, int):
            if isinstance(self.term[index], ArithRef):
                return IntegerProxy(Int(self.term[index].decl().name()))
            elif isinstance(self.term[index], IntegerProxy):
                return IntegerProxy(Int(self.term[index].term.decl().name()))
            else:
                raise TypeError(f"Unsupported type is {type(self.term[index])}")
        elif isinstance(index, slice):
            return ListProxy(self.term[index], self.name)
        elif isinstance(index, IntegerProxy):
            index = index.__index__()
            if isinstance(self.term[index], ArithRef):
                return IntegerProxy(Int(self.term[index].decl().name()))
            elif isinstance(self.term[index], IntegerProxy):
                return IntegerProxy(Int(self.term[index].term.decl().name()))
            else:
                raise TypeError(f"type is {type(self.term[index])}")
        else:
            raise TypeError(f"Invalid index type {type(index)}")
    def __setitem__(self, index, value):
        if isinstance(index, int):
            if isinstance(value, int):
                self.term[index] = value
            else:
                self.term[index] = IntegerProxy(value.term)
        elif isinstance(index, slice):
            if isinstance(value, ListProxy):
                self.term[index] = value.term
            else:
                self.term[index] = value
        elif isinstance(index, IntegerProxy):
            index = index.__index__()
            self.term[index] = IntegerProxy(value.term)
        else:
            raise TypeError(f"Invalid index type {type(index)}")
    def __delitem__(self, index):
        del self.term[index]
    def __iter__(self):
        return iter(self.term)
    def __contains__(self, item):
        return item in self.term
    def append(self, item):
        self.term.append(item)
    def extend(self, other):
        if isinstance(other, ListProxy):
            self.term.extend(other.term)
        else:
            self.term.extend(other)
    def insert(self, index, item):
        self.term.insert(index, item)
    def remove(self, item):
        self.term.remove(item)
    def pop(self, index=-1):
        return self.term.pop(index)
    def clear(self):
        self.term.clear()
    def index(self, item, start=0, end=None):
        return self.term.index(item, start, end)
    def count(self, item):
        return self.term.count(item)
    def sort(self, key=None, reverse=False):
        self.term.sort(key=key, reverse=reverse)
    def reverse(self):
        self.term.reverse()
    def copy(self):
        return ListProxy(self.term.copy(), self.name)
    def __add__(self, other):
        if isinstance(other, ListProxy):
            return ListProxy(self.term + other.term, self.name)
        elif isinstance(other, list):
            return ListProxy(self.term + other, self.name)
        else:
            raise TypeError("Unsupported type for addition")
    def __iadd__(self, other):
        if isinstance(other, ListProxy):
            self.term += other.term
        elif isinstance(other, list):
            self.term += other
        else:
            raise TypeError("Unsupported type for in-place addition")
        return self
    def __mul__(self, other):
        if isinstance(other, int):
            return ListProxy(self.term * other, self.name)
        else:
            raise TypeError("Unsupported type for multiplication")
    def __rmul__(self, other):
        return self.__mul__(other)
    def __imul__(self, other):
        if isinstance(other, int):
            self.term *= other
        else:
            raise TypeError("Unsupported type for in-place multiplication")
        return self
    
class TupleProxy:
    def __init__(self, term, name):
        self.term = term
        self.name = name
    def __len__(self):
        return len(self.term)
    def __eq__(self, other):
        if isinstance(other, TupleProxy):
            condition_list = [len(self.term) == len(other.term)]
            for i in range(len(self.term)):
                condition_list.append(self.term[i] == other.term[i])
            return BoolProxy(And(*condition_list))
        elif isinstance(other, tuple):
            condition_list = [Int(f'{self.name}_length') == len(other)]
            for i in range(len(self.term)):
                condition_list.append(self.term[i] == other[i])
            return BoolProxy(And(*condition_list))
        else:
            return BoolProxy(False)
    def __ne__(self, other):
        return not self.__eq__(other)
    def __getitem__(self, index):
        if isinstance(index, int):
            return IntegerProxy(Int(self.term[index].decl().name()))
        elif isinstance(index, slice):
            return TupleProxy(self.term[index], self.name)
        else:
            raise TypeError("Invalid index type")
    def __iter__(self):
        return iter(self.term)
    def __contains__(self, item):
        return item in self.term
    def __iter__(self):
        return iter(self.term)
    def append(self, item):
        self.term.append(item)
    def clear(self):
        self.term.clear()
    def index(self, item, start=0, end=None):
        return self.term.index(item, start, end)
    def count(self, item):
        return self.term.count(item)
    def reverse(self):
        self.term.reverse()
    def __add__(self, other):
        if isinstance(other, TupleProxy):
            return TupleProxy(self.term + other.term, self.name)
        elif isinstance(other, tuple):
            return TupleProxy(self.term + other, self.name)
        else:
            raise TypeError("Unsupported type for addition")
    def __mul__(self, other):
        if isinstance(other, int):
            return TupleProxy(self.term * other, self.name)
        else:
            raise TypeError("Unsupported type for multiplication")
    def __rmul__(self, other):
        return self.__mul__(other)

class SetProxy:
    def __init__(self, term):
        self.term = term
    
    def __contains__(self, item):
        return IsMember(item, self.term)
    
    def __eq__(self, other):
        if isinstance(other, SetProxy):
            return BoolProxy(self.term == other.term)
        elif isinstance(other, set):
            condition_list = [IsMember(element, self.term) for element in other]
            condition_list.append(self.term == SetSort(*other))
            return BoolProxy(And(*condition_list))
        else:
            return BoolProxy(False)

    def add(self, item):
        self.term = SetAdd(self.term, item)

    def remove(self, item):
        raise NotImplementedError("Z3 SetSort does not support removing elements directly.")
    
    def clear(self):
        self.term = EmptySet(IntSort())
    
    def union(self, other):
        if isinstance(other, SetProxy):
            return SetProxy(SetUnion(self.term, other.term))
        elif isinstance(other, set):
            new_set = self.term
            for element in other:
                new_set = SetAdd(new_set, element)
            return SetProxy(new_set)
        else:
            raise TypeError("Unsupported type for union")
    
    def intersection(self, other):
        if isinstance(other, SetProxy):
            return SetProxy(Intersect(self.term, other.term))
        elif isinstance(other, set):
            other_set = SetSort(*other)
            return SetProxy(Intersect(self.term, other_set))
        else:
            raise TypeError("Unsupported type for intersection")
    
    def difference(self, other):
        if isinstance(other, SetProxy):
            return SetProxy(SetDifference(self.term, other.term))
        elif isinstance(other, set):
            other_set = SetSort(*other)
            return SetProxy(SetDifference(self.term, other_set))
        else:
            raise TypeError("Unsupported type for difference")
    
    def issubset(self, other):
        if isinstance(other, SetProxy):
            return BoolProxy(IsSubset(self.term, other.term))
        elif isinstance(other, set):
            other_set = SetSort(*other)
            return BoolProxy(IsSubset(self.term, other_set))
        else:
            raise TypeError("Unsupported type for issubset")
    
    def issuperset(self, other):
        if isinstance(other, SetProxy):
            return BoolProxy(IsSubset(other.term, self.term))
        elif isinstance(other, set):
            other_set = SetSort(*other)
            return BoolProxy(IsSubset(other_set, self.term))
        else:
            raise TypeError("Unsupported type for issuperset")
    
    def __len__(self):
        raise NotImplementedError("Z3 SetSort does not support direct length calculation.")
    
    def __iter__(self):
        raise NotImplementedError("Iteration over Z3 sets is not directly supported.")
    
    def to_z3(self):
        return self.term

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
        if false_cond and not true_cond or len(path_list.__path__) >= 10: 
            return False
        if len(path_list.__path__) > len(path_list.__pathcondition__):
            branch = path_list.__path__[len(path_list.__pathcondition__)]
            path_list.__pathcondition__.append(self.formula if branch else Not(self.formula))
            return branch
        path_list.__path__.append(True)
        path_list.__pathcondition__.append(self.formula)
        return True
