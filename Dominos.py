import random

# This program has been coded quickly, so it needs optimization

def generate_domino_set() -> list:
    return [[x, y] for x in range(7) for y in range(x, 7)]


def split_set(stack: list) -> tuple:
    random.shuffle(stack)
    return stack[0:7], stack[7: 14], stack[14:]


def starter(p_stack, c_stack):
    p_dbl = [dom for dom in p_stack if dom[0] == dom[1]]
    c_dbl = [dom for dom in c_stack if dom[0] == dom[1]]
    if not p_dbl and not c_dbl:
        return None
    p_max_dbl = max(n[0] for n in p_dbl) if p_dbl else 0
    c_max_dbl = max(n[0] for n in c_dbl) if c_dbl else 0
    if p_max_dbl > c_max_dbl:
        return "player", [p_max_dbl, p_max_dbl]
    else:
        return "computer", [c_max_dbl, c_max_dbl]


def display() -> None:
    global stock, computer, player, snake, status
    print(
        "=" * 70, f"\nStock size: {len(stock)}\nComputer pieces: {len(computer)}\n", sep="")
    if len(snake) < 7:
        print(*snake)
    else:
        print(*snake[:3], "...", *snake[-3:])
    print("\nYour pieces:")
    for i, p in enumerate(player):
        print(f"{i + 1}: {p}")


def not_illegal_left(user: int, p_list: list[list]) -> bool:
    global snake
    user = abs(user) - 1
    if snake[0][0] == p_list[abs(user)][0]:
        snake.insert(0, p_list.pop(abs(user))[::-1])
        return True
    if snake[0][0] == p_list[abs(user)][1]:
        snake.insert(0, p_list.pop(abs(user)))
        return True
    else:
        return False


def not_illegal_right(user: int, p_list: list[list]) -> bool:
    global snake
    if snake[-1][-1] == p_list[user][0]:
        snake.append(p_list.pop(user))
        return True
    if snake[-1][-1] == p_list[user][1]:
        snake.append(p_list.pop(user)[::-1])
        return True
    else:
        return False


def player_play() -> None:
    global player, stock, snake
    user = input(
        "Status: It's your turn to make a move. Enter your command.\n")
    while True:
        try:
            user = int(user)
            if abs(user) - 1 >= len(player):
                raise ValueError
            if user == 0:
                take_in_stock(player)
                break
            elif user < 0:
                if not_illegal_left(user, player):
                    break
                else:
                    user = input("Illegal move. Please try again.\n")
            elif user > 0:
                user -= 1
                if not_illegal_right(user, player):
                    break
                else:
                    user = input("Illegal move. Please try again.\n")
            else:
                user = input("Illegal move. Please try again.\n")
        except ValueError:
            print("error")
            user = input("Invalid input. Please try again.\n")
    display()


def num_score() -> dict:
    global computer, snake
    scores = {}
    for dom_set in [computer, snake]:
        for dom in dom_set:
            for dots in dom:
                if dots not in scores:
                    scores[dots] = 1
                else:
                    scores[dots] += 1
    return scores


def pieces_score() -> dict:
    global computer
    num_s = num_score()
    return {num_s[pieces[0]] + num_s[pieces[1]]: i for i, pieces in enumerate(computer)}


def ai_choice(p_score) -> bool:
    global computer
    for s in sorted(p_score):
        choice = p_score[s]
        if choice == 0:
            return False
        if not_illegal_right(choice, computer) or not_illegal_left(choice, computer):
            return True


def take_in_stock(p):
    global stock, computer, player
    try:
        p.append(stock.pop())
    except IndexError:
        if p == computer:
            print("Status: The game is over. You won!")
        else:
            print("Status: The game is over. The computer won!")
        exit()


def computer_play() -> None:
    global computer, stock, snake
    input("Status: Computer is about to make a move. Press Enter to continue...\n")
    p_score = pieces_score()
    if not ai_choice(p_score):
        take_in_stock(computer)
    display()


def play(start_p: str) -> None:
    display()
    while True:
        if start_p == "player":
            player_play()
            check()
            computer_play()
            check()
        else:
            computer_play()
            check()
            player_play()
            check()


def win() -> bool:
    global computer, player
    if len(computer) == 0:
        print("Status: The game is over. The computer won!")
        exit()
    elif len(player) == 0:
        print("Status: The game is over. You won!")
        exit()
    else:
        return False


def draw() -> None:
    global snake
    count = 0
    if snake[0][0] == snake[-1][1]:
        for i in snake:
            for j in i:
                if j == snake[0][0]:
                    count += 1
    if count > 7:
        print("Status: The game is over. It's a draw!")
        exit()


def check() -> bool:
    return win() or draw()


if __name__ == "__main__":
    snake = []
    split_set(generate_domino_set())
    player, computer, stock = split_set(generate_domino_set())
    start_player, start_piece = starter(player, computer)
    if start_player == "player":
        player.remove(start_piece)
        status = "computer"
    else:
        computer.remove(start_piece)
        status = "player"
    snake.append(start_piece)
    play(status)
