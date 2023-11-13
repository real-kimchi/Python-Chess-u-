import pytest
from chess.model import Board, Pawn

# Ensure that the board is initialized correctly
def test_board_ctor():
    board = Board()
    board.set('e2', Pawn(is_white=True))
    assert board.get('e2') == Pawn(is_white=True)
    assert board.get('e4') == None
