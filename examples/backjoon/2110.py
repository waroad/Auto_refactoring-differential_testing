def main(house1, house2, C):
    house = []

    house.append(house1)
    house.append(house2)
    house.sort()

    start = 1
    end = house[-1] - house[0]
    mid = 0
    for i in range(100):
        mid = (start + end) / 2
        cnt = 1
        tmp = house[0]
        for houses in house:
            if houses-tmp >= mid:
                cnt += 1
                tmp = houses
            else:
                continue
        if cnt >= C:
            start = mid
        else:
            end = mid
    print(int(mid))