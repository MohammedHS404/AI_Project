# -*- coding: utf-8 -*-
"""AIProject.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Hd_ImKy6a_6Cr9yhBx4PtMwKQkdlCMRx
"""

import math
import random

use_agent = True

print(f"Agent active {use_agent}")

# Define board dimensions
ROWS = 6
COLS = 7

def create_board():
  return [['-' for j in range(COLS)] for i in range(ROWS)]

# Print initial board state
def print_board(board):
    for row in board:
        print('|' + '|'.join(row) + '|')
    print(' ' + '-'.join(['-' for i in range(COLS)]))

# manual
def get_player_input_manual(player):
    while True:
        try:
            col = int(input(f"Player {player}, choose a column (1-{COLS}): ")) - 1
            if col < 0 or col >= COLS:
                print(f"Column must be between 1 and {COLS}")
            else:
                return col
        except ValueError:
            print("Invalid input. Please enter a number.")

def evaluate_board(board, player):
    # Check for horizontal wins
    for row in board:
        for i in range(COLS - 3):
            window = row[i:i+4]
            if window.count(player) == 4:
                return 100

    # Check for vertical wins
    for i in range(COLS):
        col = [board[row][i] for row in range(ROWS)]
        for j in range(ROWS - 3):
            window = col[j:j+4]
            if window.count(player) == 4:
                return 100

    # Check for diagonal wins (down-right)
    for i in range(ROWS - 3):
        for j in range(COLS - 3):
            window = [board[i+k][j+k] for k in range(4)]
            if window.count(player) == 4:
                return 100

    # Check for diagonal wins (up-right)
    for i in range(3, ROWS):
        for j in range(COLS - 3):
            window = [board[i-k][j+k] for k in range(4)]
            if window.count(player) == 4:
                return 100

    # If no winning moves, return a neutral score
    return 0

def minimax(board, depth,maximizingPlayer, currentPlayer, alpha=-math.inf, beta=math.inf):
    if check_win(board, 'X') or check_win(board, 'O') or depth == 0:
        return evaluate_board(board, 'X')

    if maximizingPlayer:
        best_score = -math.inf
        for col in range(COLS):
            new_board = [row[:] for row in board]
            if add_piece(new_board, col, 'X'):
                score = minimax(new_board, depth-1, False, currentPlayer,alpha, beta)
                best_score = max(best_score, score)
                alpha = max(alpha, best_score)
                if alpha >= beta:
                    break
        return best_score
    else:
        best_score = math.inf
        for col in range(COLS):
            new_board = [row[:] for row in board]
            if add_piece(new_board, col, 'O'):
                score = minimax(new_board, depth-1, True, currentPlayer, alpha, beta)
                best_score = min(best_score, score)
                beta = min(beta, best_score)
                if alpha >= beta:
                    break
        return best_score

def is_valid_location(board, row,col):
    return board[row][col] == '-'

def get_legal_moves(board):
    legal_moves = []
    for column in range(COLS):
        if is_valid_location(board,ROWS-1,column):
            legal_moves.append(column)
    return legal_moves

# mimax 
def get_player_input_minmax(player,agent_plays_as, board):
    if player == agent_plays_as:
        print("Agent's Turn")
        # Use minimax to choose the best column
        best_score = -math.inf
        best_col = None
        for col in range(COLS):
            # Simulate a move by the maximizing player
            new_board = [row[:] for row in board]
            if add_piece(new_board, col, 'X'):
                # Call minimax to get the score for this move
                score = minimax(new_board, 4, False, player)
                # Update the best score and column if the new score is better
                if score > best_score:
                    best_score = score
                    best_col = col
        
        if(best_col is None):

          print("No best solution was found will random");
          legal_moves = get_legal_moves(board)
          best_col = random.choice(legal_moves)

        return best_col
    else:
        print("Human's Turn")
        return get_player_input_manual(player)

def add_piece(board, col, piece):
    for row in range(ROWS-1, -1, -1):
        if is_valid_location(board,row,col):
            board[row][col] = piece
            return True
    return False

def get_player_input(player,agent_plays_as, board):
  if(use_agent is True):
    return get_player_input_minmax(player,agent_plays_as,board);
  else:
    return get_player_input_manual(player);

def check_win(board, piece):
    # Check rows for win
    for row in range(ROWS):
        for col in range(COLS-3):
            if board[row][col] == piece and board[row][col+1] == piece and board[row][col+2] == piece and board[row][col+3] == piece:
                return True
    
    # Check columns for win
    for col in range(COLS):
        for row in range(ROWS-3):
            if board[row][col] == piece and board[row+1][col] == piece and board[row+2][col] == piece and board[row+3][col] == piece:
                return True
    
    # Check diagonal (down-right) for win
    for col in range(COLS-3):
        for row in range(ROWS-3):
            if board[row][col] == piece and board[row+1][col+1] == piece and board[row+2][col+2] == piece and board[row+3][col+3] == piece:
                return True
    
    # Check diagonal (up-right) for win
    for col in range(COLS-3):
        for row in range(3, ROWS):
            if board[row][col] == piece and board[row-1][col+1] == piece and board[row-2][col+2] == piece and board[row-3][col+3] == piece:
                return True
    
    return False

def switch_players(player):
    if player == 1:
        return 2
    else:
        return 1

def play():
      # Play game
    player = 1

    agent_plays_as = 1;

    print(f"Agent is player {agent_plays_as}")

    board = create_board()

    print ("initial board")

    print_board(board)

    print("Games starts")

    while True:

        # Get player input
        col = get_player_input(player,agent_plays_as, board)

        # Add piece to board
        if not add_piece(board, col, 'X' if player == 1 else 'O'):
            print("Column is full. Please choose another column.")
            continue

        print_board(board)

        # Check for win
        if check_win(board, 'X' if player == 1 else 'O'):
            if(agent_plays_as is player):
              print("Agent wins!")
            else:
              print(f"Player {player} wins!")
            break

        # Switch players
        player = switch_players(player)

play();
