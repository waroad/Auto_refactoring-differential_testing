def sortPeople(names, heights):
    (hash, hash) = ({}, {item: names[i] for (i, item) in enumerate(heights)})
    heights.sort(reverse=True)
    arr = []
    arr += [hash[i] for i in heights]
    return arr
import time
start_time = time.perf_counter()
for _ in range(100000):
    sortPeople(['Mary', 'John', 'Emma'], [180, 165, 170])
    sortPeople(['A', 'B', 'B'], [155, 185, 150])
    sortPeople(list('abcdjgifsodjifosijwnago'), list(map(int, '12314133413419684729402')))
end_time = time.perf_counter()
elapsed_time = end_time - start_time
print(f'Elapsed time: {elapsed_time:.6f} seconds')