import random
import copy
import time

class Teeko2Player:
    """ An object representation for an AI game player for the game Teeko2.
    """
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']

    def __init__(self):
        """ Initializes a Teeko2Player object by randomly selecting red or black as its
        piece color.
        """
        self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]

    def make_move(self, state):
        """ Selects a (row, col) space for the next move. You may assume that whenever
        this function is called, it is this player's turn to move.

        Args:
            state (list of lists): should be the current state of the game as saved in
                this Teeko2Player object. Note that this is NOT assumed to be a copy of
                the game state and should NOT be modified within this method (use
                place_piece() instead). Any modifications (e.g. to generate successors)
                should be done on a deep copy of the state.

                In the "drop phase", the state will contain less than 8 elements which
                are not ' ' (a single space character).

        Return:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

        Note that without drop phase behavior, the AI will just keep placing new markers
            and will eventually take over the board. This is not a valid strategy and
            will earn you no points.
        """

        # minimax algorithm to play better
        move = []
        
        best = self.max_value(state, 3, True)
        best_state = best[1]
        for r in range(5):
            for c in range(5):
                if state[r][c] != best_state[r][c]: 
                    if best_state[r][c] == ' ':
                        move.insert(1, (r,c)) # source location
                    elif state[r][c] == ' ':
                        move.insert(0, (r,c)) # destination 


        return move

    def succ(self, move_piece, state):
        piece_count = 0
        drop_phase = True
        for r in state:
            for c in range(5):
                if r[c]!=' ':piece_count += 1
        if piece_count >= 8: drop_phase = False
        x = []
        # In drop phase, all empty spots are legal
        if drop_phase:
            for r in range(5):
                for c in range(5):
                    if state[r][c]==' ':
                        new_state = copy.deepcopy(state)
                        new_state[r][c] = move_piece
                        x.append(new_state)

        # In move phase, all empty spot adjacent to current piece are legal
        elif not drop_phase:
            # Find current location of all four pieces
            curr = []
            for r in range(5):
                for c in range(5):
                    if state[r][c]==move_piece:
                        curr.append((r,c))
            for piece in curr:
                for r in range(piece[0]-1, piece[0]+2):
                    for c in range(piece[1]-1, piece[1] +2):
                        if 0<=r<5 and 0<=c<5 and state[r][c] == ' ' :
                            # spot is within board range, is empty
                            new_state = copy.deepcopy(state)
                            new_state[piece[0]][piece[1]] = ' '
                            new_state[r][c] = move_piece
                            x.append(new_state)


        return x

    def heuristic_game_value(self, state):
        #if self.game_value(state) != 0: return self.game_value(state)
        hgv = 0

        # check horizontal 
        for row in state:
            for i in range(2):
                for n in range(4):
                    if row[i+n] == self.opp: hgv-=1 
                    if row[i+n] == self.my_piece: hgv+=1

        # check vertical
        for col in range(5):
            for i in range(2):
                for n in range(4):
                    if state[i+n][col] == self.opp: hgv-=1  
                    if state[i+n][col] == self.my_piece: hgv+=1 
        # check \ diagonal
        for r in range(2):
            for c in range(2):
                for n in range(4):
                    if state[r+n][c+n] == self.opp : hgv-=1 
                    if state[r+n][c+n] == self.my_piece : hgv+=1 
        # check / diagonal
        for r in range(2):
            for c in range(3,5):
                for n in range(4):
                    if state[r+n][c-n] == self.opp : hgv-=1 
                    if state[r+n][c-n] == self.my_piece : hgv+=1 
        # check 3x3 square corners
        for r in range(1,4):
            for c in range(1,4):
                if state[r][c] == ' ':
                    for n in [(r+1,c+1),(r+1,c-1),(r-1, c+1),(r-1,c-1)]:
                        if state[n[0]][n[1]] == self.opp : hgv-=1 
                        if state[n[0]][n[1]] == self.my_piece: hgv+=1 
        return hgv/100
    
    def max_value(self, state, depth, nextTurn):
        if self.game_value(state) != 0:
            return (self.game_value(state), state, depth)
        elif depth == 0:
            return (self.heuristic_game_value(state), state, depth)
        elif nextTurn:
            max = (-1, state, 0)
            x = self.succ(self.my_piece, state)
            for y in x: #Score the best possible next move
                curr = self.max_value( y, depth-1,False)
                if curr[0] >= max[0]: max = (curr[0], y) 
            return max
        elif not nextTurn:
            min = (1, state, 0)
            x = self.succ(self.opp, state)
            for y in x: #Score the best possible next move for opponent
                curr = self.max_value(y, depth-1,True)
                if curr[0] <= min[0]: min = (curr[0], y) 
            return min

    def opponent_move(self, move):
        """ Validates the opponent's next move against the internal board representation.
        You don't need to touch this code.

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
        """
        # validate input
        if len(move) > 1:
            source_row = move[1][0]
            source_col = move[1][1]
            if source_row != None and self.board[source_row][source_col] != self.opp:
                self.print_board()
                print(move)
                raise Exception("You don't have a piece there!")
            if abs(source_row - move[0][0]) > 1 or abs(source_col - move[0][1]) > 1:
                self.print_board()
                print(move)
                raise Exception('Illegal move: Can only move to an adjacent space')
        if self.board[move[0][0]][move[0][1]] != ' ':
            raise Exception("Illegal move detected")
        # make move
        self.place_piece(move, self.opp)

    def place_piece(self, move, piece):
        """ Modifies the board representation using the specified move and piece

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

                This argument is assumed to have been validated before this method
                is called.
            piece (str): the piece ('b' or 'r') to place on the board
        """
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = ' '
        self.board[move[0][0]][move[0][1]] = piece

    def print_board(self):
        """ Formatted printing for the board """
        for row in range(len(self.board)):
            line = str(row)+": "
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")

    def game_value(self, state):
        """ Checks the current board status for a win condition

        Args:
        state (list of lists): either the current state of the game as saved in
            this Teeko2Player object, or a generated successor state.

        Returns:
            int: 1 if this Teeko2Player wins, -1 if the opponent wins, 0 if no winner

        TODO: complete checks for diagonal and 3x3 square corners wins
        """
        # check horizontal wins
        for row in state:
            for i in range(2):
                if row[i] != ' ' and row[i] == row[i+1] == row[i+2] == row[i+3]:
                    #print("Horizontal win!")
                    
                    return 1 if row[i]==self.my_piece else -1

        # check vertical wins
        for col in range(5):
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i+1][col] == state[i+2][col] == state[i+3][col]:
                    #print("Vertical win!")
                    return 1 if state[i][col]==self.my_piece else -1

        # check \ diagonal wins
        for r in range(2):
            for c in range(2):
                if state[r][c] != ' ' and state[r][c] == state[r+1][c+1] == state[r+2][c+2] ==state[r+3][c+3]:
                    #print("\ diagonal win!")
                    return 1 if state[r][c]==self.my_piece else -1 
        
        # check / diagonal wins
        for r in range(2):
            for c in range(3,5):
                if state[r][c] != ' ' and state[r][c] == state[r+1][c-1] == state[r+2][c-2] ==state[r+3][c-3]:
                    #print("/ diagonal win!")
                    return 1 if state[r][c]==self.my_piece else -1 
        
        # check 3x3 square corners wins
        for r in range(1,4):
            for c in range(1,4):
                if state[r][c] == ' ' and state[r+1][c+1] != ' ' and state[r+1][c+1] == state[r+1][c-1] == state[r-1][c+1] == state[r-1][c-1]:
                    #print('Square win!')
                    return 1 if state[r][c]==self.my_piece else -1 

        return 0 # no winner yet

############################################################################
#
# THE FOLLOWING CODE IS FOR SAMPLE GAMEPLAY ONLY
#
############################################################################
def main():
    print('Hello, this is Samaritan')
    ai = Teeko2Player()
    piece_count = 0
    turn = 0

    # drop phase
    while piece_count < 8 and ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved at "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                player_move = input("Move (e.g. B3): ")
                while player_move[0] not in "ABCDE" or player_move[1] not in "01234":
                    player_move = input("Move (e.g. B3): ")
                try:
                    ai.opponent_move([(int(player_move[1]), ord(player_move[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        piece_count += 1
        turn += 1
        turn %= 2

    # move phase - can't have a winner until all 8 pieces are on the board
    while ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved from "+chr(move[1][1]+ord("A"))+str(move[1][0]))
            print("  to "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                move_from = input("Move from (e.g. B3): ")
                while move_from[0] not in "ABCDE" or move_from[1] not in "01234":
                    move_from = input("Move from (e.g. B3): ")
                move_to = input("Move to (e.g. B3): ")
                while move_to[0] not in "ABCDE" or move_to[1] not in "01234":
                    move_to = input("Move to (e.g. B3): ")
                try:
                    ai.opponent_move([(int(move_to[1]), ord(move_to[0])-ord("A")),
                                    (int(move_from[1]), ord(move_from[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        turn += 1
        turn %= 2

    ai.print_board()
    if ai.game_value(ai.board) == 1:
        print("AI wins! Game over.")
    else:
        print("You win! Game over.")


if __name__ == "__main__":
    main()
