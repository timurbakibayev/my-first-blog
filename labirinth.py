from typing import List, Tuple

a = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 2, 1, 1, 1, 1, 7, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]


def find_i_j(lab: List, what_to_find: int) -> Tuple[int, int]:
    for i in range(len(lab)):
        for j in range(len(lab[i])):
            if lab[i][j] == what_to_find:
                return i, j
    return -1, -1


def move_7(lab: List, command: str) -> List:
    i, j = find_i_j(lab, 7)
    command = command.lower()[0]
    if command == "u":
        new_i = i - 1
        new_j = j
    elif command == "d":
        new_i = i + 1
        new_j = j
    elif command == "l":
        new_i = i
        new_j = j - 1
    elif command == "r":
        new_i = i
        new_j = j + 1
    else:
        print("command not found")
        return lab
    if lab[new_i][new_j] != 1:
        lab[i][j] = 0
        lab[new_i][new_j] = 7
    else:
        print("There is a wall, sorry")
    return lab


found = False

while not found:
    print(f"You are at position {find_i_j(a, 7)}")
    i, j = find_i_j(a, 7)
    gold_i, gold_j = find_i_j(a, 2)
    distance = abs(i-gold_i) + abs(j-gold_j)
    print(f"Distance to gold is {distance}km")
    if a[i-1][j] == 1:
        print("There is a wall ABOVE you")
    if a[i+1][j] == 1:
        print("There is a wall UNDER you")
    if a[i][j-1] == 1:
        print("There is a wall on the LEFT of you")
    if a[i][j+1] == 1:
        print("There is a wall on the RIGHT of you")
    command = input("Where do you want to go(L/R/U/D)? ")
    a = move_7(a, command)
    gold_i, gold_j = find_i_j(a, 2)
    if gold_i == -1:
        found = True

print("Congratulations!")
