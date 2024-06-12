# https://www.acmicpc.net/source/78768187
name = input()
dic = {"L": 0, "O" : 0, "V" : 0, "E": 0}
for tmp_name in name:
    if tmp_name in dic.keys():
        dic[tmp_name] += 1
# print(dic)
n = int(input())
team = []
result = []
index = 0

for _ in range(n):
    team.append(input())

team.sort()
# print(team)

for teamName in team:
    tmp_result = 1
    # print(teamName)
    for alpha in teamName:
        if alpha in dic.keys():
            dic[alpha] += 1
    # print(dic)
    count_list = list(dic.values())
    # print(count_list)
    for i in range(len(count_list) - 1):
        for j in range(i + 1, len(count_list)):
            tmp_result *= (count_list[i] + count_list[j])
    # print(tmp_result)
    tmp_result = tmp_result % 100
    result.append((teamName, tmp_result))
    # print(result)
    # print("Check", dic)
    dic = {"L": 0, "O": 0, "V": 0, "E": 0}
    for tmp_name in name:
        if tmp_name in dic.keys():
            dic[tmp_name] += 1
result = sorted(result, key = lambda x : (x[1]), reverse=True)
print(result[0][0])


