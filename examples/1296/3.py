# https://www.acmicpc.net/source/76404441
name = input()
n = int(input())
arr = []

name_arr = [0]*4
temp_arr = [0]*4
result=[]
for i in range(n):
    arr.append(input())

arr.sort()

for i in name:
    if(i=='L'):
        name_arr[0]+=1
    elif(i=='O'):
        name_arr[1]+=1
    elif(i=='V'):
        name_arr[2]+=1
    elif(i=='E'):
        name_arr[3]+=1
for i in arr:
    for j in i:
        if(j=='L'):
            temp_arr[0]+=1
        elif(j=='O'):
            temp_arr[1]+=1
        elif(j=='V'):
            temp_arr[2]+=1
        elif(j=='E'):
            temp_arr[3]+=1
    result.append(((name_arr[0]+temp_arr[0]+name_arr[1]+temp_arr[1]) * (name_arr[0]+temp_arr[0]+name_arr[2]+temp_arr[2]) * (name_arr[0]+temp_arr[0]+name_arr[3]+temp_arr[3]) * (name_arr[1]+temp_arr[1]+ name_arr[2]+temp_arr[2]) * (name_arr[1]+temp_arr[1]+name_arr[3]+temp_arr[3]) * (name_arr[2]+temp_arr[2]+name_arr[3]+temp_arr[3])) % 100)
    temp_arr = [0]*4

print(arr[result.index(max(result))])