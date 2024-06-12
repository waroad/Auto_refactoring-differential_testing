def maximizeGreatness(nums):
    nums.sort()
    (n, ans, rem, curem) = (len(nums), 0, 0, 0)
    comp = nums[n - 1]
    for i in range(n - 2, -1, -1):
        if nums[i] < comp:
            comp = nums[i]
            rem += curem
            curem = 0
            ans += 1
        elif nums[i] == nums[i + 1]:
            if rem > 0:
                rem -= 1
                ans += 1
            curem += 1
    return ans
import time
start_time = time.perf_counter()
for _ in range(100000):
    maximizeGreatness(list(map(int, '14213151565456346')))
end_time = time.perf_counter()
elapsed_time = end_time - start_time
print(f'Elapsed time: {elapsed_time:.6f} seconds')