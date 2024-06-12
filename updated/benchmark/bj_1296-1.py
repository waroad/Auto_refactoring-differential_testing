import sys

def find_letter(word, letter):
    count = 0
    for (i, item) in enumerate(word):
        if item == letter:
            count += 1
    return count
(yeondu, (teams, winning), N) = (input(), ([], {}), int(input()))
teams += [sys.stdin.readline().rstrip() for _ in range(N)]
teams.sort()
for _ in range(N):
    team = teams[_]
    (L, O, V, E) = (find_letter(yeondu, 'L') + find_letter(team, 'L'), find_letter(yeondu, 'O') + find_letter(team, 'O'), find_letter(yeondu, 'V') + find_letter(team, 'V'), find_letter(yeondu, 'E') + find_letter(team, 'E'))
    score = (L + O) * (O + V) * (V + E) * (L + V) * (O + E) * (L + E)
    winning[team] = score % 100
max_score = max(winning.values())
for _ in range(N):
    if winning[teams[_]] == max_score:
        print(teams[_])
        break