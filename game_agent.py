"""This file contains all the classes you must complete for this project.

You can use the test cases in agent_test.py to help during development, and
augment the test suite with your own test cases to further test your code.

You must test your agent's strength against a set of agents with known
relative strength using tournament.py and include the results in your report.
"""
import random
import math

class Timeout(Exception):
    """Subclass base exception for code clarity."""
    pass

def heuristic_1(game, player):
    # This heuristic expand the legal moves to one level further

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))

    return((own_moves) / (1+opp_moves))



def heuristic_2(game, player):
    # This heuristic tries to stick to the center of the board while pushing
    # the opponent away from the center

    opp = game.get_opponent(player)

    player_location = game.get_player_location(player)
    opp_location = game.get_player_location(opp)

    centerwidth = game.width/2
    centerheight = game.height/2
    player_distance_to_center = math.sqrt(((player_location[0] - centerwidth) ** 2 + (player_location[1] - centerheight) ** 2))
    opp_distance_to_center = math.sqrt(((opp_location[0] - centerwidth) ** 2 + (opp_location[1] - centerheight) ** 2))

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(opp))
    return own_moves - player_distance_to_center - opp_moves + opp_distance_to_center

def heuristic_4(game, player):
    """
    own_moves = game.get_legal_moves(player)
    own_moves_num = len(own_moves)
    for move in own_moves:
        own_moves_num += len(game.forecast_move(move).get_legal_moves(player))

    opp = game.get_opponent(player)
    opp_moves = game.get_legal_moves()
    opp_moves_num = len(opp_moves)
    for move in opp_moves:
        opp_moves_num += len(game.forecast_move(move).get_legal_moves(opp))

    return float(own_moves_num - opp_moves_num)

    :param game:
    :param player:
    :return:
    """


    # This heuristic tries to stick to the center of the board while pushing
    # the opponent away from the center
    opponent = game.get_opponent(player)

    player_moves = game.get_legal_moves(player)
    num_player_moves = len(player_moves)

    opponent_moves = game.get_legal_moves(opponent)
    num_opponent_moves = len(opponent_moves)
   # board_covered = 1 - (len(game.get_blank_spaces()) / float(game.height * game.width))

    player_next_moves = sum([game.__get_moves__(move) for move in game.get_legal_moves(player)], [])
    opponent_next_moves = sum([game.__get_moves__(move) for move in game.get_legal_moves(opponent)], [])

    # player_last_move = game.get_player_location(player)
    # opponent_last_move = game.get_player_location(player)

    # plm_r, plm_c = player_last_move
    # olm_r, olm_c = opponent_last_move

    # player_empty_spaces_nearby = sum([(plm_r - i, plm_c - j) in game.get_blank_spaces() for i in [-2, -1, 0, 1, 2] for j in [-2, -1, 0, 1, 2]])
    # opp_empty_spaces_nearby = sum([(olm_r - i, olm_c - j) in game.get_blank_spaces() for i in [-2, -1, 0, 1, 2] for j in [-2, -1, 0, 1, 2]])
    # distance_to_opponent = abs(plm_r - olm_r) + abs(plm_c - olm_c)
    # distance_to_center = sqrt((plm_r-game.height)**2 + (plm_c-game.width)**2)

    #move_diff = num_player_moves - num_opponent_moves

    # return sign(move_diff)*(move_diff)**2 + len(player_next_moves) - len(opponent_next_moves)
    # return move_diff + sign(move_diff)*max(num_player_moves/num_opponent_moves, num_opponent_moves/num_player_moves) #+ 2*len(player_next_moves)
    # return move_diff + sign(move_diff) * max(num_player_moves / num_opponent_moves, num_opponent_moves / num_player_moves)*100.0 - distance_to_opponent
    #calc_1 = ((num_player_moves - num_opponent_moves) / min(num_player_moves, num_opponent_moves))

    return ((len(player_next_moves) - len(opponent_next_moves)))


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")



    #Heuristic 1
    #return float(own_moves - opp_moves)

    # Heuristic 2
    #return float(own_moves - 2*opp_moves)
    # Heuristic 3
    #return ((own_moves)/opp_moves)
    return heuristic_4(game, player)
    # Heuristic 4
   # return (math.exp((own_moves) - opp_moves))


    #raise NotImplementedError


class CustomPlayer:
    """Game-playing agent that chooses a move using your evaluation function
    and a depth-limited minimax algorithm with alpha-beta pruning. You must
    finish and test this player to make sure it properly uses minimax and
    alpha-beta to return a good move before the search time limit expires.

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    iterative : boolean (optional)
        Flag indicating whether to perform fixed-depth search (False) or
        iterative deepening search (True).

    method : {'minimax', 'alphabeta'} (optional)
        The name of the search method to use in get_move().

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """

    def __init__(self, search_depth=3, score_fn=custom_score,
                 iterative=True, method='minimax', timeout=10.):
        self.search_depth = search_depth
        self.iterative = iterative
        self.score = score_fn
        self.method = method
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

    def get_move(self, game, legal_moves, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        This function must perform iterative deepening if self.iterative=True,
        and it must use the search method (minimax or alphabeta) corresponding
        to the self.method value.

        **********************************************************************
        NOTE: If time_left < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        legal_moves : list<(int, int)>
            A list containing legal moves. Moves are encoded as tuples of pairs
            of ints defining the next (row, col) for the agent to occupy.

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """

        self.time_left = time_left

        # Perform any required initializations, including selecting an initial
        # move from the game board (i.e., an opening book), or returning
        # immediately if there are no legal moves

        best_move = (-1, -1)
        if len(legal_moves) == 0:
            return best_move
        called_method = self.minimax
        if self.method == "alphabeta":
            called_method = self.alphabeta
        try:
            # The search method call (alpha beta or minimax) should happen in
            # here in order to avoid timeout. The try/except block will
            # automatically catch the exception raised by the search method
            # when the timer gets close to expiring
            # pass
            if self.iterative:
                current_best_move = best_move
                i = 0
                while True:
                    _,best_move = called_method(game,i)
                    i +=1
            else:
                _, best_move = called_method(game,self.search_depth)

        except Timeout:
            # Handle any actions required at timeout, if necessary
            pass

        # Return the best move from the last completed search iteration
        return best_move

    def minimax(self, game, depth, maximizing_player=True):
        """Implement the minimax search algorithm as described in the lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.

        Algorithm
        ---------
            if depth = 0 or node is a terminal node
                return the heuristic value of node (using self.score())
            if maximizingPlayer
                bestValue := −∞
                for each child of node
                    v := minimax(child, depth − 1, FALSE)
                    bestValue := max(bestValue, v)
                return bestValue
            else    (* minimizing player *)
                bestValue := +∞
                for each child of node
                    v := minimax(child, depth − 1, TRUE)
                    bestValue := min(bestValue, v)
                return bestValue
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        legal_moves = game.get_legal_moves()

        if len(legal_moves) == 0 or depth == 0:
            return self.score(game, self), (-1, -1)
        best_move = ()
        if maximizing_player:
            best_value = -float("inf")
            for a in legal_moves:
                v, _ = self.minimax(game.forecast_move(a), depth - 1, False)
                best_value = max(best_value, v)
                # check if we just updated the best value with v
                if best_value == v:
                    best_move = a
            return best_value, best_move

        else:
            best_value = float("inf")
            for a in legal_moves:
                v, _ = self.minimax(game.forecast_move(a), depth - 1, True)
                best_value = min(best_value, v)
                if best_value == v:
                    best_move = a
            return best_value, best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf"), maximizing_player=True):
        """Implement minimax search with alpha-beta pruning as described in the
        lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        """Search game to determine best action; use alpha-beta pruning.
           This version cuts off search and uses an evaluation function."""

        legal_moves = game.get_legal_moves()

        if len(legal_moves) == 0 or depth == 0:
            return self.score(game, self), (-1, -1)
        best_move = ()
        if maximizing_player:
            best_value = -float("inf")
            for a in legal_moves:
                v, _ = self.alphabeta(game.forecast_move(a), depth - 1, alpha, beta, False)
                best_value = max(best_value, v)
                if best_value == v:
                    best_move = a
                # if best value is higher than beta => prune
                if best_value >= beta:
                    return best_value, best_move
                alpha = max(alpha, best_value)
            return best_value, best_move

        else:
            best_value = float("inf")
            for a in legal_moves:
                v, _ = self.alphabeta(game.forecast_move(a), depth - 1, alpha, beta, True)
                best_value = min(best_value, v)
                if best_value == v:
                    best_move = a
                # if best value is lower than alpha => prune
                if best_value <= alpha:
                    return best_value, best_move
                # else update beta value
                beta = min(beta, best_value)
            return best_value, best_move
