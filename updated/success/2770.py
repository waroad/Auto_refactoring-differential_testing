def maximumJumps(nums, target):
    (dp, dp[0]) = ([0] * len(nums), 0)
    for i in range(1, len(nums)):
        if not dp[i]:
            continue
        for j in range(i + 1, len(nums)):
            if abs(nums[j] - nums[i]) <= target:
                dp[j] = max(dp[i] + 1, dp[j])
    return dp[-1]
import time
start_time = time.perf_counter()
for _ in range(100000):
    maximumJumps(list(map(int, '14213151565456346')), 3)
end_time = time.perf_counter()
elapsed_time = end_time - start_time
print(f'Elapsed time: {elapsed_time:.6f} seconds')