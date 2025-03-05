from copy import deepcopy
import json
from typing import Dict, List, Union
from constants import COLS, ROWS, ColorEnum, PointsEnum
from piece import Piece, Position


class Engine:
    def __init__(self):
        self.engine_color = ColorEnum.BLACK
        pass

    def _check_if_piece_exists(self, board, row, col):
        if not self._check_outside_bounds(row, col):
            if isinstance(board[row][col], Piece):
                return True
            return False

    def _check_outside_bounds(self, row, col) -> bool:
        if (row < 0) or (col < 0) or (row >= ROWS) or (col >= COLS):
            return True
        return False

    def get_piece(self, board, row, col):
        if not self._check_outside_bounds(row, col):
            if self._check_if_piece_exists(board, row, col):
                return board[row][col]

    def _check_if_same_piece_exists(self, board, piece, new_row, new_col):
        if not self._check_outside_bounds(new_row, new_col):
            if self._check_if_piece_exists(board, new_row, new_col):
                new_piece = board[new_row][new_col]
                if new_piece:
                    return True if new_piece.color == piece.color else False
            return False

    def _check_if_move_is_diagonal(self, row, col, new_row, new_col) -> bool:
        return True if abs(new_col - col) == 1 and abs(new_row - row) == 1 else False

    def can_capture(
        self, board, row: int, col: int, new_row: int, new_col: int, player_piece: Piece
    ):
        try:
            # current_piece: Piece = self.get_piece(row, col)
            immediate_piece: Piece = self.get_piece(board, new_row, new_col)
            if immediate_piece:
                print(
                    self._check_if_same_piece_exists(
                        board, player_piece, new_row, new_col
                    )
                )
                if self._check_if_same_piece_exists(
                    board, player_piece, new_row, new_col
                ):
                    return False
                elif immediate_piece.color != player_piece.color:
                    # Clone Player Piece and update row and col as we are trying to capture.
                    clone_player_piece = deepcopy(player_piece)
                    clone_player_piece.move(
                        immediate_piece.position["row"], immediate_piece.position["col"]
                    )
                    for immediate_move in clone_player_piece.get_immediate_moves():
                        if (
                            self._check_if_same_piece_exists(
                                board,
                                immediate_piece,
                                immediate_move["row"],
                                immediate_move["col"],
                            )
                            or immediate_move["col"] == player_piece.position["col"]
                            or self._check_outside_bounds(
                                immediate_move["row"], immediate_move["col"]
                            )
                        ):
                            continue

                        return self.can_capture(
                            board,
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

    def set_points(self, player_piece: Piece, move: Position, captured: bool = False):
        clone_player_piece = deepcopy(player_piece)
        clone_player_piece.move(move["row"], move["col"])
        if clone_player_piece.has_reached_opponent_end():
            return PointsEnum.KING.value
        elif captured:
            return PointsEnum.PIECE.value
        else:
            return PointsEnum.EMPTY.value

    def find_best_move(self, board: List[List[Union[int, Piece]]]):
        moves: Dict[Position, int] = dict()
        for i, j in [(i, j) for i in range(ROWS) for j in range(COLS)]:
            print(f"({i}, {j})")
            if not self._check_if_piece_exists(board, i, j):
                print(f"No piece ({i}, {j})")
                continue
            current_piece: Piece = self.get_piece(board, i, j)
            if current_piece.color != self.engine_color.value:
                print(f"Opponent piece ie Red ({i}, {j})")
                continue
            for immediate_move in current_piece.get_immediate_moves():
                if self._check_outside_bounds(
                    immediate_move["row"], immediate_move["col"]
                ):
                    print(
                        f"Outside Bounds ({i}, {j}) - ({immediate_move['row']}, {immediate_move['col']})"
                    )
                    continue
                # Checks both if piece exists and if yes, checks if it's same piece or opponent's piece.
                elif not self._check_if_piece_exists(
                    board, immediate_move["row"], immediate_move["col"]
                ):
                    print(
                        f"Immediate move piece ({i}, {j}) - ({immediate_move['row']}, {immediate_move['col']})"
                    )
                    moves[(i, j, immediate_move["row"], immediate_move["col"])] = (
                        self.set_points(current_piece, immediate_move)
                    )
                else:
                    print(
                        f"Check Can Capture ({i}, {j}) - ({immediate_move['row']}, {immediate_move['col']})"
                    )
                    if self.can_capture(
                        board,
                        i,
                        j,
                        immediate_move["row"],
                        immediate_move["col"],
                        current_piece,
                    ):
                        moves[(i, j, immediate_move["row"], immediate_move["col"])] = (
                            self.set_points(current_piece, immediate_move, True)
                        )
        print(moves)
        print(max(moves, key=moves.get))
        if not moves:
            return None
        return max(moves, key=moves.get)

    def copy_board(self, board):
        return deepcopy(board)
