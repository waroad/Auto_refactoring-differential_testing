def myAtoi(s):
    num = '0123456789'
    res = ''
    for x in s:
        if x == ' ' and len(res) == 0:
            continue
        if x != ' ' and (x =='-' or x=='+' or x in num) and len(res) == 0:
            res += x
        elif x in num:
            res += x
        else:
            break
    if res == '' or res =='-' or res=='+':
        return 0
    else:
        if int(res) < -(2**31):
            return -(2**31)
        elif int(res) > (2**31 - 1):
            return (2**31 - 1)
        else:
            return int(res)
        
import time
start_time = time.perf_counter()
for _ in range(100000):
    myAtoi('14213151565456346')
end_time = time.perf_counter()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.6f} seconds")