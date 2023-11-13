import pytest
from chess.model import Game, Bishop, Rook, Queen, Knight, Pawn, King, Board

@pytest.fixture(autouse=True)
def game():
    game = Game(debug=True)
    yield game

def test_valid_move(game):
    game.set_up_pieces()
    # Test if a valid move is accepted and the board is updated
    move = 'a2a4'
    game.accept_move(move)
    assert game.board.get('a4') == Pawn(is_white=True)

def test_invalid_move(game):
    # Test if an invalid move is rejected and the board is not updated
    move = 'b2b5'
    with pytest.raises(Exception):
        game.accept_move(move)

def test_nonexistent_piece(game):
    # Test if the player is able to move a non-existent piece
    move = 'a3a4'
    with pytest.raises(Exception):
        game.accept_move(move)

def test_invalid_format(game):
    # Test if an ill-formatted move is rejected and the board is not updated
    move = 'b2b'
    with pytest.raises(Exception):
        game.accept_move(move)

def test_player_turn():
    # Instantiate a game with debug mode off
    game = Game()
    # Test if a move is rejected when it is not the player's turn
    # i.e. don't allow a player to move their opponent's piece
    move = 'a7a5'
    with pytest.raises(Exception):
        game.accept_move(move)

def test_pawn_move(game):
    game.board.set('a4', Pawn(is_white=True))

    # Test if a pawn is only allowed to move forward
    move = 'a4a3'
    with pytest.raises(Exception):
        game.accept_move(move)

    # Test if a pawn can move forward 2 squares on its first move
    game.set_up_pieces()
    move = 'c2c4'
    game.accept_move(move)
    assert game.board.get('c4') == Pawn(is_white=True)

    # Test if a pawn can move forward 1 square on its subsequent moves
    move = 'c4c5'
    game.accept_move(move)
    assert game.board.get('c5') == Pawn(is_white=True)

    # Test if a pawn can move diagonally to capture an opponent's piece
    game.board.set('b5', Pawn(is_white=False))
    move = 'a4b5'
    game.accept_move(move)
    assert game.board.get('b5') == Pawn(is_white=True)

    # Test if a pawn can't move diagonally to a square not occupied by an opponent's piece
    move = 'b6c7'
    with pytest.raises(Exception):
        game.accept_move(move)

    # Test if a pawn can't move diagonally to a square occupied by an opponent's piece
    game.board.set('c7', Pawn(is_white=False))
    with pytest.raises(Exception):
        game.accept_move(move)

    # Test if a pawn can't move diagonally to a square occupied by a friendly piece
    game.board.set('c7', Pawn(is_white=True))
    with pytest.raises(Exception):
        game.accept_move(move)

def test_bishop_move(game):
    bishop = Bishop(is_white=True)
    game.board.set('c1', bishop)

    # Test if bishop can't move to a square not on its diagonal
    with pytest.raises(Exception):
        game.accept_move('c1d3')

    # Test if it can move to a square on its diagonal
    game.board.set('b2', bishop)
    game.accept_move('b2c3')
    assert game.board.get('c3') == bishop

def test_rook_move(game):
    rook = Rook(is_white=True)
    game.board.set('c1', rook)

    # Test if rook can't move to a square not on its row or column
    with pytest.raises(Exception):
        game.accept_move('c1d3')

    # Test if it can move to a square on its row or column
    game.accept_move('c1c3')
    assert game.board.get('c3') == rook

def test_queen_move(game):
    queen = Queen(is_white=True)

    # Test if queen can't move to a square not on its row, column, or diagonal
    game.board.set('d1', queen)
    with pytest.raises(Exception):
        game.accept_move('d1e3')

    # Test if it can move to a square on its column
    game.accept_move('d1d3')
    assert game.board.get('d3') == queen

    # Test if it can move to a square on its row
    game.accept_move('d3d5')
    assert game.board.get('d5') == queen

    # Test if it can move to a square on its diagonal
    game.accept_move('d5e6')
    assert game.board.get('e6') == queen

def test_knight_move(game):
    knight = Knight(is_white=True)
    game.board.set('b1', knight)

    # Test if knight can't move to a square not 3x2 squares away
    with pytest.raises(Exception):
        game.accept_move('b1c4')

    # Test if it can move to a square 3x2 squares away
    game.accept_move('b1c3')
    assert game.board.get('c3') == knight

    # Test if it can't move to a square 3 squares above its current square
    with pytest.raises(Exception):
        game.accept_move('c3c6')

    # Test if it can't move to a square 3 squares to the right of its current square
    with pytest.raises(Exception):
        game.accept_move('c3f3')


def test_king_move(game):
    king = King(is_white=True)
    game.board.set('e1', king)

    # Test if king can't move to a square not 1 square away
    with pytest.raises(Exception):
        game.accept_move('e1e3')

    # Test if it can move to a square 1 square away
    game.accept_move('e1e2')
    assert game.board.get('e2') == king

def test_piece_over_existing_pieces(game):
    # Test if a rook can't move over an existing piece
    rook1 = Rook(is_white=True)
    obstacle = Rook(is_white=True)
    game.board.set('d1', rook1)
    game.board.set('d2', obstacle)

    # Test if a bishop can't move over an existing piece
    bishop1 = Bishop(is_white=True)
    game.board.set('e1', bishop1)
    with pytest.raises(Exception):
        game.accept_move('e1d2')

    # Test if a knight can move over an existing piece
    knight1 = Knight(is_white=True)
    game.board.set('c1', knight1)
    game.accept_move('c1e2')

def test_king_in_check(game):
    # Test if move results in king being in check
    king = King(is_white=True)
    queen = Queen(is_white=False)
    game.board.set('e1', king)
    game.board.set('e8', queen)

    with pytest.raises(Exception):
        game.accept_move('e1e2')

def test_castling_white_king_move_right(game):
    king = King(is_white=True)
    rook = Rook(is_white=True)
    game.board.set('d1', king)
    game.board.set('h1', rook)
    
    # Test if there is obstruction between king and rook
    game.board.set('e1', rook)
    with pytest.raises(Exception):
        game.accept_move('d1f1')
    
    # Test if castling is allowed
    game.board.set('e1', None)
    game.accept_move('d1f1')
    assert game.board.get('f1') == king
    assert game.board.get('e1') == rook

    # Test if castling is not allowed if king has moved
    with pytest.raises(Exception):
        game.accept_move('f1h1')  

def test_castling_black_king_move_left(game):
    king = King(is_white=False)
    rook = Rook(is_white=False)
    game.board.set('d8', king)
    game.board.set('a8', rook)
    
    # Test if there is obstruction between king and rook
    game.board.set('c8', rook)
    with pytest.raises(Exception):
        game.accept_move('d8b8')
    
    # Test if castling is allowed
    game.board.set('c8', None)
    game.accept_move('d8b8')
    assert game.board.get('b8') == king
    assert game.board.get('c8') == rook

    # Test if castling is not allowed if king has moved
    game.accept_move('c8h8')
    with pytest.raises(Exception):
        game.accept_move('b8d8')  
    





