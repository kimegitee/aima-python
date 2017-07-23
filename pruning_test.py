from games import Game, alphabeta_search

infinity = float('inf')

def alphabeta_search_alt(state, game):
    """Search game to determine best action; use alpha-beta pruning.
    As in [Figure 5.7], this version searches all the way to the leaves."""

    player = game.to_move(state)

    # Functions used by alphabeta
    def max_value(state, alpha, beta):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = -infinity
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a), alpha, beta))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = infinity
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a), alpha, beta))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    # Body of alphabeta_cutoff_search:
    best_score = -infinity
    beta = infinity
    best_action = None
    for a in game.actions(state):
        v = min_value(game.result(state, a), best_score, beta)
        # =================================================================
        # This is a verbatim copy of the official implementation with only
        # one change that we use >= instead of > for best_score
        # =================================================================
        if v >= best_score:
            best_score = v
            best_action = a
    return best_action

class TestGame(Game):
	"""Test case for pruning.

	A 2-ply game tree whose terminal nodes have the following values:
	                  ______
	                 |      |
	                 | root |
	                 |______|
	                   /_\
	                    |
	    ________________|_____________________
	   |                |                     |
	 __|__            __|__                 __|__
	|     |          |     |               |     |
	|  A  |          |  B  |               |  C  | 
	|_____|          |_____|               |_____|
	  \_/              \_/                   \_/
	   |                |                     |
	   |           _____|____            _____|____
	   |          |          |          |          |
	 __|__      __|__      __|__      __|__      __|__   	
	|     |    |     |    |     |    |     |    |     |
	|  3  |    |  3  |    | -6  |    |  3  |    | -9  | 
	|_____|    |_____|    |_____|    |_____|    |_____|

	Node values after running Minimax
	                  ______
	                 |      |
	                 |  3   |
	                 |______|
	                   /_\
	                    |
	    ________________|_____________________
	   |                |                     |
	 __|__            __|__                 __|__
	|     |          |     |               |     |
	|  3  |          | -6  |               | -9  | 
	|_____|          |_____|               |_____|
	  \_/              \_/                   \_/
	   |                |                     |
	   |           _____|____            _____|____
	   |          |          |          |          |
	 __|__      __|__      __|__      __|__      __|__   	
	|     |    |     |    |     |    |     |    |     |
	|  3  |    |  3  |    | -6  |    |  3  |    | -9  | 
	|_____|    |_____|    |_____|    |_____|    |_____|

	The optimal move for this game tree is A


	Running AlphaBeta on the tree gives the following values
	                  ______
	                 |      |
	                 |  3   |
	                 |______|
	                   /_\
	                    |
	    ________________|_____________________
	   |                |                     |
	 __|__            __|__                 __|__
	|     |          |     |               |     |
	|  3  |          | <=3 |               | <=3 | 
	|_____|          |_____|               |_____|
	  \_/              \_/                   \_/
	   |                |                     |
	   |           _____|____            _____|____
	   |          |          |          |          |
	 __|__      __|__      __|__      __|__      __|__   	
	|     |    |     |    |     |    |     |    |     |
	|  3  |    |  3  |    |prune|    |  3  |    |prune|
	|_____|    |_____|    |_____|    |_____|    |_____|

	If the current best move that root can find is updated with every new 
	min node value >= current best value, for this game tree AlphaBeta 
	will recommend C. This is not the optimal move

	If move is only updated if new found value exceeds current best value,
	subsequent moves evaluated with the same score are discarded. AlphaBeta 
	recommends A, which is the optimal move. 

	AlphaBeta should only recommend the move whose value caused alpha to 
	change.
	"""

	succs = dict(root=dict(a='A', b='B', c='C'),
		A=dict(a1='A1'),
		B=dict(b1='B1', b2='B2'),
		C=dict(c1='C1', c2='C2'))

	utils = dict(A1=3, B1=3, B2=-6, C1=3, C2='-9')

	initial = 'root'

	def actions(self, state):
		return list(self.succs.get(state, {}).keys())

	def result(self, state, move):
		return self.succs[state][move]

	def utility(self, state, player):
		if player == 'MAX':
			return self.utils[state]
		else:
			return -self.utils[state]

	def terminal_test(self, state):
		return state not in ('root', 'A', 'B', 'C')

	def to_move(self, state):
		return 'MIN' if state in 'ABC' else 'MAX'


if __name__ == '__main__':
	game = TestGame()
	print('Official implementation recommends', alphabeta_search('root', game))
	print('Making one change from > to >= recommends', alphabeta_search_alt('root', game))