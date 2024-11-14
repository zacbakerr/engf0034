from board import Direction, Rotation, Action
from random import Random

import board

class Player:
    def choose_action(self, board):
        raise NotImplementedError

class NonRandomPlayer(Player):
    def __init__(self, seed=None):
        self.random = Random(seed)
        self.GAP_WEIGHT = 35.0
        self.HEIGHT_WEIGHT = 2.0
        self.LINE_WEIGHT = -30.0
        self.BUMPINESS_WEIGHT = 2.5

        self.last_move = None
        self.last_discard = 0
        self.move_count = 0
    
    def choose_action(self, board):
        self.move_count += 1
        curr_gaps = self.calculate_gaps(board)
        try:
            if board.falling is None:
                return None
            
            heights = self.get_column_heights(board)
            max_height = max(heights) if heights else 0
            if max_height > (board.height * 0.65) and board.bombs_remaining > 0:
                max_height_col = heights.index(max_height)
                test_board = board.clone()
                test_moves = []
                
                current_x = test_board.falling.left
                steps = max_height_col - current_x
                
                if steps < 0:
                    for _ in range(abs(steps)):
                        test_moves.append(Direction.Left)
                elif steps > 0:
                    for _ in range(steps):
                        test_moves.append(Direction.Right)
                        
                test_moves.append(Action.Bomb)
                return test_moves[0]
            
            best_score = 999999999999999
            best_moves = []
            
            for rot_count in range(4):
                for x in range(board.width):
                    test_board = board.clone()
                    test_moves = []

                    num_blocks = len(test_board.cells) + len(test_board.falling.cells)
                    
                    for _ in range(rot_count):
                        test_moves.append(Rotation.Clockwise)
                        test_board.rotate(Rotation.Clockwise)
                    
                    current_x = test_board.falling.left
                    steps = x - current_x
                    
                    if steps < 0:
                        for _ in range(abs(steps)):
                            test_moves.append(Direction.Left)
                            test_board.move(Direction.Left)
                    elif steps > 0:
                        for _ in range(steps):
                            test_moves.append(Direction.Right)
                            test_board.move(Direction.Right)
                    
                    test_moves.append(Direction.Drop)
                    test_board.move(Direction.Drop)

                    completed_lines = (num_blocks - len(test_board.cells)) / test_board.width
                    
                    score = self.evaluate_board(test_board, int(completed_lines))

                    if score < best_score:
                        best_score = score
                        best_moves = test_moves.copy()
                        best_board = test_board

            added_gaps = self.calculate_gaps(best_board) - curr_gaps
            if best_board.discards_remaining > 0 and added_gaps > 0: return Action.Discard
            self.last_move = best_moves[0]
            return best_moves[0]
        
        except Exception as e:
            return Direction.Drop
    
    def evaluate_board(self, board, completed_lines):
        heights = self.get_column_heights(board)
        bumpiness = sum(abs(heights[i] - heights[i+1]) for i in range(len(heights)-1))
        
        max_height = max(heights) if heights else 0

        if max_height == board.height: return 99999999
        
        gaps = self.calculate_gaps(board)
        
        almost_complete_lines = self.count_almost_complete_lines(board) 
        
        if completed_lines == 4: return -99999999
        if board.height * 0.65 < max_height and completed_lines == 3: return -99999999
        if board.height * 0.7 < max_height and completed_lines == 2: return -99999999
        if board.height * 0.75 < max_height and completed_lines == 1: return -99999999

        if gaps > 1 and completed_lines == 3 and board.discards_remaining == 0: return -99999999
        if gaps > 2 and completed_lines == 2 and board.discards_remaining == 0: return -99999999
        if gaps > 3 and completed_lines == 1 and board.discards_remaining == 0: return -99999999
        
        if board.height * 0.6 > max_height:
            score = (gaps * self.GAP_WEIGHT +
                    max_height * self.HEIGHT_WEIGHT +
                    almost_complete_lines * self.LINE_WEIGHT +
                    bumpiness * self.BUMPINESS_WEIGHT)
        else:
            score = (gaps * self.GAP_WEIGHT * 20 +
                    max_height * self.HEIGHT_WEIGHT * 20 +
                    completed_lines * self.LINE_WEIGHT * 100 +
                    bumpiness * self.BUMPINESS_WEIGHT)

        return score
    
    def calculate_gaps(self, board):
        gaps = 0
        for x in range(board.width):
            found_block = False
            for y in range(board.height):
                if (x, y) in board.cells:
                    found_block = True
                elif found_block:
                    gaps += 1
        return gaps
    
    def get_column_heights(self, board):
        heights = []
        for x in range(board.width):
            for y in range(board.height):
                if (x, y) in board.cells:
                    heights.append(board.height - y)
                    break
            else:
                heights.append(0)
        return heights
    
    def count_complete_lines(self, board):
        complete_lines = 0
        for y in range(board.height):
            if sum(1 for x in range(board.width) if (x, y) in board.cells) == board.width:
                complete_lines += 1
        return complete_lines

    def count_almost_complete_lines(self, board):
        almost_complete_lines = 0
        for y in range(board.height):
            if sum(1 for x in range(board.width) if (x, y) in board.cells) == board.width - 1:
                almost_complete_lines += 1
        return almost_complete_lines

SelectedPlayer = NonRandomPlayer