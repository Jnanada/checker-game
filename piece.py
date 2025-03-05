from typing import Tuple, TypedDict
import json

import streamlit as st
from constants import ROWS, ColorEnum, ColorInitialEnum, DirectionEnum
from helper import CheckerEncoder


class Position(TypedDict):
    """
    Class that holds the value for row and column.
    """

    row: int
    col: int


class Piece:
    """ "
    Class that indicates the Piece on the board.
    """

    def __init__(self, row: int, col: int, color: Tuple):
        """
        Initializes the Piece object with row, col and color.
        Color is either RED or BLACK.
        For simplicity, RED is placed on the top and black on the bottom.

        :param row (int): Row Position of the Piece.
        :param col (int): Column Position of the Piece.
        :param color (Tuple): Color of the Piece to define the Players.
        """
        self._row = row
        self._col = col
        self.color = color
        # Set the King to False
        self.king = False
        # Set the Position with the row, column values.
        self.position: Position = {"row": self._row, "col": self._col}
        # Set the direction based on the color of the piece.
        self.set_direction()

    def __str__(self):
        """
        String representation of the Piece object.

        :return Json representation of the object
        """
        return json.dumps(self, cls=CheckerEncoder)

    def __repr__(self):
        return (
            ColorInitialEnum.R.value
            if self.color == ColorEnum.RED.value
            else ColorInitialEnum.B.value
        )

    def move(self, row: int, col: int) -> None:
        """
        Update the position based on the new row and column values"""
        self._row = self.position["row"] = row
        self._col = self.position["col"] = col

    def set_direction(self) -> None:
        """
        Define the directio based on the Piece.
        If Piece is King, set the direction to BOTH.
        Set to FORWARD(1) for RED piece and BACKWARD(-1) to BLACK piece.
        """
        if self.king:
            self.direction = DirectionEnum.BOTH
        if self.color == ColorEnum.RED.value:
            self.direction = DirectionEnum.FORWARD
        elif self.color == ColorEnum.BLACK.value:
            self.direction = DirectionEnum.BACKWARD

    def set_king(self) -> None:
        """
        Make the Piece a King. King can move diagonally forwards and backwards.
        """
        self.king = True
        # Update the direction to Both (FORWARD & BACKWARD)
        self.set_direction()

    def get_immediate_moves(self):
        all_immediate_moves: list[Position] = []
        if self.king:
            all_immediate_moves.append(
                {"row": self.position["row"] - 1, "col": self.position["col"] - 1}
            )
            all_immediate_moves.append(
                {"row": self.position["row"] - 1, "col": self.position["col"] + 1}
            )
            all_immediate_moves.append(
                {"row": self.position["row"] + 1, "col": self.position["col"] - 1}
            )
            all_immediate_moves.append(
                {"row": self.position["row"] + 1, "col": self.position["col"] - 1}
            )
        else:
            if self.direction == DirectionEnum.FORWARD:
                all_immediate_moves.append(
                    {"row": self.position["row"] + 1, "col": self.position["col"] + 1}
                )
                all_immediate_moves.append(
                    {"row": self.position["row"] + 1, "col": self.position["col"] - 1}
                )
            else:
                all_immediate_moves.append(
                    {"row": self.position["row"] - 1, "col": self.position["col"] - 1}
                )
                all_immediate_moves.append(
                    {"row": self.position["row"] - 1, "col": self.position["col"] + 1}
                )
        return all_immediate_moves

    def has_reached_opponent_end(self) -> bool:
        """
        Checks if the piece has reached the opponent's side, and returns True if so. Otherwise returns False.

        :param piece (Piece): The current Piece object.
        :return: True if the piece has reached the opponent's side, otherwise False.
        """
        if self.color == ColorEnum.RED.value:
            return True if self.position["row"] == ROWS - 1 else False
        if self.color == ColorEnum.BLACK.value:
            return True if self.position["row"] == 0 else False
