players = [1, 2, 3, 4, 5]
for i, item in enumerate(players):
    print(i, item)
    print(players[i - 1])
    players[i] = 1