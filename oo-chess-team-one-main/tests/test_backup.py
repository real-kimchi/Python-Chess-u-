import pytest
from chess.model import Game, Bishop, Rook, Queen, Knight, Pawn, King, Board

def test_undo_move():
    game = Game()
    game.set_up_pieces()  # Sets up the initial board

    # Make a move that can be undone
    move = 'e2e4'  # Pawn moves from e2 to e4
    game.accept_move(move)

    # The square e4 should now have a white pawn, and e2 should be empty
    assert isinstance(game.board.get('e4'), Pawn)
    assert game.board.get('e2') is None

    # Now undo the move
    game.undo_move()

    # After undo, e2 should have the white pawn back, and e4 should be empty
    assert isinstance(game.board.get('e2'), Pawn)
    assert game.board.get('e4') is None
