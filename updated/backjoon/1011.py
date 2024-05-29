def main(x, y):
    (distance, count, move, move_plus) = (y - x, 0, 1, 0)
    while distance > move_plus:
        count += 1
        move_plus += move
        if not count % 2:
            move += 1
    print(count)