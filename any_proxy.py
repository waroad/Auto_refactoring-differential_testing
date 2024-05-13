from z3 import *

class AnyProxy:
    def __init__(self, name):
        self.name = name
    
    def _convert(self, other):
        pass


# class IntegerProxy:
#     def __init__(self, term):
#         if isinstance(term, str):
#             self.term = Int(term)
#         else:
#             self.term = term

#     def __add__(self, other):
#         if isinstance(other, int):
#             other = IntegerProxy(other)
#         return IntegerProxy(self.term + other.term)
    
#     def __radd__(self, other):
#         return self.__add__(other)
    
#     def __sub__(self, other):
#         if isinstance(other, int):
#             other = IntegerProxy(other)
#         return IntegerProxy(self.term - other.term)

#     def __mul__(self, other):
#         if isinstance(other, int):
#             other = IntegerProxy(other)
#         return IntegerProxy(self.term * other.term)

#     def __rmul__(self, other):
#         return self.__mul__(other)

#     def __mod__(self, other):
#         if isinstance(other, int):
#             other = IntegerProxy(other)
#         return IntegerProxy(self.term % other.term)

#     def __div__(self, other):
#         if isinstance(other, int):
#             other = IntegerProxy(other)
#         return IntegerProxy(self.term / other.term)

#     def __floordiv__(self, other):
#         if isinstance(other, int):
#             other = IntegerProxy(other)
#         return IntegerProxy(self.term // other.term)

#     def __pow__(self, other):
#         if isinstance(other, int):
#             other = IntegerProxy(other)
#         return IntegerProxy(self.term ** other.term)
    
#     def __neg__(self):
#         return IntegerProxy(-self.term)
    
#     def __eq__(self, other):
#         if isinstance(other, int):
#             other = IntegerProxy(other)
#         return BoolProxy(self.term == other.term)
    
#     def __req__(self, other):
#         return self.__eq__(other)
    
#     def __lt__(self, other):
#         if isinstance(other, int):
#             other = IntegerProxy(other)
#         return BoolProxy(self.term < other.term)
    
#     def __gt__(self, other):
#         if isinstance(other, int):
#             other = IntegerProxy(other)
#         return BoolProxy(self.term > other.term)
    
# class StringProxy:
#     def __init__(self, name):
#         self.term = String(name)  # Z3 심볼릭 변수 생성

#     def __add__(self, other):
#         if isinstance(other, StringProxy):
#             return StringProxy(Concat(self.term, other.term))
#         else:
#             raise TypeError("Can only concatenate with StringProxy")

#     def __mul__(self, times):
#         if isinstance(times, int) and times >= 0:
#             result = self.term
#             for _ in range(times - 1):
#                 result = Concat(result, self.term)
#             return StringProxy(result)
#         else:
#             raise ValueError("Can only multiply by a non-negative integer")

#     def __eq__(self, other):
#         if isinstance(other, StringProxy):
#             return BoolProxy(self.term == other.term)
#         elif isinstance(other, str):
#             return BoolProxy(self.term == other)
#         else:
#             return BoolProxy(False)

#     def __len__(self):
#         return Length(self.term)  # Z3의 Length 함수 사용

#     def __contains__(self, item):
#         if isinstance(item, StringProxy):
#             return BoolProxy(Contains(self.term, item.term))
#         else:
#             raise TypeError("Contains method expects a StringProxy")

#     def __str__(self):
#         return f"StringProxy({self.term})"

#     def __repr__(self):
#         return f"StringProxy({repr(self.term)})"
    

# class ListProxy:
#     def __init__(self, iterable=None):
#         if iterable is None:
#             self.items = []
#         else:
#             self.items = list(iterable)

#     def __getitem__(self, index):
#         if isinstance(index, slice):
#             return ListProxy(self.items[index])
#         return self.items[index]

#     def __setitem__(self, index, value):
#         self.items[index] = value

#     def __delitem__(self, index):
#         del self.items[index]

#     def append(self, item):
#         self.items.append(item)

#     def extend(self, iterable):
#         self.items.extend(iterable)

#     def insert(self, index, item):
#         self.items.insert(index, item)

#     def remove(self, item):
#         self.items.remove(item)

#     def pop(self, index=-1):
#         return self.items.pop(index)

#     def clear(self):
#         self.items.clear()

#     def __len__(self):
#         return len(self.items)

#     def __iter__(self):
#         return iter(self.items)

#     def __contains__(self, item):
#         return item in self.items

#     def __str__(self):
#         return str(self.items)

#     def __repr__(self):
#         return f'ListProxy({self.items})'

#     def __eq__(self, other):
#         if isinstance(other, ListProxy):
#             return BoolProxy(self.items == other.items)
#         elif isinstance(other, list):
#             return BoolProxy(self.items == other)
#         else:
#             return BoolProxy(False)

#     def __lt__(self, other):
#         if isinstance(other, ListProxy):
#             return BoolProxy(self.items < other.items)
#         elif isinstance(other, list):
#             return BoolProxy(self.items < other)
#         else:
#             raise TypeError("Comparison only possible with list or ListProxy")

#     def __gt__(self, other):
#         if isinstance(other, ListProxy):
#             return BoolProxy(self.items > other.items)
#         elif isinstance(other, list):
#             return BoolProxy(self.items > other)
#         else:
#             raise TypeError("Comparison only possible with list or ListProxy")

# class SetProxy:
#     def __init__(self, iterable=None):
#         if iterable is None:
#             self.items = set()
#         else:
#             self.items = set(iterable)

#     def add(self, item):
#         self.items.add(item)

#     def discard(self, item):
#         self.items.discard(item)

#     def remove(self, item):
#         if item in self.items:
#             self.items.remove(item)
#         else:
#             raise KeyError("Item not found in the set")

#     def pop(self):
#         return self.items.pop()

#     def clear(self):
#         self.items.clear()

#     def update(self, iterable):
#         self.items.update(iterable)

#     def intersection_update(self, iterable):
#         self.items.intersection_update(iterable)

#     def difference_update(self, iterable):
#         self.items.difference_update(iterable)

#     def symmetric_difference_update(self, iterable):
#         self.items.symmetric_difference_update(iterable)

#     def __len__(self):
#         return len(self.items)

#     def __iter__(self):
#         return iter(self.items)

#     def __contains__(self, item):
#         return BoolProxy(item in self.items)

#     def __str__(self):
#         return str(self.items)

#     def __repr__(self):
#         return f'SetProxy({self.items})'

#     def __eq__(self, other):
#         if isinstance(other, SetProxy):
#             return BoolProxy(self.items == other.items)
#         elif isinstance(other, set):
#             return BoolProxy(self.items == other)
#         else:
#             return BoolProxy(False)

#     def __lt__(self, other):
#         if isinstance(other, SetProxy):
#             return BoolProxy(self.items < other.items)
#         elif isinstance(other, set):
#             return BoolProxy(self.items < other)
#         else:
#             raise TypeError("Comparison only possible with set or SetProxy")

#     def __gt__(self, other):
#         if isinstance(other, SetProxy):
#             return BoolProxy(self.items > other.items)
#         elif isinstance(other, set):
#             return BoolProxy(self.items > other)
#         else:
#             raise TypeError("Comparison only possible with set or SetProxy")

# class DictProxy:
#     def __init__(self, dictionary=None):
#         if dictionary is None:
#             self.items = {}
#         else:
#             self.items = dict(dictionary)

#     def __getitem__(self, key):
#         return self.items[key]

#     def __setitem__(self, key, value):
#         self.items[key] = value

#     def __delitem__(self, key):
#         del self.items[key]

#     def keys(self):
#         return self.items.keys()

#     def values(self):
#         return self.items.values()

#     def items(self):
#         return self.items.items()

#     def get(self, key, default=None):
#         return self.items.get(key, default)

#     def setdefault(self, key, default=None):
#         return self.items.setdefault(key, default)

#     def pop(self, key, default=None):
#         return self.items.pop(key, default)

#     def popitem(self):
#         return self.items.popitem()

#     def update(self, other):
#         if isinstance(other, DictProxy):
#             self.items.update(other.items)
#         elif isinstance(other, dict):
#             self.items.update(other)
#         else:
#             raise ValueError("update() argument must be a dict or DictProxy")

#     def clear(self):
#         self.items.clear()

#     def __contains__(self, key):
#         return BoolProxy(key in self.items)

#     def __len__(self):
#         return len(self.items)

#     def __str__(self):
#         return str(self.items)

#     def __repr__(self):
#         return f'DictProxy({self.items})'

#     def __eq__(self, other):
#         if isinstance(other, DictProxy):
#             return BoolProxy(self.items == other.items)
#         elif isinstance(other, dict):
#             return BoolProxy(self.items == other)
#         else:
#             return BoolProxy(False)

#     def __lt__(self, other):
#         raise NotImplementedError("Less than is not supported between instances of 'DictProxy'")

#     def __gt__(self, other):
#         raise NotImplementedError("Greater than is not supported between instances of 'DictProxy'")

# class TupleProxy:
#     def __init__(self, iterable=None):
#         if iterable is None:
#             self.items = tuple()
#         else:
#             self.items = tuple(iterable)

#     def __getitem__(self, index):
#         return self.items[index]

#     def __len__(self):
#         return len(self.items)

#     def __contains__(self, item):
#         return BoolProxy(item in self.items)

#     def __iter__(self):
#         return iter(self.items)

#     def __str__(self):
#         return str(self.items)

#     def __repr__(self):
#         return f'TupleProxy({self.items})'

#     def __eq__(self, other):
#         if isinstance(other, TupleProxy):
#             return BoolProxy(self.items == other.items)
#         elif isinstance(other, tuple):
#             return BoolProxy(self.items == other)
#         else:
#             return BoolProxy(False)

#     def __lt__(self, other):
#         if isinstance(other, TupleProxy):
#             return BoolProxy(self.items < other.items)
#         elif isinstance(other, tuple):
#             return BoolProxy(self.items < other)
#         else:
#             raise TypeError("Comparison only possible with tuple or TupleProxy")

#     def __gt__(self, other):
#         if isinstance(other, TupleProxy):
#             return BoolProxy(self.items > other.items)
#         elif isinstance(other, tuple):
#             return BoolProxy(self.items > other)
#         else:
#             raise TypeError("Comparison only possible with tuple or TupleProxy")

#     def __hash__(self):
#         return hash(self.items)

# class BoolProxy:
    def __init__(self, formula):
        self.formula = formula


    def __not__(self):
        return BoolProxy(Not(self.formula))
    
    def __and__(self, other):
        if not isinstance(other, BoolProxy):
            other = BoolProxy(bool(other))
        return BoolProxy(And(self.formula, other.formula))

    def __or__(self, other):
        if not isinstance(other, BoolProxy):
            other = BoolProxy(bool(other))
        return BoolProxy(Or(self.formula, other.formula))
    
    def __bool__(self):
        global __path__, __pathcondition__
        s = Solver()
        s.push()
        s.add(__pathcondition__)
        s.add(self.formula)
        true_cond = s.check()
        s.pop()
        
        s.push()
        s.add(__pathcondition__)
        s.add(Not(self.formula))
        false_cond = s.check()
        s.pop()

        if true_cond == sat and false_cond == unsat:
            return True
        
        if false_cond == sat and true_cond == unsat:
            return False
        
        if len(__path__) > len(__pathcondition__):
            branch = __path__[len(__pathcondition__)]
            __pathcondition__.append(self.formula if branch else Not(self.formula))
            return branch
        
        __path__.append(True)
        __pathcondition__.append(self.formula)
        return True