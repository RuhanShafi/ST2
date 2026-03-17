move_count = 0

def moveDisks(n, fromTower, toTower, auxTower):
    global move_count
    if n == 1:
        print(f"Move disk 1 from {fromTower} to {toTower}")
        move_count += 1
    else:
        moveDisks(n - 1, fromTower, auxTower, toTower)
        print(f"Move disk {n} from {fromTower} to {toTower}")
        move_count += 1
        moveDisks(n - 1, auxTower, toTower, fromTower)


def main():
    global move_count
    n = int(input("Enter number of disks: "))
    move_count = 0
    moveDisks(n, 'A', 'B', 'C')
    print(f"\nTotal moves: {move_count}")


main()