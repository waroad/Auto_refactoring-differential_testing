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


def transform_comparisons(node):
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
        left = comparisons[0].left
        ops = []
        comparators = []
        print(ast.unparse(left))
        for c in comparisons:
            print(ast.unparse(c))
        for c in rest:
            print(ast.unparse(c))
        for comp in comparisons:
            # Ensure that the current comparison's left side matches the previous comparator
            if ops and comparators and comparators[-1] != comp.left:
                return node  # Return as is if the chain is broken

            ops.append(comp.ops[0])
            comparators.append(comp.comparators[0])

        # Create a single chained comparison
        chained_comp = ast.Compare(
            left=left,
            ops=ops,
            comparators=comparators
        )
        print(ast.unparse(chained_comp))
        return chained_comp

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
        print(ast.unparse(node.test))
        node.test = transform_comparisons(node.test)
        self.generic_visit(node)
        return node


class CodeReplacer(ast.NodeTransformer):
    def visit_FunctionDef(self, node):
        node.body = perform_comprehension(node.body)
        return node

    def visit_Module(self, node):
        node.body = perform_comprehension(node.body)
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
