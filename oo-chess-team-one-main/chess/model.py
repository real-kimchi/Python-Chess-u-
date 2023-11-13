"""Chess Game model."""
from typing import Optional
import re


class Board:
    def __init__(self):
        self._squares = dict()

    def get(self, location:str) -> Optional['Piece']:
        return self._squares.get(location, None)

    def set(self, location:str, piece: 'Piece'):
        self._squares[location] = piece

    def remove(self, location: str):
        if location in self._squares:
            del self._squares[location]

    def deep_copy(self):
        new_board = Board()
        # Only copy pieces that are not None
        new_board._squares = {location: piece.copy() if piece is not None else None for location, piece in self._squares.items()}
        return new_board
    
    def copy(self):
        return self.deep_copy()

class Piece:
    """Abstract base class for chess pieces."""
    def __init__(self, is_white: bool) -> None:
        self._is_white = is_white

    def __hash__(self):
        return hash((type(self), self._is_white))

    def __eq__(self, other: "Piece") -> bool:
        return hash(self) == hash(other)

    def copy(self):
        # Return a new instance of the same piece
        return type(self)(self._is_white)

##first implementation of chess game without use of object oriented class logic

class Pawn(Piece):
    #TODO: Implement this class by encapsulating movement rules for this piece here
    pass

class Rook(Piece):
    #TODO: Implement this class by encapsulating movement rules for this piece here
    pass

class Knight(Piece):
    #TODO: Implement this class by encapsulating movement rules for this piece here
    pass

class Bishop(Piece):
    #TODO: Implement this class by encapsulating movement rules for this piece here
    pass

class Queen(Piece):
    #TODO: Implement this class by encapsulating movement rules for this piece here
    pass

class King(Piece):
    #TODO: Implement this class by encapsulating movement rules for this piece here
    pass


class Game:
    def __init__(self, debug = False):
        self.board = Board()
        self.white_to_play = True
        self.game_over = False
        self.debug = debug
        self.move_history = []

    def save_state(self, captured_piece=None):
        # Create a deep copy of the board, current turn, and any captured piece
        state = {
            'board': self.board.deep_copy(),
            'white_to_play': self.white_to_play,
            'captured_piece': captured_piece  # Store the captured piece, if any
        }
        self.move_history.append(state)

    def undo_move(self):
        """
        Undo the last move.
        """
        if not self.move_history:
            print("No moves to undo.")
            return

        # Restore the last saved state
        last_state = self.move_history.pop()
        self.board = last_state['board']
        self.white_to_play = last_state['white_to_play']
        # Restore any additional state information as needed
        # ...

        # If a piece was captured, restore it to its previous location
        captured_piece = last_state['captured_piece']
        if captured_piece:
            self.board.set(captured_piece['location'], captured_piece['piece'])

    def accept_move(self, move):
        # TODO: Implement updating the board with the give move

        self.save_state()

        # check the format of move
        pattern = re.compile(r"[a-h][1-8][a-h][1-8]")
        if bool(pattern.match(move)) == False:
            raise Exception("Incorrect Format: Please enter a move in the format of 'a1a2' and try again.")

        prevLocation = move[:2]
        newLocation = move[2:]
        piece = self.board.get(prevLocation)
        captured_piece = self.board.get(newLocation)

        # check for move a non-existent piece
        if piece == None:
            raise Exception("Illegal Move: Moving a non-existent piece!")

        # check for move my opponent's piece
        if (piece._is_white != self.white_to_play) and (self.debug == False):
            raise Exception("Illegal Move: Moving your opponent's piece!")

        # check for move my Bishop to any square not on its diagonal
        # print(type(piece) == Bishop)
        if (type(piece) == Bishop):
            dx = abs(ord(newLocation[:1]) - ord(prevLocation[:1]))
            dy = abs(ord(newLocation[1:]) - ord(prevLocation[1:]))
            if (dx != dy):
                raise Exception("Illegal Move: Moving a Bishop to any square not on its diagonal!")

        # check for move my rook to any square not on its row or column.
        if (type(piece) == Rook):
            dx = abs(ord(newLocation[:1]) - ord(prevLocation[:1]))
            dy = abs(ord(newLocation[1:]) - ord(prevLocation[1:]))
            if (dx != 0 and dy != 0):
                raise Exception("Illegal Move: Moving a Rook to any square not on its row or column!")

        # check for move my queen to any square not on its row, column, or diagonal.
        if (type(piece) == Queen):
            dx = abs(ord(newLocation[:1]) - ord(prevLocation[:1]))
            dy = abs(ord(newLocation[1:]) - ord(prevLocation[1:]))
            if (dx != 0 and dy != 0) and (dx != dy):
                raise Exception("Illegal Move: Moving a queen to any square not on its row, column, or diagonal!")

        # check for move my knight to any square not 3x2 squares aware.
        if (type(piece) == Knight):
            dx = abs(ord(newLocation[:1]) - ord(prevLocation[:1]))
            dy = abs(ord(newLocation[1:]) - ord(prevLocation[1:]))
            if (dx + dy != 3 or dx == 0 or dy == 0):
                raise Exception("Illegal Move: Moving a knight to any square not 3x2 squares aware!")

        # check for move any piece other than a knight over existing pieces.
        if (type(piece) != Knight):
            dx = abs(ord(newLocation[:1]) - ord(prevLocation[:1]))
            dy = abs(ord(newLocation[1:]) - ord(prevLocation[1:]))

            collision_warning = "Illegal Move: Moving any piece other than a knight over existing pieces!"
            # if moving on same row or column
            if dx != dy:
                # check for collision on same row
                # left to right
                if (ord(newLocation[:1]) > ord(prevLocation[:1])):
                    for char in range(ord(prevLocation[:1])+1, ord(newLocation[:1]), 1):
                        temp = chr(char) + newLocation[1:]
                        if (self.board.get(temp) != None):
                            raise Exception(collision_warning)

                # right to left
                if (ord(newLocation[:1]) < ord(prevLocation[:1])):
                    for char in range(ord(prevLocation[:1])-1, ord(newLocation[:1]), -1):
                        temp = chr(char) + newLocation[1:]
                        if (self.board.get(temp) != None):
                            raise Exception(collision_warning)

                # check for collision on same column
                # bottom to top
                if (ord(newLocation[1:]) > ord(prevLocation[1:])):
                    for char in range(ord(prevLocation[1:])+1, ord(newLocation[1:]), 1):
                        temp = newLocation[:1] + chr(char)
                        if (self.board.get(temp) != None):
                            raise Exception(collision_warning)

                # top to bottom
                if (ord(newLocation[1:]) < ord(prevLocation[1:])):
                    for char in range(ord(prevLocation[1:])-1, ord(newLocation[1:]), -1):
                        temp = newLocation[:1] + chr(char)
                        if (self.board.get(temp) != None):
                            raise Exception(collision_warning)

            # if moving on diagonal
            if dx == dy:
                # left-bottom to right-top
                if (ord(newLocation[:1]) > ord(prevLocation[:1])):
                    y_coordinate = prevLocation[1:]
                    for char in range(ord(prevLocation[:1])+1, ord(newLocation[:1]), 1):
                        y_coordinate = int(y_coordinate)+1
                        temp = chr(char) + str(y_coordinate)
                        if (self.board.get(temp) != None):
                            raise Exception(collision_warning)

                # right-top to left-bottom
                if (ord(newLocation[:1]) < ord(prevLocation[:1])):
                    y_coordinate = prevLocation[1:]
                    for char in range(ord(prevLocation[:1])-1, ord(newLocation[:1]), -1):
                        y_coordinate = int(y_coordinate)-1
                        temp = chr(char) + str(y_coordinate)
                        if (self.board.get(temp) != None):
                            raise Exception(collision_warning)

        # check for move any piece to a square occupied by another of my pieces.
        if (self.board.get(newLocation) != None):
            if (piece._is_white == self.board.get(newLocation)._is_white):
                raise Exception("Illegal Move: Moving any piece to a square occupied by another of your pieces!")

        # check for move my pawn in violation of pawn-movement rules.
        if (type(piece) == Pawn):
            dx = abs(ord(newLocation[:1]) - ord(prevLocation[:1]))
            dy = (ord(newLocation[1:]) - ord(prevLocation[1:]))

            pawn_illegal_move_warning = "Illegal Move: Moving a pawn in violation of pawn-movement rules!"

            # Move forward
            if (dx == 0):
                if (piece._is_white):
                    if (dy < 0):
                        raise Exception(pawn_illegal_move_warning)
                    if(int(prevLocation[1:])==2 and dy>2):
                        raise Exception(pawn_illegal_move_warning)
                    if(int(prevLocation[1:])!=2 and dy>1):
                        raise Exception(pawn_illegal_move_warning)
                else:
                    dy = -dy
                    if (dy < 0):
                        raise Exception(pawn_illegal_move_warning)
                    if(int(prevLocation[1:])==7 and dy>2):
                        raise Exception(pawn_illegal_move_warning)
                    if(int(prevLocation[1:])!=7 and dy>1):
                        raise Exception(pawn_illegal_move_warning)
                if(self.board.get(newLocation) != None):
                    raise Exception(pawn_illegal_move_warning)

            # move too far
            if (dx > 1 or (dx == 1 and abs(dy) > 1)):
                raise Exception(pawn_illegal_move_warning)

            # move in the same row
            if (dx == 1 and dy == 0):
                raise Exception(pawn_illegal_move_warning)

            # capture enemy
            if (dx == abs(dy)):
                if (piece._is_white):
                    if (dy < 0):
                        raise Exception(pawn_illegal_move_warning)
                else:
                    dy = -dy
                    if (dy < 0):
                        raise Exception(pawn_illegal_move_warning)
                if (self.board.get(newLocation) == None):
                    raise Exception(pawn_illegal_move_warning)

        # check for move my king in violation of king-movement rules.
        if (type(piece) == King):
            dx = abs(ord(newLocation[:1]) - ord(prevLocation[:1]))
            dy = abs(ord(newLocation[1:]) - ord(prevLocation[1:]))

            # move my king two squares towards my rook and see the rook also moved to complete a castle.
            if (dx == 2 and dy == 0):
                # castling for white king
                if piece._is_white and (prevLocation == "d1"):
                    # white king castling to right
                    if (newLocation == "f1") and (type(self.board.get("h1")) == Rook) and (self.board.get("e1") == None) and (self.board.get("f1") == None) and (self.board.get("g1") == None):
                        # move king to f1
                        self.board.set(prevLocation, None)
                        self.board.set(newLocation, King(is_white=True))
                        # move rook to e1
                        self.board.set("h1", None)
                        self.board.set("e1", Rook(is_white=True))
                        # check if the move causes a check
                        if self.is_check(piece._is_white):
                            # Undo the move
                            self.board.set(prevLocation, piece)
                            self.board.set(newLocation, captured_piece)
                            self.board.set("h1", Rook(is_white=True))
                            self.board.set("e1", None)
                            # Since the move causes the king to be in check, it's not a valid move
                            raise Exception("Illegal Move: This move would leave your king in check.")
                    # white king castling to left
                    elif (newLocation == "b1") and (type(self.board.get("a1")) == Rook) and self.board.get("b1") == None and self.board.get("c1") == None:
                        # move king to b1
                        self.board.set(prevLocation, None)
                        self.board.set(newLocation, King(is_white=True))
                        # move rook to c1
                        self.board.set("a1", None)
                        self.board.set("c1", Rook(is_white=True))
                        # check if the move causes a check
                        if self.is_check(piece._is_white):
                            # Undo the move
                            self.board.set(prevLocation, piece)
                            self.board.set(newLocation, captured_piece)
                            self.board.set("a1", Rook(is_white=True))
                            self.board.set("c1", None)
                            # Since the move causes the king to be in check, it's not a valid move
                            raise Exception("Illegal Move: This move would leave your king in check.")

                # castling for black king
                elif not piece._is_white and prevLocation == "d8":
                    # black king castling to right
                    if (newLocation == "f8") and (type(self.board.get("h8")) == Rook) and (self.board.get("e8") == None) and (self.board.get("f8") == None) and (self.board.get("g8") == None):
                        # move king to f8
                        self.board.set(prevLocation, None)
                        self.board.set(newLocation, King(is_white=False))
                        # move rook to e8
                        self.board.set("h8", None)
                        self.board.set("e8", Rook(is_white=False))
                        # check if the move causes a check
                        if self.is_check(piece._is_white):
                            # Undo the move
                            self.board.set(prevLocation, piece)
                            self.board.set(newLocation, captured_piece)
                            self.board.set("h8", Rook(is_white=False))
                            self.board.set("e8", None)
                            # Since the move causes the king to be in check, it's not a valid move
                            raise Exception("Illegal Move: This move would leave your king in check.")
                    # black king castling to left
                    elif (newLocation == "b8") and (type(self.board.get("a8")) == Rook) and self.board.get("b8") == None and self.board.get("c8") == None:
                        # move king to b8
                        self.board.set(prevLocation, None)
                        self.board.set(newLocation, King(is_white=False))
                        # move rook to c8
                        self.board.set("a8", None)
                        self.board.set("c8", Rook(is_white=False))
                        # check if the move causes a check
                        if self.is_check(piece._is_white):
                            # Undo the move
                            self.board.set(prevLocation, piece)
                            self.board.set(newLocation, captured_piece)
                            self.board.set("a8", Rook(is_white=False))
                            self.board.set("c8", None)
                            # Since the move causes the king to be in check, it's not a valid move
                            raise Exception("Illegal Move: This move would leave your king in check.")

                # not satisfy the castling rules but seems like attempting to castle
                else:
                    raise Exception("Illegal Move: Moving the king more than one square or performing castling incorrectly.")

            # normal king movement
            elif (dx > 1 or dy > 1):
                raise Exception("Illegal Move: Moving the king more than one square.")

        #TODO check for make any other moves prohibited by movement rules

        self.board.set(newLocation, piece)
        self.board.set(prevLocation, None)

        # Check if the move causes a check
        if self.is_check(piece._is_white):
            # Undo the move
            self.board.set(prevLocation, piece)
            self.board.set(newLocation, captured_piece)
            # self.undo_move(piece, prevLocation, newLocation, captured_piece)

            # Since the move causes the king to be in check, it's not a valid move
            raise Exception("Illegal Move: This move would leave your king in check.")

        self.white_to_play = not self.white_to_play

    def is_check(self, is_white):
        # Check if the current player's king is in check.
        
        # Find the king's position
        king_position = None
        for location, piece in self.board._squares.items():
            if isinstance(piece, King) and piece._is_white == is_white:
                king_position = location
                break

        # If the king's position isn't found, return False (should not happen in a valid game)
        if king_position is None:
            return False

        # Check all squares to see if any piece of the opposite color can attack the king
        for location, piece in self.board._squares.items():
            if piece and piece._is_white != is_white:
                if self.can_piece_attack(piece, location, king_position):
                    return True
        return False

    def can_piece_attack(self, piece, start, end):
        
        #Determine if a piece can attack the square at 'end' from its current 'start' position.
        #This method checks if a move is theoretically possible for the given piece type.
        
        start_col, start_row = start[0], int(start[1])
        end_col, end_row = end[0], int(end[1])
        dx = abs(ord(end_col) - ord(start_col))
        dy = abs(end_row - start_row)

        if isinstance(piece, Bishop):
            if dx == dy:
                return self.is_path_clear(start, end, dx, dy)
            return False

        if isinstance(piece, Rook):
            if dx == 0 or dy == 0:
                return self.is_path_clear(start, end, dx, dy)
            return False

        if isinstance(piece, Queen):
            if dx == dy or dx == 0 or dy == 0:
                return self.is_path_clear(start, end, dx, dy)
            return False

        if isinstance(piece, Knight):
            return (dx == 2 and dy == 1) or (dx == 1 and dy == 2)

        if isinstance(piece, Pawn):
            dy = end_row - start_row if piece._is_white else start_row - end_row
            if dx == 1 and dy == 1:  # Diagonal capture
                target_piece = self.board.get(end)
                if target_piece and target_piece._is_white != piece._is_white:
                    return True  # There is an opponent's piece to capture
            return False  # No capture possible

        if isinstance(piece, King):
            return dx <= 1 and dy <= 1  # King can move one square in any direction

        return False

    def is_path_clear(self, start, end, dx, dy):
        """
        Check if the path is clear for the piece to move from start to end. This does not include the end square.
        """
        if dx == 0:  # Moving vertically
            step = 1 if start[1] < end[1] else -1
            for y in range(int(start[1]) + step, int(end[1]), step):
                if self.board.get(f'{start[0]}{y}') is not None:
                    return False
        elif dy == 0:  # Moving horizontally
            step = 1 if start[0] < end[0] else -1
            for x in range(ord(start[0]) + step, ord(end[0]), step):
                if self.board.get(f'{chr(x)}{start[1]}') is not None:
                    return False
        else:  # Moving diagonally
            step_x = 1 if start[0] < end[0] else -1
            step_y = 1 if start[1] < end[1] else -1
            for x, y in zip(range(ord(start[0]) + step_x, ord(end[0]), step_x),
                            range(int(start[1]) + step_y, int(end[1]), step_y)):
                if self.board.get(f'{chr(x)}{y}') is not None:
                    return False
        return True

    def set_up_pieces(self):
        """Place pieces on the board as per the initial setup."""
        for col in 'abcdefgh':
            self.board.set(f'{col}2', Pawn(is_white=True))
            self.board.set(f'{col}7', Pawn(is_white=False))

        # set up black Rook
        self.board.set('a8', Rook(is_white=False))
        self.board.set('h8', Rook(is_white=False))

        # set up white Rook
        self.board.set('a1', Rook(is_white=True))
        self.board.set('h1', Rook(is_white=True))

        # set up black Knight
        self.board.set('b8', Knight(is_white=False))
        self.board.set('g8', Knight(is_white=False))

        # set up white Knight
        self.board.set('b1', Knight(is_white=True))
        self.board.set('g1', Knight(is_white=True))

        # set up black Bishop
        self.board.set('c8', Bishop(is_white=False))
        self.board.set('f8', Bishop(is_white=False))

        # set up white Bishop
        self.board.set('c1', Bishop(is_white=True))
        self.board.set('f1', Bishop(is_white=True))

        # set up black King
        self.board.set('e8', King(is_white=False))

        # set up white King
        self.board.set('e1', King(is_white=True))

        # set up black Queen
        self.board.set('d8', Queen(is_white=False))

        # set up white Queen
        self.board.set('d1', Queen(is_white=True))


    def can_attack(self, piece, from_pos, to_pos):
        #Determine if a piece can attack the square at 'to_pos' from its current 'from_pos' position.
        #This method checks if a move is theoretically possible for the given piece type.
        
        start_col, start_row = from_pos[0], int(from_pos[1])
        end_col, end_row = to_pos[0], int(to_pos[1])
        dx = abs(ord(end_col) - ord(start_col))
        dy = abs(end_row - start_row)

        # Check if the target position is occupied by a piece of the same color
        target_piece = self.board.get(to_pos)
        if target_piece and target_piece._is_white == piece._is_white:
            return False  # Can't capture your own piece

        if isinstance(piece, Bishop):
            if dx == dy:
                return self.is_path_clear(from_pos, to_pos, dx, dy)

        elif isinstance(piece, Rook):
            if dx == 0 or dy == 0:
                return self.is_path_clear(from_pos, to_pos, dx, dy)

        elif isinstance(piece, Queen):
            if dx == dy or dx == 0 or dy == 0:
                return self.is_path_clear(from_pos, to_pos, dx, dy)

        elif isinstance(piece, Knight):
            return (dx == 2 and dy == 1) or (dx == 1 and dy == 2)

        elif isinstance(piece, Pawn):
            # Include pawn's forward movement for non-capturing moves
            dy = end_row - start_row if piece._is_white else start_row - end_row
            if dx == 0 and (dy == 1 or (dy == 2 and ((start_row == 2 and piece._is_white) or (start_row == 7 and not piece._is_white)))):
                return self.board.get(to_pos) is None  # Forward move is only possible if the target square is empty
            elif dx == 1 and dy == 1:  # Diagonal capture
                return target_piece is not None and target_piece._is_white != piece._is_white  # Must be an opponent's piece to capture

        elif isinstance(piece, King):
            # Normal king movement
            if dx <= 1 and dy <= 1:
                return True
            # Castling
            elif dy == 0 and dx == 2:
                return False
            else:
                return False
        # other conditions to consider?

    def generate_legal_moves(self, is_white):
        legal_moves = []

        for pos, piece in self.board._squares.items():
            if piece is not None and piece._is_white == is_white:
                for target_pos in self.board._squares:
                    if self.is_legal_move(piece, pos, target_pos):
                        legal_moves.append((pos, target_pos))

        return legal_moves

    def is_legal_move(self, piece, from_pos, to_pos):
        # If the destination is the same as the starting point, it's not a move
        if from_pos == to_pos:
            return False

        # Check for valid movement patterns for the given piece
        if not self.can_piece_attack(piece, from_pos, to_pos):
            return False

        # Calculate dx and dy based on the current and target positions
        dx = ord(to_pos[0]) - ord(from_pos[0])  # Difference in files (columns)
        dy = int(to_pos[1]) - int(from_pos[1])  # Difference in ranks (rows)

        # Check if the path is clear for pieces that require it (rooks, bishops, queens)
        if not isinstance(piece, Knight) and not self.is_path_clear(from_pos, to_pos, dx, dy):
            return False


        # Check for castling legality
        if isinstance(piece, King) and abs(ord(to_pos[0]) - ord(from_pos[0])) == 2:
            return self.can_castle(piece.is_white, from_pos, to_pos)

        # Make the move on a temporary copy of the board to see if it would put the king in check
        temp_game = Game()
        temp_game.board = self.board.copy()
        try:
            temp_game.accept_move(from_pos + to_pos)
            if temp_game.is_check(piece.is_white):
                return False
        except Exception as e:
            # If accept_move throws an exception, the move is illegal
            return False

        # If all checks pass, the move is legal
        return True

    def can_castle(self, is_white, from_pos, to_pos):
        # Check if the king has moved, which would make castling illegal
        if self.has_king_moved(is_white):
            return False

        # Determine the direction of the castling move
        direction = 1 if to_pos[0] > from_pos[0] else -1

        # Check if the path between the king and the rook is clear
        if not self.is_path_clear_for_castling(is_white, from_pos, direction):
            return False

        # Check if the king is currently in check
        if self.is_check(is_white):
            return False

        # Check if any of the squares the king would move through are under attack
        if self.is_king_passing_through_attack(is_white, from_pos, direction):
            return False

        # If all checks pass, castling is legal
        return True


    def make_move(self, move):
        from_pos, to_pos = move
        piece = self.board.get(from_pos)

        # Perform the move
        self.board.set(to_pos, piece)
        self.board.set(from_pos, None)

        # Change the player turn
        self.white_to_play = not self.white_to_play

    def is_checkmate(self, is_white):
        # If the player is not currently in check, it's not a checkmate
        if not self.is_check(is_white):
            return False

        # Generate all legal moves for the player
        legal_moves = self.generate_legal_moves(is_white)

        # If there are no legal moves, and the player is in check, it's checkmate
        if not legal_moves:
            return True

        # Try each move to see if it gets the king out of check
        for move in legal_moves:
            # Make the move on a copy of the board
            board_copy = self.board.copy()
            board_copy.make_move(move)

            # If after making the move, the player is not in check, it's not a checkmate
            if not board_copy.is_check(is_white):
                return False

        # If no moves get the king out of check, it's checkmate
        return True