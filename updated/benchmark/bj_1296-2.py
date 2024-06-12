(name, dic) = (input(), {'L': 0, 'O': 0, 'V': 0, 'E': 0})
for tmp_name in name:
    if tmp_name in dic.keys():
        dic[tmp_name] += 1
(n, team, result, index) = (int(input()), [], [], 0)
team += [input() for _ in range(n)]
team.sort()
for teamName in team:
    tmp_result = 1
    for alpha in teamName:
        if alpha in dic.keys():
            dic[alpha] += 1
    count_list = list(dic.values())
    for i in range(len(count_list) - 1):
        for j in range(i + 1, len(count_list)):
            tmp_result *= count_list[i] + count_list[j]
    tmp_result = tmp_result % 100
    result.append((teamName, tmp_result))
    dic = {'L': 0, 'O': 0, 'V': 0, 'E': 0}
    for tmp_name in name:
        if tmp_name in dic.keys():
            dic[tmp_name] += 1
result = sorted(result, key=lambda x: x[1], reverse=True)
print(result[0][0])