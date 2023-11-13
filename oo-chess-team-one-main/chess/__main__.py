import chess.model as model
import chess.view as view

# Instructions for the player
instructions = """
Welcome to Python Chess by Team One!

Instructions:
- Enter moves in algebraic notation (e.g., 'e2e4' for moving a piece from e2 to e4).
- To castle, input 'kcastle' for kingside or 'qcastle' for queenside castling (if legal).
- For pawn promotion, enter the move followed by the piece you want to promote to (e.g., 'e7e8Q' for Queen, 'R' for Rook, 'B' for Bishop, 'N' for Knight).
- Enter 'u' or 'backup' to undo the last move.
- Enter 'q' to quit the game.

White begins the game.
"""

print(instructions)

game = model.Game()
game.set_up_pieces()

while not game.game_over:
    print("")
    print(view.board_to_text(game.board))
    prompt = "White to play:" if game.white_to_play else "Black to play:"
    move = input(prompt).lower()  # Convert input to lowercase for consistency

    # Handle special commands
    if move == 'u' or move == 'backup':
        game.undo_move()
        continue
    
    elif move == 'q':
        print("Game has been quit.")
        break

    # Process a regular move
    try:
        game.accept_move(move)
        # Check for checkmate immediately after the move
        if game.is_checkmate(game.white_to_play):
            # print the board after checkmate
            print("")
            print(view.board_to_text(game.board))
            game.game_over = True
            winner = "White" if not game.white_to_play else "Black"
            print(f"Checkmate, {winner} Wins!")
    except Exception as e:  # Catch the exception to provide feedback
        print(f"You made an illegal move: {e}, please try again")
        continue


    # Check for checkmate
    if game.is_checkmate(not game.white_to_play):
        game.game_over = True
        winner = "White" if game.white_to_play else "Black"
        print(f"Checkmate, {winner} Wins!")
        continue  # This allows for the 'undo' command after checkmate
