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
    pprint(board.board)


class Board:
    """ board builder """

    def __init__(self, dim_size: int, num_bombs: int):
        self.dim_size = dim_size
        self.num_bombs = num_bombs

        # create board and add bombs
        self.board: List[List[Any]] = self.make_new_board()
        # assign values to spaces to indicate number of bombs near location
        self.assign_values_to_board()

        self.dug: Set[tuple[int, int]] = set()

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


def main() -> None:
    """ main """
    play()


if __name__ == "__main__":
    main()
