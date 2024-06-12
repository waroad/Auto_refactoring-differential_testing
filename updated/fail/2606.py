def maximumCostSubstring(s: str, chars: str, vals: list[int]) -> int:
    ((nums, c), c) = (([], {}), {item: i for (i, item) in enumerate(chars)})
    for i in s:
        if i in c:
            nums.append(vals[c[i]])
        else:
            nums.append(ord(i) - ord('a') + 1)
    (res, total) = (0, 0)
    for i in nums:
        total += i
        res = max(res, total)
        if total < 0:
            total = 0
    return res
import time
start_time = time.perf_counter()
for _ in range(100000):
    maximumCostSubstring('adaa', 'd', [-1000])
    maximumCostSubstring('abc', 'abc', [-1, -1, -1])
    maximumCostSubstring('abeyczodfgbjxflfzjfdosijfisggnnvxvzbjfkhfkahsfkd', 'bdh', [-10, -1, -5])
end_time = time.perf_counter()
elapsed_time = end_time - start_time
print(f'Elapsed time: {elapsed_time:.6f} seconds')