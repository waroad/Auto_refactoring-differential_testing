def prime_numbers(n):
    (arr, end) = ([i for i in range(n + 1)], int(n ** (1 / 2)))
    for i in range(2, end + 1):
        if not arr[i]:
            continue
        for j in range(i * i, n + 1, i):
            arr[j] = 0
    return [i for i in arr[2:] if arr[i]]

def main(N):
    if N == 1:
        print(0)
        exit()
    (primes, pointer1, pointer2) = (prime_numbers(N), 0, 0)
    (sum, num_of_cases) = (primes[0], 0)
    while True:
        if sum < N:
            if pointer2 < len(primes) - 1:
                pointer2 += 1
                sum += primes[pointer2]
            else:
                break
        elif sum > N:
            sum -= primes[pointer1]
            pointer1 += 1
        else:
            num_of_cases += 1
            if pointer2 < len(primes) - 1:
                pointer2 += 1
                sum += primes[pointer2]
            else:
                break
        if pointer1 > pointer2:
            break
    print(num_of_cases)