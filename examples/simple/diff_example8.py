def main(players):
    for i in range(len(players)):
        print(i, players[i])
        print(players[i-1])
        players[i] = 1
    return players