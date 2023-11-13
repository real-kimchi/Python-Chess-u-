import pytest
from chess.model import Game, Bishop, Rook, Queen, Knight, Pawn, King, Board

# Sample function to set up a board in a specific configuration

def setup_board(game, moves):
    game.set_up_pieces()  # Make sure to set up the board before making moves
    for move in moves:
        game.accept_move(move)

def test_initial_pawn_position():
    game = Game()
    game.set_up_pieces()
    assert isinstance(game.board.get('e2'), Pawn) and game.board.get('e2')._is_white

def test_direct_checkmate():
    game = Game()
    setup_board(game, ['f2f3', 'e7e5', 'g2g4', 'd8h4']) # This sequence should lead to a checkmate
    assert game.is_checkmate(True) == True # White is checkmated

def test_not_checkmate_but_in_check():
    game = Game()
    setup_board(game, ['e2e4', 'f7f6', 'd1h5', 'g7g6']) # Black is in check but not checkmate
    assert game.is_checkmate(False) == False

def test_not_checkmate_not_in_check():
    game = Game()
    setup_board(game, ['e2e4', 'e7e5']) # Game has just started, no check
    assert game.is_checkmate(False) == False