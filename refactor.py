import argparse
import ast

def replace_loops_and_declarations(body):
    updated_body = []
    for stmt in body:

        if isinstance(stmt, ast.For):
            # Gather comprehensions for all lists used in the loop
            comprehensions_to_add = []

            for node in stmt.body:
                if (isinstance(node, ast.Expr) and isinstance(node.value, ast.Call)
                        and isinstance(node.value.func, ast.Attribute) and node.value.func.attr == 'append'):
                        list_name = node.value.func.value.id
                        comprehension = ast.ListComp(
                            elt=node.value.args[0],
                            generators=[ast.comprehension(
                                target=stmt.target,
                                iter=stmt.iter,
                                ifs=[],
                                is_async=0
                            )]
                        )
                        comprehension_assignment = ast.AugAssign(
                            target=ast.Name(id=list_name, ctx=ast.Store()),
                            op=ast.Add(),
                            value=comprehension
                        )
                        comprehensions_to_add.append(ast.unparse(comprehension_assignment))
                else:
                    comprehensions_to_add=[]
                    break
            if comprehensions_to_add:
                # Insert comprehensions before the loop
                updated_body.extend([ast.parse(c).body[0] for c in comprehensions_to_add])
                continue

        updated_body.append(stmt)
    return updated_body


class CodeReplacer(ast.NodeTransformer):
    def visit_FunctionDef(self, node):
        node.body = replace_loops_and_declarations(node.body)
        return node

    def visit_Module(self, node):
        node.body = replace_loops_and_declarations(node.body)
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