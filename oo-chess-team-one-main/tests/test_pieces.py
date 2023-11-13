from chess.model import Pawn

# Ensure that pieces are equal if they are the same color and type and not otherwise
def test_identity():
    pawn1 = Pawn(is_white=True)
    pawn2 = Pawn(is_white=True)
    pawn3 = Pawn(is_white=False)
    assert pawn1 == pawn2
    assert not pawn1 == pawn3
