import random
import copy
import keyboard
import json
import os
import sys


glob_score = 0
score = [0]


def cell(matrix, w):
    count = 0
    for i in matrix:
        if len(str(max(i))) > 3:
            count += 1

    if count == 0:
        w = 3
        return w
    elif count >= 1:
        w = len(str(max(i)))
        return w


def show_state(state):
    w_cell = 3
    h_cell = 1

    matrix = state['matrix']
    w_cell = cell(matrix, w_cell)

    hor_line = ('+' + '-' * w_cell) * state['y_cols'] + '+\n'
    line_with_gaps = ('|' + '%s') * state['y_cols'] + '|\n'
    table = (hor_line + line_with_gaps * h_cell) * state['x_cols'] + hor_line

    print('\n' * 5)
    print(table % tuple((str(cell).center(w_cell, ' ') for row in matrix for cell in row)))
    print("Score: ", state['score'])
    print("Best score: ", state['best_score'])
    print("Чтобы получить помощь, нажмите 'H'.")
    print("Чтобы выйти из игры, нажмите 'ESC' ")
    print("Чтобы начать новую игру, нажмите 'N' ")
    print("version 1.4.0")


def step(state, cmd):
    n_turns = {  # main direction is left
        'w': (0, 0),
        'a': (1, 3),
        's': (2, 2),
        'd': (3, 1),
    }
    before, after = n_turns[cmd]


def turn(lst):
    lst.reverse()
    a = []

    for j in range(len(lst)):
        temp = []
        for i in lst:
            temp.append(i[j])
        a.append(temp)

    lst, a = a, lst

    return lst


def remove_zeros(lst):
    for i in lst:
        value = 0
        while value in i:
            i.remove(value)
    return lst


def sum_score(score_x):
    a = [x * 2 for x in score_x]
    a = sum(a)
    return a


def aggregation(ls):
    lst2 = []

    ls_score = copy.deepcopy(ls)

    def sum_for_score(bbb):

        for i in bbb:
            for k in range(len(i) - 1):
                if i[k] == i[k + 1]:
                    score.append(i[k])
                    x = i[k] + i[k + 1]
                    i.pop(k + 1)
                    i.insert(k, x)
                    i.pop(k + 1)
                    i.append(0)
        return score

    global score
    score = sum_for_score(ls_score)

    def sum_element_app_zero(lst):  # Функция, которая складывает элементы в списке и добавляет ноль в конец!
        for i in range(len(lst) - 1):
            if lst[i] == lst[i + 1]:
                x = lst[i] + lst[i + 1]
                lst.pop(i + 1)
                lst.insert(i, x)
                lst.pop(i + 1)
                lst.append(0)
        return lst

    for j in ls:
        lst2.append(sum_element_app_zero(j))  # Добавляет полученный результат в список

    def remove_zeros1(lst):  # Функция удаления нулей
        num = 0
        for i in lst:
            while num in i:
                i.remove(num)
        return lst

    ls = remove_zeros1(lst2)
    return ls


def append_zeros(lst, state):
    for i in lst:
        while len(i) < state['y_cols']:
            i.append(0)
    return lst


def n_turn(lst1, num):
    lst1 = turn(lst1)
    num -= 1
    if num > 0:
        return n_turn(lst1, num)
    elif num == 0:
        return lst1


def step_random(matrix, state):
    coordinates = [(x, y) for x in range(state['x_cols']) for y in range(state['y_cols'])]
    rows = 1
    while rows > 0:
        x, y = random.choice(coordinates)
        if matrix[x][y] == 0:
            matrix[x][y] = random.choice([2, 4])
            rows -= 1
        elif matrix[x][y] != 0:
            continue
    return matrix


def game_over(state):
    lst = state['matrix']
    k = 0
    for i in lst:
        if 0 in i:
            k += 1
        else:
            continue

    if k > 0:
        pass
    elif k == 0:
        print("Game Over")
        exit(0)


def set_matrix(matrix, state):
    new_matrix = remove_zeros(matrix)
    new_matrix = aggregation(new_matrix)
    return append_zeros(new_matrix, state)


def event(state, cmd):
    if cmd == "w":
        matrix = move(state, cmd)
        game_over(state)
        return matrix
    elif cmd == "a":
        matrix = move_left(state, cmd)
        game_over(state)
        return matrix
    elif cmd == "s":
        matrix = move(state, cmd)
        game_over(state)
        return matrix
    elif cmd == "d":
        matrix = move(state, cmd)
        game_over(state)
        return matrix


def create_matrix(n, m):
    h = [0 for _ in range(n)]
    b2 = [[each - x for x in h] for each in h]
    return randomize(b2, n, m)


def randomize(matrix, n, m):
    coordinates = [(x, y) for x in range(n) for y in range(m)]
    rows = n
    while rows > 0:
        x, y = random.choice(coordinates)
        matrix[x][y] = random.choice([2, 4])
        rows -= 1
    return matrix


def best_score(a, c):
    if a > c:
        return a
    else:
        return c


def print_help():  
    print("Подсказака.",
          "Наша игра базируется на принципе сложения чисел. По сути это копия оригинальной игры 2048,"
          "но проще.",
          "Победить ты не сможешь, но можешь весело провести время. :)",
          "Основные правила: ",
          "1) Чтобы начать играть, нужно запустить программу. Ты с этим справился - молодец!",
          "2) Числа складываются, если они рядом, они равны и ты нажал верную клавишу",
          "3) Чтобы сдвинуть числа влево, нажми 'a';",
          "4) Чтобы сдвинуть числа вправо, нажми 'd';",
          "5) Чтобы сдвинуть числа вверх, нажми 'w';",
          "6) Чтобы сдвинуть числа вниз, нажми 's';",
          "7) Чтобы начать новую игру, нажми 'N';",
          "8) Чтобы выйти из игры, нажми 'ESC'",
          "9) Игра разработана силами Николая Курако и  Сергея Смирнова", sep="\n")


def step(cmd):
    n_turns = {  
        'w': (3, 1),
        'a': (0, 0),
        's': (1, 3),
        'd': (2, 2),
    }
    global before, after
    before, after = n_turns[cmd]


def move(state, cmd):
    step(cmd)
    matrix = n_turn(state['matrix'], before)
    matrix = set_matrix(matrix, state)
    matrix = n_turn(matrix, after)
    matrix = step_random(matrix, state)
    return matrix


def move_left(state, cmd):
    matrix = set_matrix(state['matrix'], state)
    matrix = step_random(matrix, state)
    return matrix


def run():
    state = dict()
    state['x_cols'] = 0
    state['y_cols'] = 0
    old_game = input('Добро пожаловать в 2048. Начать новую игру? (yes - начать новую, no - продолжить старую) : ')
    old_game = old_game.lower().strip()

    if 'yes' in old_game:
        state['x_cols'] = int(input('Введите число строк: '))
        state['y_cols'] = int(input('Введите число столбцов: '))
    state['matrix'] = create_matrix(state['x_cols'], state['y_cols'])
    state['score'] = 0
    state['best_score'] = 0

    if 'no' in old_game:
        with open('state.json', 'r') as file:
            state_old = json.load(file)
            state['matrix'] = state_old['matrix']
            state['score'] = state_old['score']
            state['best_score'] = state_old['best_score']
            state['x_cols'] = state_old['x_cols']
            state['y_cols'] = state_old['y_cols']

    elif 'yes' in old_game:
        print('Начата новая игра. Удачи!')
        try:
            with open('state.json', 'r') as file:
                state_old = json.load(file)
                state['best_score'] = state_old['best_score']
        except FileNotFoundError:
            with open('state.json', 'w') as j:
                json.dump(state, j)

    elif old_game == "exit":
        exit(0)

    while True:
        show_state(state)
        e = keyboard.read_event()

        if e.event_type != 'up':
            continue

        if e.name in "wasd":
            cmd = e.name
            state['matrix'] = event(state, cmd)
            if old_game == 'no':
                state['score'] = sum_score(score) + state_old['score']
            else:
                state['score'] = sum_score(score)

            state['best_score'] = best_score(state['score'], state['best_score'])
            with open('state.json', 'w') as j:
                json.dump(state, j)

        elif e.name == "esc":
            exit(0)

        elif e.name == "n":
            os.execl(sys.executable, sys.executable, *sys.argv)

        elif e.name == "h":
            print_help()

            
if __name__ == '__main__':
    run()
