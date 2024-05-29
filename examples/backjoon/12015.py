def main(N, list1):
    lis = [0]

    for integer in list1:
        if lis[-1] < integer:
            lis.append(integer)
        else:
            left = 0
            right = len(lis)
            
            while left < right:
                mid = (left + right) // 2
                
                if lis[mid] < integer:
                    left = mid + 1
                else:
                    right = mid
                    
            lis[right] = integer

    print(len(lis) - 1)