import ast
code = '''
a = 1+2
'''

node = ast.parse(code)
print(ast.dump(node, indent=2))