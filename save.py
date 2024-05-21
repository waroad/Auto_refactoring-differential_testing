import ast
import time

def transform_empty_test(node): # (5)
    new_node = node
    comparator = node.comparators[0]
    if isinstance(node.ops[0], ast.Eq): # A==(empty) -> not A
        if isinstance(comparator, (ast.List, ast.Tuple)) and not comparator.elts: # [list] , (tuple)
            new_node = ast.UnaryOp(op=ast.Not(), operand=node.left)
        elif isinstance(comparator, ast.Dict) and not comparator.keys: # {dict}
            new_node = ast.UnaryOp(op=ast.Not(), operand=node.left)
        elif isinstance(comparator, ast.Constant) and not comparator.value: # 'string'
            new_node = ast.UnaryOp(op=ast.Not(), operand=node.left)
    elif isinstance(node.ops[0], ast.NotEq): # A!=(empty) -> A
        if isinstance(comparator, (ast.List, ast.Tuple)) and not comparator.elts: # [list] , (tuple)
            new_node = node.left
        elif isinstance(comparator, ast.Dict) and not comparator.keys: # {dict}
            new_node = node.left
        elif isinstance(comparator, ast.Constant) and not comparator.value: # 'string'
            new_node = node.left
    ast.copy_location(new_node, node)
    return new_node

def transform_If(node): # (6, 7, 9)
    if len(node.body)==1:
        if isinstance(node.body[0], ast.If) and not node.orelse and not node.body[0].orelse:
            node = transform_nestedIf(node) # 6. NestedIf
        elif node.orelse:
            node = transform_Ifexp(node) # 7. Ifexp
            node = transform_return_boolean(node) # 9. Return Boolean Statement 
    return node

def transform_nestedIf(node): # (6)
    new_test = ast.BoolOp(op=ast.And(), values=[node.test, node.body[0].test])
    new_node = ast.If(test=new_test, body=node.body[0].body, orelse=node.body[0].orelse)
    ast.copy_location(new_node, node)
    return new_node

def transform_Ifexp(node):
    new_node = node
    if isinstance(node.body[0], ast.Assign) and isinstance(node.orelse[0], ast.Assign): # (7) Assign
        if len(node.body[0].targets)==1 and len(node.orelse[0].targets)==1 and isinstance(node.body[0].targets[0], ast.Name) and isinstance(node.orelse[0].targets[0], ast.Name):
            if node.body[0].targets[0].id == node.orelse[0].targets[0].id:
                new_exp = ast.IfExp(test=node.test, body=node.body[0].value, orelse=node.orelse[0].value)
                new_node = ast.Assign(targets=node.body[0].targets, value=new_exp)
    elif isinstance(node.body[0], ast.Expr) and isinstance(node.orelse[0], ast.Expr): # (7) print
        if isinstance(node.body[0].value, ast.Call) and isinstance(node.orelse[0].value, ast.Call):
            if isinstance(node.body[0].value.func, ast.Name) and isinstance(node.orelse[0].value.func, ast.Name):
                if node.body[0].value.func.id=='print' and node.orelse[0].value.func.id=='print':
                    new_exp = ast.IfExp(test=node.test, body=node.body[0].value.args[0], orelse=node.orelse[0].value.args[0])
                    new_node = ast.Expr(value=ast.Call(func = node.body[0].value.func, args=[new_exp], keywords=[]))
    ast.copy_location(new_node, node)
    return new_node

def transform_toEnumerate(self, node): # (8)
    list_id, new_node = '', node
    if isinstance(node.iter, ast.Call):
            if isinstance(node.iter.func, ast.Name):
                if node.iter.func.id=='range':
                    if isinstance(node.iter.args[0], ast.Call):
                        if isinstance(node.iter.args[0].func, ast.Name):
                            if node.iter.args[0].func.id=='len':
                                if isinstance(node.iter.args[0].args[0], ast.Name):
                                    list_id=node.iter.args[0].args[0].id
                                    self.toItem[list_id]=node.target.id
                                    new_target = ast.Tuple(elts=[node.target, ast.Name(id='item', ctx=ast.Store())])
                                    ast.copy_location(new_target, node.target)
                                    new_iter = node.iter.args[0]
                                    new_iter.func=ast.Name(id='enumerate', ctx=ast.Load())
                                    new_node = ast.For(target=new_target, iter=new_iter, body=node.body, orelse=node.orelse)
                                    ast.copy_location(new_node, node)
    return list_id, new_node

def transform_to_item(self, node): # (8)
    new_node = node
    if node.value.id in self.toItem and isinstance(node.slice, ast.Name):
        if node.slice.id==self.toItem[node.value.id]:
            new_node = ast.Name(id='item', ctx=ast.Store())
    ast.copy_location(new_node, node)
    return new_node

def keep_assign_left(self, targets): # (8)
    if isinstance(targets[0], ast.Subscript):
            if targets[0].value.id in self.toItem and isinstance(targets[0].slice, ast.Name):
                if targets[0].slice.id==self.toItem[targets[0].value.id]:
                    return True
    return False

def transform_return_boolean(node): # (9)
    new_node = node
    if isinstance(node.body[0], ast.Return) and isinstance(node.orelse[0], ast.Return):
        if isinstance(node.body[0].value, ast.Constant) and isinstance(node.orelse[0].value, ast.Constant):
            if node.body[0].value.value==True and node.orelse[0].value.value==False:
                new_node = ast.Return(value=node.test)
    ast.copy_location(new_node, node)
    return new_node

def transform_multi_assign(body): # (10)
    new_stmts, temp_targets, temp_values, first_node = [], [], [], None
    for stmt in body:
        if isinstance(stmt, ast.Assign) and len(stmt.targets)==1:
            if first_node is None:
                first_node=stmt
            temp_targets.append(stmt.targets[0])
            temp_values.append(stmt.value)
        else:
            if temp_targets:
                new_assign = ast.Assign(targets=[ast.Tuple(elts=temp_targets, ctx=ast.Store())], value=ast.Tuple(elts=temp_values, ctx=ast.Load()))
                ast.copy_location(new_assign, first_node)
                if len(temp_targets)==1:
                    new_assign = first_node
                new_stmts.append(new_assign)
                temp_targets=[]
                temp_values=[]
                first_node=None
            new_stmts.append(stmt)
    if temp_targets:
        new_assign = ast.Assign(targets=[ast.Tuple(elts=temp_targets, ctx=ast.Store())], value=ast.Tuple(elts=temp_values, ctx=ast.Load()))
        ast.copy_location(new_assign, first_node)
        if len(temp_targets)==1:
            new_assign = first_node
        new_stmts.append(new_assign)
    return new_stmts
    
class CodeTF(ast.NodeTransformer):
    def __init__(self):
        self.toItem={} # (8)

    def generic_visit(self, node):
        if hasattr(node, 'body'):
            node.body = transform_multi_assign(node.body)
        return super().generic_visit(node)

    def visit_If(self, node):
        # node.body = transform_multi_assign(node.body)
        node = transform_If(node) # 6, 7, 9
        print('hs1', ast.unparse(node))
        self.generic_visit(node)
        print('hs2', ast.unparse(node))
        return node
    
    def visit_Module(self, node):
        # node.body = transform_multi_assign(node.body)
        self.generic_visit(node)
        return node

    def visit_Compare(self, node): # 5. Truth Value Test
        node = transform_empty_test(node)
        self.generic_visit(node)
        return node
    
    def visit_For(self, node): # 8. toEnumerate
        list_id, node = transform_toEnumerate(self, node)
        self.generic_visit(node)
        self.toItem.pop(list_id, None)
        return node
    
    def visit_Subscript(self, node): # change body (8).
        node = transform_to_item(self, node)
        self.generic_visit(node)
        return node
    
    def visit_Assign(self, node): # handle exception (8). 
        result = keep_assign_left(self, node.targets)
        if result:
            return node
        return self.generic_visit(node)


code ='''
A, B = (1, 2), [1, 2]
if A==[]:
    print(1)
elif B!=():
    print(2)
'''
# condition=1
# (a,b,c)=(1,2,3) if condition else (3,2,1)
# print(a,b,c)
# print('code0 :')
# print(code)
tree = ast.parse(code)
file=ast.dump(tree, indent=2)
with open ('before.txt', 'w') as result:
    result.write(file)
time.sleep(0.5)
tree1 = CodeTF().visit(tree)
with open ('after.txt', 'w') as result:
    result.write(file)
code1 = ast.unparse(tree1)
print('changed :')
print(code1)