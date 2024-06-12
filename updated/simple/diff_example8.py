def main(players):
    for (i, item) in enumerate(players):
        print(i, item)
        print(players[i - 1])
        players[i] = 1
    return players