""" sample module doc string """

import random
from pprint import pprint
from typing import List, Any, Set


def play(dim_size: int = 10, num_bombs: int = 10) -> None:
    """ Play a new game """
    # create board
    # show board
    # wait for dig location
    #   if clear, expand area
    #   else bomb, end game
    board = Board(dim_size, dim_size)

    safe = True

    while len(board.dug) < board.dim_size ** 2 - num_bombs:
        print(board)
        user_input = input("Where would you like to dig? ex: row, col <enter> : ")
        row, col = list(map(int, user_input.split(",")))

        if row < 0 or row > board.dim_size or col < 0 or col > board.dim_size:
            print("Invalid Input Try again.")
            continue

        safe = board.dig(row, col)

        if not safe:
            break

    if safe:
        print("You Win")
    else:
        print("BOOM!")


class Board:
    """ board builder """

    def __init__(self, dim_size: int, num_bombs: int):
        self.dim_size = dim_size
        self.num_bombs = num_bombs

        # create board and add bombs
        self.board: List[List[Any]] = self.make_new_board()
        # assign values to spaces to indicate number of bombs near location
        self.assign_values_to_board()

        # Track places dug
        self.dug: Set[tuple[int, int]] = set()

    def dig(self, row: int, col: int) -> bool:
        """ lets look get to digging """

        # add dig location to self.dug
        self.dug.add((row, col))

        if self.board[row][col] == "*":
            return False
        elif self.board[row][col] > 0:
            return True

        for r in range(max(0, row - 1), min(self.dim_size - 1, (row + 1)) + 1):
            for c in range(max(0, col - 1), min(self.dim_size - 1, (col + 1)) + 1):
                if (r, c) in self.dug:
                    continue  # already dug here move along
                self.dig(r, c)
        return True

    def make_new_board(self) -> List[List[Any]]:
        """ Create a new game board and populate with bombs"""
        # create empty board
        board: List[List[Any]] = [
            [None for _ in range(self.dim_size)] for _ in range(self.dim_size)
        ]

        # plant bombs
        bombs_planted: int = 0
        while bombs_planted < self.num_bombs:
            loc = random.randint(0, self.dim_size ** 2 - 1)
            row = loc // self.dim_size
            col = loc % self.dim_size
            if board[row][col] == "*":
                continue

            board[row][col] = "*"
            bombs_planted += 1

        return board

    def assign_values_to_board(self) -> None:
        """ assign numbers to board indicating num of surrounding bombs """
        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if self.board[r][c] == "*":
                    # skip locations with bomb
                    continue
                self.board[r][c] = self.get_neighboring_bomb_count(r, c)
        return None

    def get_neighboring_bomb_count(self, row: int, col: int) -> int:
        """ count up surrounding bombs """
        num_of_neighboring_bombs = 0

        for r in range(max(0, row - 1), min(self.dim_size - 1, (row + 1)) + 1):
            for c in range(max(0, col - 1), min(self.dim_size - 1, (col + 1)) + 1):
                if r == row and c == col:
                    continue
                if self.board[r][c] == "*":
                    num_of_neighboring_bombs += 1

        return num_of_neighboring_bombs

    def __str__(self):
        # this is a magic function where if you call print on this object,
        # it'll print out what this function returns!
        # return a string that shows the board to the player

        # first let's create a new array that represents what the user would see
        visible_board = [
            [None for _ in range(self.dim_size)] for _ in range(self.dim_size)
        ]
        for row in range(self.dim_size):
            for col in range(self.dim_size):
                if (row, col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    visible_board[row][col] = " "

        # put this together in a string
        string_rep = ""
        # get max column widths for printing
        widths = []
        for idx in range(self.dim_size):
            columns = map(lambda x: x[idx], visible_board)
            widths.append(len(max(columns, key=len)))

        # print the csv strings
        indices = [i for i in range(self.dim_size)]
        indices_row = "   "
        cells = []
        for idx, col in enumerate(indices):
            format = "%-" + str(widths[idx]) + "s"
            cells.append(format % (col))
        indices_row += "  ".join(cells)
        indices_row += "  \n"

        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f"{i} |"
            cells = []
            for idx, col in enumerate(row):
                format = "%-" + str(widths[idx]) + "s"
                cells.append(format % (col))
            string_rep += " |".join(cells)
            string_rep += " |\n"

        str_len = int(len(string_rep) / self.dim_size)
        string_rep = indices_row + "-" * str_len + "\n" + string_rep + "-" * str_len

        return string_rep


def main() -> None:
    """ main """
    play()


if __name__ == "__main__":
    main()
