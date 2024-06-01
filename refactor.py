import argparse
import ast
import time
import os

def transform_empty_test(node):  # (5)
    new_node = node
    comparator = node.comparators[0]
    if isinstance(node.ops[0], ast.Eq):  # A==(empty) -> not A
        if isinstance(comparator, (ast.List, ast.Tuple)) and not comparator.elts:  # [list] , (tuple)
            new_node = ast.UnaryOp(op=ast.Not(), operand=node.left)
        elif isinstance(comparator, ast.Dict) and not comparator.keys:  # {dict}
            new_node = ast.UnaryOp(op=ast.Not(), operand=node.left)
        elif isinstance(comparator, ast.Constant) and not comparator.value:  # 'string'
            new_node = ast.UnaryOp(op=ast.Not(), operand=node.left)
    elif isinstance(node.ops[0], ast.NotEq):  # A!=(empty) -> A
        if isinstance(comparator, (ast.List, ast.Tuple)) and not comparator.elts:  # [list] , (tuple)
            new_node = node.left
        elif isinstance(comparator, ast.Dict) and not comparator.keys:  # {dict}
            new_node = node.left
        elif isinstance(comparator, ast.Constant) and not comparator.value:  # 'string'
            new_node = node.left
    ast.copy_location(new_node, node)
    return new_node


def transform_If(node):  # (6, 7, 9)
    if len(node.body) == 1:
        if isinstance(node.body[0], ast.If) and not node.orelse and not node.body[0].orelse:
            node = transform_nestedIf(node)  # 6. NestedIf
        elif node.orelse:
            if isinstance(node.body[0], ast.Assign) or isinstance(node.body[0], ast.Expr):
                node = transform_Ifexp(node)  # 7. Ifexp
            elif isinstance(node.body[0], ast.Return):
                node = transform_return_boolean(node)  # 9. Return Boolean Statement
    return node


def transform_nestedIf(node):  # (6)
    new_test = ast.BoolOp(op=ast.And(), values=[node.test, node.body[0].test])
    new_node = ast.If(test=new_test, body=node.body[0].body, orelse=node.body[0].orelse)
    ast.copy_location(new_node, node)
    return new_node


def transform_Ifexp(node):
    new_node = node
    if isinstance(node.body[0], ast.Assign) and isinstance(node.orelse[0], ast.Assign):  # (7) Assign
        if len(node.body[0].targets) == 1 and len(node.orelse[0].targets) == 1 and isinstance(node.body[0].targets[0],
                                                                                              ast.Name) and isinstance(
                node.orelse[0].targets[0], ast.Name):
            if node.body[0].targets[0].id == node.orelse[0].targets[0].id:
                new_exp = ast.IfExp(test=node.test, body=node.body[0].value, orelse=node.orelse[0].value)
                new_node = ast.Assign(targets=node.body[0].targets, value=new_exp)
    elif isinstance(node.body[0], ast.Expr) and isinstance(node.orelse[0], ast.Expr):  # (7) print
        if isinstance(node.body[0].value, ast.Call) and isinstance(node.orelse[0].value, ast.Call):
            if isinstance(node.body[0].value.func, ast.Name) and isinstance(node.orelse[0].value.func, ast.Name):
                if node.body[0].value.func.id == 'print' and node.orelse[0].value.func.id == 'print':
                    new_exp = ast.IfExp(test=node.test, body=node.body[0].value.args[0],
                                        orelse=node.orelse[0].value.args[0])
                    new_node = ast.Expr(value=ast.Call(func=node.body[0].value.func, args=[new_exp], keywords=[]))
    ast.copy_location(new_node, node)
    return new_node


def transform_toEnumerate(self, node):  # (8)
    list_id, new_node = '', node
    if isinstance(node.iter, ast.Call):
        if isinstance(node.iter.func, ast.Name):
            if node.iter.func.id == 'range':
                if isinstance(node.iter.args[0], ast.Call):
                    if isinstance(node.iter.args[0].func, ast.Name):
                        if node.iter.args[0].func.id == 'len':
                            if isinstance(node.iter.args[0].args[0], ast.Name):
                                list_id = node.iter.args[0].args[0].id
                                self.toItem[list_id] = node.target.id
                                new_target = ast.Tuple(elts=[node.target, ast.Name(id='item', ctx=ast.Store())])
                                ast.copy_location(new_target, node.target)
                                new_iter = node.iter.args[0]
                                new_iter.func = ast.Name(id='enumerate', ctx=ast.Load())
                                new_node = ast.For(target=new_target, iter=new_iter, body=node.body, orelse=node.orelse)
                                ast.copy_location(new_node, node)
    return list_id, new_node


def transform_to_item(self, node):  # (8)
    new_node = node
    if hasattr(node.value, "id"):
        if node.value.id in self.toItem and isinstance(node.slice, ast.Name):
            if node.slice.id == self.toItem[node.value.id]:
                new_node = ast.Name(id='item', ctx=ast.Store())
    ast.copy_location(new_node, node)
    return new_node


def keep_assign_left(self, targets):  # (8)
    if isinstance(targets[0], ast.Subscript):
        if hasattr(targets[0].value, 'id'):
            if targets[0].value.id in self.toItem and isinstance(targets[0].slice, ast.Name):
                if targets[0].slice.id == self.toItem[targets[0].value.id]:
                    return True
    return False


def transform_return_boolean(node):  # (9)
    new_node = node
    if isinstance(node.body[0], ast.Return) and isinstance(node.orelse[0], ast.Return):
        if isinstance(node.body[0].value, ast.Constant) and isinstance(node.orelse[0].value, ast.Constant):
            if node.body[0].value.value == True and node.orelse[0].value.value == False:
                new_node = ast.Return(value=node.test)
    ast.copy_location(new_node, node)
    return new_node

def transform_multi_assign(body): # (10)
    new_stmts, temp_targets, temp_values, first_node, prev = [], [], [], None, []
    for stmt in body:
        if isinstance(stmt, ast.Assign):
            if dup_target(prev, stmt.value):
                new_stmts.append(merge_assign(first_node, temp_targets, temp_values))
                temp_targets=[]
                temp_values=[]
                first_node, prev = stmt, []
            if first_node is None:
                first_node = stmt
            for node in ast.walk(stmt.targets[0]):
                if hasattr(node, 'id'):
                    prev.append(node.id)
            temp_targets.append(stmt.targets[0])
            temp_values.append(stmt.value)
        else:
            if temp_targets:
                new_stmts.append(merge_assign(first_node, temp_targets, temp_values))
                temp_targets=[]
                temp_values=[]
                first_node, prev = None, []
            new_stmts.append(stmt)
    if temp_targets:
        new_stmts.append(merge_assign(first_node, temp_targets, temp_values))
    return new_stmts

def merge_assign(first_node, temp_targets, temp_values): # (10)
    new_assign = ast.Assign(targets=[ast.Tuple(elts=temp_targets, ctx=ast.Store())], value=ast.Tuple(elts=temp_values, ctx=ast.Load()))
    ast.copy_location(new_assign, first_node)
    if len(temp_targets)==1:
        new_assign = first_node
    return new_assign

def dup_target(prev, node): # (10)
    for target in ast.walk(node):
        if hasattr(target, 'id'):
            for id in prev:
                if target.id==id:
                    return True
    return False


def perform_comprehension(body, dict_list, lineno=1):
    # 'append' for list, 'add' for set comprehension
    comprehension_map = {"append": [ast.ListComp, ast.Add()], "add": [ast.SetComp, ast.BitOr()]}
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
                    print(dict_name)
                    if dict_name not in dict_list:
                        continue
                    key = node.targets[0].slice.value if isinstance(node.targets[0].slice, ast.Index) else node.targets[
                        0].slice
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
    map1 = {
        ast.Lt: ast.Gt,
        ast.LtE: ast.GtE,
        ast.Gt: ast.Lt,
        ast.GtE: ast.LtE,
        ast.Eq: ast.Eq,
        ast.NotEq: ast.NotEq
    }
    if isinstance(node, ast.BoolOp):
        for i in range(len(node.values)):
            if isinstance(node.values[i],ast.BoolOp):
                node.values[i]=transform_chaining_comparisons(node.values[i])
        while True:
            broken=False
            if type(node.op).__name__!="And":
                break
            for i,cur_comp in enumerate(node.values):
                for j,comp in enumerate(node.values):
                    if i >= j or not isinstance(node.values[i],ast.Compare) or not isinstance(node.values[j],ast.Compare):
                        continue
                    if ast.unparse(cur_comp.left) == ast.unparse(comp.left):
                        cur_comp.comparators.reverse()
                        cur_comp.ops.reverse()
                        chained_comp = ast.Compare(
                            left=cur_comp.comparators[0],
                            ops=[map1[type(x)]() for x in cur_comp.ops]+comp.ops,
                            comparators=cur_comp.comparators[1:]+[cur_comp.left]+ comp.comparators
                        )
                        if i>j:
                            node.values.pop(i)
                            node.values.pop(j)
                            node.values.append(chained_comp)
                        else:
                            node.values.pop(j)
                            node.values.pop(i)
                            node.values.append(chained_comp)
                        broken = True
                        break
                    elif ast.unparse(cur_comp.left) == ast.unparse(comp.comparators[-1]):
                        chained_comp = ast.Compare(
                            left=comp.left,
                            ops=comp.ops+cur_comp.ops,
                            comparators=comp.comparators+cur_comp.comparators
                        )
                        if i>j:
                            node.values.pop(i)
                            node.values.pop(j)
                            node.values.append(chained_comp)
                        else:
                            node.values.pop(j)
                            node.values.pop(i)
                            node.values.append(chained_comp)
                        broken = True
                        break
                    elif ast.unparse(cur_comp.comparators[-1]) == ast.unparse(comp.left):
                        chained_comp = ast.Compare(
                            left=cur_comp.left,
                            ops=cur_comp.ops+comp.ops,
                            comparators=cur_comp.comparators+comp.comparators
                        )
                        if i>j:
                            node.values.pop(i)
                            node.values.pop(j)
                            node.values.append(chained_comp)
                        else:
                            node.values.pop(j)
                            node.values.pop(i)
                            node.values.append(chained_comp)
                        broken = True
                        break
                    elif ast.unparse(cur_comp.comparators[-1]) == ast.unparse(comp.comparators[-1]):
                        comp.comparators.reverse()
                        comp.ops.reverse()
                        chained_comp = ast.Compare(
                            left=cur_comp.left,
                            ops=cur_comp.ops+[map1[type(x)]() for x in comp.ops],
                            comparators=cur_comp.comparators+comp.comparators[1:]+[comp.left]
                        )
                        if i>j:
                            node.values.pop(i)
                            node.values.pop(j)
                            node.values.append(chained_comp)
                        else:
                            node.values.pop(j)
                            node.values.pop(i)
                            node.values.append(chained_comp)
                        broken = True
                        break
                if broken:
                    break
            else:
                break
        return node

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


def find_dict(node):
    dict_list=[]
    for stmt in node:
        if isinstance(stmt, ast.Assign):
            if isinstance(stmt.value, (ast.Set,ast.Dict)):
                dict_list.append(stmt.targets[0].id)
    return dict_list


class CodeReplacer(ast.NodeTransformer):
    def __init__(self):
        self.toItem = {}  # (8)
        self.dict_list=[]

    def generic_visit(self, node): # 10. transform multiple assign
        if hasattr(node, 'body') and isinstance(node.body, list):
            node.body = transform_multi_assign(node.body)
        return super().generic_visit(node)

    def visit_Compare(self, node):  # 5. Test Empty Collection
        node = transform_empty_test(node)
        self.generic_visit(node)
        return node

    def visit_For(self, node):  # 8. toEnumerate
        list_id, node = transform_toEnumerate(self, node)
        self.generic_visit(node)
        self.toItem.pop(list_id, None)
        return node

    def visit_Subscript(self, node):  # change body (8).
        node = transform_to_item(self, node)
        self.generic_visit(node)
        return node

    def visit_Assign(self, node):  # handle exception (8).
        result = keep_assign_left(self, node.targets)
        if result:
            return node
        return self.generic_visit(node)

    def visit_FunctionDef(self, node):
        self.dict_list+=find_dict(node.body)
        self.generic_visit(node)
        node.body = perform_comprehension(node.body, self.dict_list)
        node.body = transform_list_appends(node.body)
        return node

    def visit_Module(self, node):
        self.dict_list+=find_dict(node.body)
        self.generic_visit(node)
        node.body = perform_comprehension(node.body, self.dict_list)
        node.body = transform_list_appends(node.body)
        return node

    def visit_If(self, node):
        node.test = transform_equality_comparisons(node.test)
        node.test = transform_chaining_comparisons(node.test)
        self.generic_visit(node) # to handle merge If over 3
        node = transform_If(node)  # 6, 7, 9
        return node

def main(ex_dir, updated_dir):
    for root, dirs, files in os.walk(ex_dir):
        for file in files:
            if file.endswith('.py'):
                try:
                    file_path = os.path.join(root, file)
                    with open(file_path, encoding="utf-8") as origin:
                        source_code = origin.read()

                    replacer = CodeReplacer()
                    updated_root = replacer.visit(ast.parse(source_code))
                    updated_code = ast.unparse(updated_root)

                    # updated_dir 하위 경로에 동일한 디렉토리 구조를 생성
                    relative_path = os.path.relpath(root, ex_dir)
                    target_dir = os.path.join(updated_dir, relative_path)

                    if not os.path.exists(target_dir):
                        os.makedirs(target_dir)

                    new_file_path = os.path.join(target_dir, file)
                    with open(new_file_path, "w") as new:
                        new.write(updated_code)
                    
                    time.sleep(0.5)
                except PermissionError:
                    print(f"Permission denied: {file_path}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Difference test with two folders.')
    parser.add_argument('-t1', '--target1', required=True)
    parser.add_argument('-t2', '--target2', required=True)
    parse_args = parser.parse_args()
    original_folder = parse_args.target1
    refactored_folder = parse_args.target2
    main(original_folder, refactored_folder)