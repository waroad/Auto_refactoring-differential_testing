import math
def maxStrength(nums):
    if len(nums) == 1:
        return nums[0]

    nums.sort()
    neg = [i for i in nums if i < 0]
    pos = [i for i in nums if i > 0]

    if neg==[] and pos==[]:
        return 0

    if len(neg)%2 == 1:
        if neg[:-1]!=[]:
            p = math.prod(neg[:-1])
        else:
            p = 0
    else:
        p = math.prod(neg)

    q = math.prod(pos) if pos else 0

    return max(p*q,q,p)
import time
start_time = time.perf_counter()
for _ in range(100000):
    maxStrength(list(map(int, '142131221235141565451141241356346')))
    maxStrength([-1, 4, -5, 8, 10, -7, 5, 6, 8, 9])
end_time = time.perf_counter()
elapsed_time = end_time - start_time
print(f'Elapsed time: {elapsed_time:.6f} seconds')