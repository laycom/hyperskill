from random import randint
from math import inf as infinity
import time


def is_win(current_field, symbol):
    win_state = [
        [current_field[0][0], current_field[0][1], current_field[0][2]],
        [current_field[1][0], current_field[1][1], current_field[1][2]],
        [current_field[2][0], current_field[2][1], current_field[2][2]],
        [current_field[0][0], current_field[1][0], current_field[2][0]],
        [current_field[0][1], current_field[1][1], current_field[2][1]],
        [current_field[0][2], current_field[1][2], current_field[2][2]],
        [current_field[0][0], current_field[1][1], current_field[2][2]],
        [current_field[2][0], current_field[1][1], current_field[0][2]],
    ]
    if [symbol, symbol, symbol] in win_state:
        return True
    else:
        return False


def is_draw(current_field):
    current_field_mod = sum(current_field, [])
    if ' ' not in current_field_mod:
        return True
    return False


class Player:
    def __init__(self, level, symbol):
        self.level = level
        self.x = None
        self.y = None
        self.valid = None
        self.symbol = symbol

    def next_move(self, current_field):
        if self.level == 'user':
            while True:
                coordinate = input("Enter the coordinates: ").split()
                self.valid, x, y = self.valid_user_coordinates(coordinate, current_field)
                if self.valid == 'Valid':
                    self.x = x
                    self.y = y
                    return self.x, self.y
                else:
                    print(self.valid)
        elif self.level == 'easy':
            print('Making move level "easy"')
            self.y, self.x = self.bot_level_easy(current_field)
            return self.x, self.y
        elif self.level == 'medium':
            print('Making move level "medium"')
            self.y, self.x = self.bot_level_medium(current_field)
            return self.x, self.y
        elif self.level == 'hard':
            print('Making move level "hard"')
            self.y, self.x = self.bot_level_hard(current_field)
            return self.x, self.y

    @staticmethod
    def valid_user_coordinates(coordinate, current_field):
        switch_x = {
            '1': 0,
            '2': 1,
            '3': 2
        }
        switch_y = {
            '1': 2,
            '2': 1,
            '3': 0
        }
        x = None
        y = None
        limit_field = ['1', '2', '3']
        if len(coordinate) != 2:
            return "Input 2 coordinate", x, y
        for item in coordinate:
            if not item.isnumeric():
                return "You should enter numbers!", x, y
            elif item not in limit_field:
                return "Coordinates should be from 1 to 3!", x, y
        x = switch_x[coordinate[0]]
        y = switch_y[coordinate[1]]
        if current_field[y][x] != ' ':
            return "This cell is occupied! Choose another one!", x, y
        return "Valid", x, y

    def bot_level_easy(self, current_field):
        while True:
            x = randint(0, 2)
            y = randint(0, 2)
            if current_field[y][x] == ' ':
                break
        return y, x

    def bot_level_medium(self, current_field):

        for i in range(len(current_field)):
            if current_field[i][0] == current_field[i][1] != ' ' and current_field[i][2] == ' ':
                return i, 2
            elif current_field[i][0] == current_field[i][2] != ' ' and current_field[i][1] == ' ':
                return i, 1
            elif current_field[i][1] == current_field[i][2] != ' ' and current_field[i][0] == ' ':
                return i, 0

        for i in range(len(current_field)):
            if current_field[0][i] == current_field[1][i] != ' ' and current_field[2][i] == ' ':
                return 2, i
            elif current_field[0][i] == current_field[2][i] != ' ' and current_field[1][i] == ' ':
                return 1, i
            elif current_field[1][i] == current_field[2][i] != ' ' and current_field[0][i] == ' ':
                return 0, i

        if current_field[0][0] == current_field[1][1] != ' ' and current_field[2][2] == ' ':
            return 2, 2
        elif current_field[0][0] == current_field[2][2] != ' ' and current_field[1][1] == ' ':
            return 1, 1
        elif current_field[1][1] == current_field[2][2] != ' ' and current_field[0][0] == ' ':
            return 0, 0

        if current_field[0][2] == current_field[1][1] != ' ' and current_field[2][0] == ' ':
            return 2, 0
        elif current_field[0][2] == current_field[2][0] != ' ' and current_field[1][1] == ' ':
            return 1, 1
        elif current_field[1][1] == current_field[2][0] != ' ' and current_field[0][2] == ' ':
            return 0, 2

        return self.bot_level_easy(current_field)

    def bot_level_hard(self, current_field):

        symbol = self.symbol
        another_symbol = {
            "X": "O",
            "O": "X"
        }

        def evaluate(current_field):
            if is_win(current_field, symbol):
                score = 1
            elif is_win(current_field, another_symbol[symbol]):
                score = -1
            else:
                score = 0
            return score

        def game_over(current_field):
            return is_win(current_field, "X") or is_win(current_field, "O")

        def valid_move(x, y):
            if [x, y] in empty_cells(current_field):
                return True
            else:
                return False

        def empty_cells(current_field):
            cells = []
            for x, row in enumerate(current_field):
                for y, cell in enumerate(row):
                    if cell == ' ':
                        cells.append([x, y])
            return cells

        def minimax(current_field, depth, player):
            if player == symbol:
                best = [-1, -1, -infinity]
            else:
                best = [-1, -1, +infinity]

            if depth == 0 or game_over(current_field):
                score = evaluate(current_field)
                return [-1, -1, score]
            for cell in empty_cells(current_field):
                x, y = cell[0], cell[1]
                current_field[x][y] = player
                score = minimax(current_field, depth - 1, another_symbol[player])
                current_field[x][y] = ' '
                score[0], score[1] = x, y

                if player == symbol:
                    if score[2] > best[2]:
                        best = score  # max value
                else:
                    if score[2] < best[2]:
                        best = score  # min value

            return best

        def ai_turn(current_field):
            depth = len(empty_cells(current_field))
            if depth == 0 or game_over(current_field):
                return

            if depth == 9:
                x = 1
                y = 1
            else:
                move = minimax(current_field, depth, symbol)
                x, y = move[0], move[1]

            if valid_move(x, y):
                return x, y

        return ai_turn(current_field)


class GameField:
    def __init__(self):
        self.current_field = [[' ' for _ in range(3)] for _ in range(3)]

    def print_field(self):
        print("---------")
        for item in self.current_field:
            print('|', item[0], item[1], item[2], '|')
        print("---------")

    def make_move(self, x, y, symbol):
        self.current_field[y][x] = symbol
        self.print_field()


def start_valid(command):
    players_list = ['user', 'easy', 'medium', 'hard']
    if len(command) != 3:
        return True
    elif len(command) != 3 or command[1] not in players_list or command[2] not in players_list:
        return True
    elif command[0] != 'start':
        return True
    else:
        return False


def main():
    while True:
        command = input("Input command start user or bot (easy, medium, hard) /exit: ").split()
        if command[0] == 'exit':
            break
        elif start_valid(command):
            print("Bad parameters")
        else:
            game_field = GameField()
            game_field.print_field()
            first_player = Player(command[1], 'X')
            second_player = Player(command[2], 'O')
            player = first_player
            while True:
                x, y = player.next_move(game_field.current_field)
                game_field.make_move(x, y, player.symbol)
                time.sleep(1)
                if is_win(game_field.current_field, player.symbol):
                    print(f'{player.level} for {player.symbol} won: ')
                    break
                elif is_draw(game_field.current_field):
                    print('Draw')
                    break
                if player == first_player:
                    player = second_player
                else:
                    player = first_player


if __name__ == "__main__":
    main()
