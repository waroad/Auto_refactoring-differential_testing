import argparse
import ast


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


class CodeReplacer(ast.NodeTransformer):
    def visit_FunctionDef(self, node):
        node.body = perform_comprehension(node.body)
        self.generic_visit(node)
        return node

    def visit_Module(self, node):
        node.body = perform_comprehension(node.body)
        self.generic_visit(node)
        return node

    def visit_If(self, node):
        node.test = transform_equality_comparisons(node.test)
        node.test = transform_chaining_comparisons(node.test)
        self.generic_visit(node)
        return node


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Measures coverage.')
    parser.add_argument('-t', '--target', required=True)
    parser.add_argument("remaining", nargs="*")
    args = parser.parse_args()
    target = args.target
    lines = open(target, "r").readlines()
    code = "".join(lines)
    replacer = CodeReplacer()
    updated_root = replacer.visit(ast.parse(code))
    print(ast.unparse(updated_root))
