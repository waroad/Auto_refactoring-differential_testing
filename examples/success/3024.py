def triangleType(nums):
    result = ''
    if sum(sorted(nums)[:2]) <= max(nums):
        result = 'none'
    elif len(set(nums)) == 1:
        result = 'equilateral'
    elif len(set(nums)) == 2:
        result = 'isosceles'
    else:
        result = 'scalene'
    return result

import time
start_time = time.perf_counter()
for _ in range(100000):
    triangleType([3, 3, 3])
    triangleType([3, 4, 5])
    triangleType([1, 2, 3])
    triangleType([1, 3, 3])
end_time = time.perf_counter()
elapsed_time = end_time - start_time
print(f'Elapsed time: {elapsed_time:.6f} seconds')