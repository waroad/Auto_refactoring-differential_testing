def findClosestNumber(nums):
    (pos, neg) = ([], [])
    for item in nums:
        if item < 0:
            neg.append(item)
        elif item > 0:
            pos.append(item)
        else:
            return 0
    (result, result) = (0, sorted(pos)[0] if not neg else sorted(neg)[-1] if not pos else sorted(neg)[-1] if abs(sorted(neg)[-1]) < sorted(pos)[0] else sorted(pos)[0])
    return result
import time
start_time = time.perf_counter()
for _ in range(100000):
    findClosestNumber(list(map(int, '142131221235141565451141241356346')))
end_time = time.perf_counter()
elapsed_time = end_time - start_time
print(f'Elapsed time: {elapsed_time:.6f} seconds')