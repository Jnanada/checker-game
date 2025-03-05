from copy import deepcopy
from typing import List, Tuple, Union

import streamlit as st
from streamlit_extras.stylable_container import stylable_container
from constants import COLS, ROWS, PIECES, ColorEnum
from elements import circle, squares
from piece import Piece


class Checkers:
    def __init__(self):
        self.board: List[List[Union[int, Piece]]] = [
            [0 for j in range(COLS)] for i in range(ROWS)
        ]
        self.REDS = self.BLACKS = PIECES
        self.RED_KINGS = self.BLACK_KINGS = 0
        self.initalize_board()

    def initalize_board(self):
        print("Initializing board")
        for row in range(ROWS):
            if row >= 3 and row < 5:
                continue
            for col in range(COLS):
                if col % 2 == (row + 1) % 2:
                    if row < 3:
                        self.board[row][col] = Piece(row, col, ColorEnum.RED.value)
                    elif row > 4:
                        self.board[row][col] = Piece(row, col, ColorEnum.BLACK.value)

    def display_board(self):
        for row in range(ROWS):
            st_row = st.columns(COLS)
            col = 0
            for st_col in st_row:
                st_square = squares(st_col)
                if self.check_if_piece_exists(row, col):
                    circle(st_square, ColorEnum(self.board[row][col].color))
                col += 1

    def update_board(self, current_piece: Piece, new_row: int, new_col: int):
        # Swap the position of the current peice with the new position
        (
            self.board[current_piece.position["row"]][current_piece.position["col"]],
            self.board[new_row][new_col],
        ) = (
            self.board[new_row][new_col],
            self.board[current_piece.position["row"]][current_piece.position["col"]],
        )
        # Update the current pice
        current_piece.move(new_row, new_col)
        if current_piece.has_reached_opponent_end():
            self.make_king(current_piece)

    def check_if_piece_exists(self, row, col):
        if isinstance(self.board[row][col], Piece):
            return True
        return False

    def get_piece(self, row, col):
        if not self._check_outside_bounds(row, col):
            if self.check_if_piece_exists(row, col):
                return self.board[row][col]

    def _check_if_same_piece_exists(self, piece, new_row, new_col):
        if self.check_if_piece_exists(new_row, new_col):
            new_piece = self.board[new_row][new_col]
            if new_piece:
                return True if new_piece.color == piece.color else False
        return False

    def _check_outside_bounds(self, row, col) -> bool:
        if (row < 0) or (col < 0) or (row >= ROWS) or (col >= COLS):
            return True
        return False

    def _check_if_move_is_diagonal(self, row, col, new_row, new_col) -> bool:
        return True if abs(new_col - col) == 1 and abs(new_row - row) == 1 else False

    def _is_in_direction(self, piece: Piece, new_row, new_col) -> bool:
        # If it is king, the new_row and new_col should be valid at this point.
        if piece.king:
            return True
        else:
            return new_row == piece.position["row"] + piece.direction.value and (
                new_col == piece.position["col"] + piece.direction.value
                or new_col == piece.position["col"] - piece.direction.value
            )

    def can_capture(
        self, row: int, col: int, new_row: int, new_col: int, player_piece: Piece
    ):
        try:
            # current_piece: Piece = self.get_piece(row, col)
            immediate_piece: Piece = self.get_piece(new_row, new_col)
            if immediate_piece:
                print(self._check_if_same_piece_exists(player_piece, new_row, new_col))
                if self._check_if_same_piece_exists(player_piece, new_row, new_col):
                    return False
                elif (
                    immediate_piece.color
                    != player_piece.color
                    # and immediate_piece.position in current_piece.get_immediate_moves()
                ):
                    # Clone Player Piece and update row and col as we are trying to capture.
                    clone_player_piece = deepcopy(player_piece)
                    clone_player_piece.move(
                        immediate_piece.position["row"], immediate_piece.position["col"]
                    )
                    for immediate_move in clone_player_piece.get_immediate_moves():
                        if (
                            self._check_if_same_piece_exists(
                                immediate_piece,
                                immediate_move["row"],
                                immediate_move["col"],
                            )
                            or immediate_move["col"] == player_piece.position["col"]
                        ):
                            continue

                        return self.can_capture(
                            immediate_piece.position["row"],
                            immediate_piece.position["col"],
                            immediate_move["row"],
                            immediate_move["col"],
                            player_piece,
                        )
                else:
                    return True
            elif not self._check_if_move_is_diagonal(
                player_piece.position["row"],
                player_piece.position["col"],
                new_row,
                new_col,
            ):
                return True
            return False
        except Exception as e:
            print(f"An error occurred {e}")

    def is_valid_move(self, piece: Piece, new_row: int, new_col: int):
        if piece:
            # Check if outside the bounds of the board
            if self._check_outside_bounds(new_row, new_col):
                return False
            # Check if the move to new_col is diagonal and not in the adjacent boxes.
            elif self._check_if_move_is_diagonal(
                piece.position["row"], piece.position["col"], new_row, new_col
            ):
                # Check if the direction is correct for the piece.
                if not self._is_in_direction(piece, new_row, new_col):
                    return False
                return True
            # Check if Piece exists and is of the current Player, at the index new_row and new_col
            elif self._check_if_same_piece_exists(piece, new_row, new_col):
                return False
        return True

    def make_king(self, piece: Piece):
        """
        Make the Piece a king.

        :param piece (Piece): A piece instance.
        """
        piece.set_king()
        # Update the counter for the kings.
        if piece.color == ColorEnum.RED:
            self.RED_KINGS += 1
        else:
            self.BLACK_KINGS += 1

    def capture_all_pieces(
        self, player_piece: Piece, new_row, new_col
    ) -> Tuple[int, int]:
        """
        Captures all the opponent's pieces and returns the new position after jumps.
        """
        try:
            immediate_piece: Piece = self.get_piece(new_row, new_col)
            if immediate_piece and immediate_piece.color != player_piece.color:
                # Clone Player Piece and update row and col as we are trying to capture.
                clone_player_piece = deepcopy(player_piece)
                clone_player_piece.move(
                    immediate_piece.position["row"], immediate_piece.position["col"]
                )
                print("clone player piece")
                print(clone_player_piece)
                for immediate_move in clone_player_piece.get_immediate_moves():
                    print("immediate move")
                    print(immediate_move)
                    if (
                        self._check_if_same_piece_exists(
                            immediate_piece,
                            immediate_move["row"],
                            immediate_move["col"],
                        )
                        or immediate_move["col"] == player_piece.position["col"]
                    ):
                        continue
                    return self.capture_all_pieces(
                        player_piece,
                        immediate_move["row"],
                        immediate_move["col"],
                    )
            else:
                return (
                    new_row,
                    new_col,
                )
        except Exception as e:
            print(f"An exception occurred while capturing opponent pieces - {e}")

    def remove(self, removed_pieces_positions: List):
        for row, col in removed_pieces_positions:
            current_piece: Piece = self.get_piece(row, col)
            if current_piece.color == ColorEnum.RED.value:
                if current_piece.king:
                    self.RED_KINGS -= 1
                self.REDS -= 1
            if current_piece.color == ColorEnum.BLACK.value:
                if current_piece.king:
                    self.BLACK_KINGS -= 1
                self.BLACKS -= 1
            current_piece = None
            self.board[row][col] = 0

    def move(self, row, col, new_row, new_col):
        try:
            current_piece: Piece = self.get_piece(row, col)
            removed_pieces_positions = []
            if current_piece:
                # First Check if the move is valid (ie not outside bounds, to the next available diagonal position and not occupied by the current player piece)
                if self.is_valid_move(current_piece, new_row, new_col):
                    print(self.can_capture(row, col, new_row, new_col, current_piece))
                    if self.can_capture(row, col, new_row, new_col, current_piece):
                        # TODO: Run this loop to check if any further captures are possible.
                        jump_row, jump_col = self.capture_all_pieces(
                            current_piece, new_row, new_col
                        )
                        self.update_board(current_piece, jump_row, jump_col)
                        removed_pieces_positions.append((new_row, new_col))
                        self.remove(removed_pieces_positions)
                    # Second if empty position
                    elif not self.check_if_piece_exists(new_row, new_col):
                        self.update_board(current_piece, new_row, new_col)
            else:
                raise ValueError("Invalid Move")
        except Exception as e:
            print(f"An exception has occurred while moving piece - {e}")

    def winner(self):
        if self.REDS <= 0:
            return "Player 2 (Engine) is the winner"
        elif self.BLACKS <= 0:
            return "Player 1 is the winner"
