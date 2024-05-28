import ast
code = '''
players = [1, 2, 3, 4, 5]
for i in range(len(players)):
    print(i, players[i])
    print(players[i-1])
    players[i] = 1
'''

node = ast.parse(code)
print(ast.dump(node, indent=2))