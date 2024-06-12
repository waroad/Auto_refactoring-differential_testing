def findClosestNumber(nums): #// nums = [-4, -2, 1, 4, 8]
    pos, neg = [], []
    for item in nums:
        if item < 0:
            neg.append(item)
        elif item > 0:
            pos.append(item)
        else:
            return 0
                                        #// neg = [-4, -2]     pos = [1, 4, 8]    
    result = 0
    if neg==[]:
        result = sorted(pos)[0]
    elif pos==[]:
        result = sorted(neg)[-1]
    else:
        if abs(sorted(neg)[-1]) < sorted(pos)[0]:
            result = sorted(neg)[-1]
        else:
            result = sorted(pos)[0]
    return result

import time
start_time = time.perf_counter()
for _ in range(100000):
    findClosestNumber(list(map(int, '142131221235141565451141241356346')))
end_time = time.perf_counter()
elapsed_time = end_time - start_time
print(f'Elapsed time: {elapsed_time:.6f} seconds')