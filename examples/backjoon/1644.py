def prime_numbers(n):
    arr = [i for i in range(n+1)] 
    end = int(n**(1/2))
    for i in range(2, end+1):
        if arr[i] == 0:
            continue
        for j in range(i*i, n+1, i):
            arr[j] = 0
            
    return [i for i in arr[2:] if arr[i]]

def main(N):
    if N == 1:
        print(0)
        exit()
    primes = prime_numbers(N)
    # print(primes)
    pointer1 = 0
    pointer2 = 0
    sum = primes[0]
    num_of_cases = 0

    while True:
        # print(pointer1 ,pointer2)
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