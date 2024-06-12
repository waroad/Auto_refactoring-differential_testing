# BOJ 1296. 팀 이름 정하기
import sys


# 특정 글자의 수를 세주는 함수
def find_letter(word, letter):
    count = 0

    for i in range(len(word)):
        if word[i] == letter:
            count += 1

    return count


# 입력과, 연두 이름의 L, O, V, E 값을 세기
yeondu = input()
teams, winning = [], {}
N = int(input())

for _ in range(N):
    teams.append(sys.stdin.readline().rstrip())

teams.sort()

# 팀 이름을 바탕으로 확률을 계산하여 사전에 저장
for _ in range(N):
    team = teams[_]
    L = find_letter(yeondu, 'L') + find_letter(team, 'L')
    O = find_letter(yeondu, 'O') + find_letter(team, 'O')
    V = find_letter(yeondu, 'V') + find_letter(team, 'V')
    E = find_letter(yeondu, 'E') + find_letter(team, 'E')
    score = (L + O) * (O + V) * (V + E) * (L + V) * (O + E) * (L + E)
    winning[team] = score % 100

max_score = max(winning.values())

for _ in range(N):
    if winning[teams[_]] == max_score:
        print(teams[_])
        break