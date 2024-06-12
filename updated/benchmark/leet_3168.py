def isValid(word):
    if len(word) < 3:
        return False
    (vowelcount, consonantcount, validcharacterscount) = (0, 0, 0)
    for char in word:
        if char.isalpha():
            if char in ['a', 'e', 'i', 'o', 'u']:
                vowelcount += 1
            else:
                consonantcount += 1
            validcharacterscount += 1
        elif char.isdigit():
            validcharacterscount += 1
        else:
            return False
    return validcharacterscount >= 3 and vowelcount >= 1 and (consonantcount >= 1)
import time
start_time = time.perf_counter()
for _ in range(100000):
    isValid('234adas')
    isValid('b3')
    isValid('a3$e')
    isValid('1414215adsfsakfhalkh')
end_time = time.perf_counter()
elapsed_time = end_time - start_time
print(f'Elapsed time: {elapsed_time:.6f} seconds')