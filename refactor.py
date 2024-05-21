import argparse
import ast

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
            if isinstance(node.body[0], ast.Assign) or isinstance(node.body[0], ast.Expr):
                node = transform_Ifexp(node) # 7. Ifexp
            elif isinstance(node.body[0], ast.Return):
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
    

def perform_comprehension(body, lineno=1):
    comprehension_map={"append":[ast.ListComp, ast.Add()], "add":[ast.SetComp, ast.BitOr()]}
    updated_body = []
    for stmt in body:
        stmt.lineno = lineno

        if isinstance(stmt, ast.For):
            # Gather comprehensions for all lists used in the loop
            comprehensions_to_add = []

            for node in stmt.body:
                node.lineno = lineno + 1
                if (isinstance(node, ast.Expr) and isinstance(node.value, ast.Call)
                        and isinstance(node.value.func, ast.Attribute) and node.value.func.attr in comprehension_map):
                    name = node.value.func.value.id
                    comprehension = comprehension_map[node.value.func.attr][0](
                        elt=node.value.args[0],
                        generators=[ast.comprehension(
                            target=stmt.target,
                            iter=stmt.iter,
                            ifs=[],
                            is_async=0
                        )]
                    )
                    comprehension_assignment = ast.AugAssign(
                        target=ast.Name(id=name, ctx=ast.Store()),
                        op=comprehension_map[node.value.func.attr][1],
                        value=comprehension
                    )
                    comprehensions_to_add.append(ast.unparse(comprehension_assignment))
                elif isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Subscript):
                    dict_name = node.targets[0].value.id
                    key = node.targets[0].slice.value if isinstance(node.targets[0].slice, ast.Index) else node.targets[0].slice
                    value = node.value
                    temp_dict_name = f"temp_{dict_name}"
                    comprehension = ast.DictComp(
                        key=key,
                        value=value,
                        generators=[ast.comprehension(
                            target=stmt.target,
                            iter=stmt.iter,
                            ifs=[],
                            is_async=0
                        )]
                    )
                    comprehension.lineno = lineno + 2
                    comprehension_assignment = ast.Assign(
                        targets=[ast.Name(id=temp_dict_name, ctx=ast.Store())],
                        value=comprehension
                    )
                    update_call = ast.Expr(ast.Call(
                        func=ast.Attribute(value=ast.Name(id=dict_name, ctx=ast.Load()), attr='update', ctx=ast.Load()),
                        args=[ast.Name(id=temp_dict_name, ctx=ast.Load())],
                        keywords=[]
                    ))
                    comprehension_assignment.lineno = lineno + 3
                    comprehensions_to_add.append(ast.unparse(comprehension_assignment))
                    comprehensions_to_add.append(ast.unparse(update_call))
                else:
                    comprehensions_to_add = []
                    break
            if comprehensions_to_add:
                # Insert comprehensions before the loop
                updated_body.extend([ast.parse(c).body[0] for c in comprehensions_to_add])
                continue

        updated_body.append(stmt)
    return updated_body


def transform_chaining_comparisons(node):
    map1= {
        ast.Lt: ast.Gt,
        ast.LtE: ast.GtE,
        ast.Gt: ast.Lt,
        ast.GtE: ast.LtE,
        ast.Eq: ast.Eq,
        ast.NotEq: ast.NotEq
    }
    if isinstance(node, ast.BoolOp) and isinstance(node.op, ast.And):
        comparisons = []
        rest=[]
        for value in node.values:
            if isinstance(value, ast.Compare) and len(value.ops) == 1:
                comparisons.append(value)
            else:
                rest.append(value)

        if not comparisons:
            return node

        # Initialize the left part and gather all ops and comparators
        for cur_comp in comparisons:
            for comp in comparisons:
                if comp==cur_comp:
                    continue
                if ast.unparse(cur_comp.left)==ast.unparse(comp.left):
                    chained_comp = ast.Compare(
                        left=cur_comp.comparators[0],
                        ops=[map1[type(cur_comp.ops[0])](),comp.ops[0]],
                        comparators=[cur_comp.left, comp.comparators[0]]
                    )
                    return chained_comp
                elif ast.unparse(cur_comp.left)==ast.unparse(comp.comparators[0]):
                    chained_comp = ast.Compare(
                        left=cur_comp.comparators[0],
                        ops=[map1[type(cur_comp.ops[0])](),map1[type(comp.ops[0])]()],
                        comparators=[cur_comp.left, comp.left]
                    )
                    return chained_comp
                elif ast.unparse(cur_comp.comparators[0])==ast.unparse(comp.left):
                    chained_comp = ast.Compare(
                        left=cur_comp.left,
                        ops=[cur_comp.ops[0],comp.ops[0]],
                        comparators=[cur_comp.comparators[0], comp.comparators[0]]
                    )
                    return chained_comp
                elif ast.unparse(cur_comp.comparators[0])==ast.unparse(comp.comparators[0]):
                    chained_comp = ast.Compare(
                        left=cur_comp.left,
                        ops=[cur_comp.ops[0],map1[type(comp.ops[0])]()],
                        comparators=[cur_comp.comparators[0], comp.left]
                    )
                    return chained_comp

    return node


def transform_equality_comparisons(node):
    if isinstance(node, ast.BoolOp) and isinstance(node.op, ast.Or):
        equalities = []
        left_name = None

        for value in node.values:
            if (isinstance(value, ast.Compare) and
                    len(value.ops) == 1 and
                    isinstance(value.ops[0], ast.Eq) and
                    isinstance(value.left, ast.Name)):

                if left_name is None:
                    left_name = value.left.id
                elif left_name != value.left.id:
                    return node  # Different left values, do not transform

                equalities.append(value.comparators[0])
            else:
                return node  # Not a valid equality chain, do not transform

        if not equalities:
            return node

        # Create a new 'in' comparison
        in_comparison = ast.Compare(
            left=ast.Name(id=left_name, ctx=ast.Load()),
            ops=[ast.In()],
            comparators=[ast.List(elts=equalities, ctx=ast.Load())]
        )
        return in_comparison

    return node


def transform_list_appends(body):
    updated_body = []
    i = 0
    while i < len(body):
        stmt = body[i]
        if (isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Call) and
                isinstance(stmt.value.func, ast.Attribute) and stmt.value.func.attr == 'append'):

            list_name = stmt.value.func.value.id
            appends = [stmt.value.args[0]]

            j = i + 1
            while j < len(body):
                next_stmt = body[j]
                if (isinstance(next_stmt, ast.Expr) and isinstance(next_stmt.value, ast.Call) and
                        isinstance(next_stmt.value.func, ast.Attribute) and
                        next_stmt.value.func.attr == 'append' and
                        next_stmt.value.func.value.id == list_name):

                    appends.append(next_stmt.value.args[0])
                    j += 1
                else:
                    break

            if len(appends) > 1:
                new_stmt = ast.AugAssign(
                    target=ast.Name(id=list_name, ctx=ast.Store()),
                    op=ast.Add(),
                    value=ast.List(elts=appends, ctx=ast.Load())
                )
                updated_body.append(new_stmt)
                i = j
            else:
                updated_body.append(stmt)
                i += 1
        else:
            updated_body.append(stmt)
            i += 1

    return updated_body


class CodeReplacer(ast.NodeTransformer):
    def __init__(self):
        self.toItem={} # (8)

    def generic_visit(self, node):
        if hasattr(node, 'body') and isinstance(node.body, list):
            node.body = transform_multi_assign(node.body)
        return super().generic_visit(node)

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
    
    def visit_FunctionDef(self, node):
        node.body = perform_comprehension(node.body)
        node.body = transform_list_appends(node.body)
        self.generic_visit(node)
        return node

    def visit_Module(self, node):
        node.body = perform_comprehension(node.body)
        node.body = transform_list_appends(node.body)
        self.generic_visit(node)
        return node

    def visit_If(self, node):
        node.test = transform_equality_comparisons(node.test)
        node.test = transform_chaining_comparisons(node.test)
        node = transform_If(node) # 6, 7, 9
        self.generic_visit(node)
        return node

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Measures coverage.')
    parser.add_argument('-t', '--target', required=True)
    parser.add_argument("remaining", nargs="*")
    args = parser.parse_args()
    ex_dir, file = tuple(args.target.split('/'))
    updated_dir = 'updated/'
    with open(ex_dir+file, "r") as target:
        source_code = target.read()
    replacer = CodeReplacer()
    updated_root = replacer.visit(ast.parse(source_code))
    updated_code = ast.unparse(updated_root)
    output_path = updated_dir+file
    with open(output_path, "w") as new_file:
        new_file.write(updated_code)
