class TicTacToe:
    def __init__(self):
        self.board = [" " for _ in range(9)]
        self.current_winner = None

    def print_board(self):
        for row in [self.board[i:i+3] for i in range(0, 9, 3)]:
            print("| " + " | ".join(row) + " |")

    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == " "]

    def empty_squares(self):
        return " " in self.board

    def num_empty_squares(self):
        return self.board.count(" ")

    def make_move(self, square, letter):
        if self.board[square] == " ":
            self.board[square] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False

    def winner(self, square, letter):
        # Row check
        row_ind = square // 3
        row = self.board[row_ind*3:(row_ind+1)*3]
        if all([spot == letter for spot in row]):
            return True

        # Column check
        col_ind = square % 3
        column = [self.board[col_ind+i*3] for i in range(3)]
        if all([spot == letter for spot in column]):
            return True

        # Diagonal check
        if square % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 4, 8]]
            diagonal2 = [self.board[i] for i in [2, 4, 6]]
            if all([spot == letter for spot in diagonal1]) or \
               all([spot == letter for spot in diagonal2]):
                return True

        return False


class AIPlayer:
    def __init__(self, letter):
        self.letter = letter

    def get_move(self, game):
        if len(game.available_moves()) == 9:
            return 4  # Take center first
        else:
            return self.minimax(game, self.letter)['position']

    def minimax(self, state, player):
        max_player = self.letter
        other_player = "O" if player == "X" else "X"

        if state.current_winner == other_player:
            return {
                'position': None,
                'score': 1 * (state.num_empty_squares() + 1)
                if other_player == max_player else
                -1 * (state.num_empty_squares() + 1)
            }

        elif not state.empty_squares():
            return {'position': None, 'score': 0}

        if player == max_player:
            best = {'position': None, 'score': -float('inf')}
        else:
            best = {'position': None, 'score': float('inf')}

        for possible_move in state.available_moves():
            state.make_move(possible_move, player)
            sim_score = self.minimax(state, other_player)

            state.board[possible_move] = " "
            state.current_winner = None
            sim_score['position'] = possible_move

            if player == max_player:
                if sim_score['score'] > best['score']:
                    best = sim_score
            else:
                if sim_score['score'] < best['score']:
                    best = sim_score

        return best


def play():
    game = TicTacToe()
    ai = AIPlayer("O")

    print("You are X. AI is O")
    game.print_board()

    while game.empty_squares():
        # Human Move
        square = int(input("Enter position (0-8): "))
        if game.make_move(square, "X"):
            game.print_board()
            if game.current_winner:
                print("🎉 You win!")
                return

        # AI Move
        ai_move = ai.get_move(game)
        game.make_move(ai_move, "O")
        print("\nAI chose position:", ai_move)
        game.print_board()
        if game.current_winner:
            print("🤖 AI wins!")
            return

    print("🤝 It's a Draw!")


if __name__ == "__main__":
    play()