def main(house1, house2, C):
    house = []
    house += [house1, house2]
    house.sort()
    (start, end, mid) = (1, house[-1] - house[0], 0)
    for i in range(100):
        (mid, cnt, tmp) = ((start + end) / 2, 1, house[0])
        for houses in house:
            if houses - tmp >= mid:
                cnt += 1
                tmp = houses
            else:
                continue
        if cnt >= C:
            start = mid
        else:
            end = mid
    print(int(mid))