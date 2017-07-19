"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random
from random import randint
import math

class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

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
    
    
    # Distance from centre
    w, h = game.width / 2., game.height / 2.
    y, x = game.get_player_location(player)
    score = float(math.sqrt(((h - y)**2 + (w - x)**2)))
    return score



def custom_score_2(game, player):
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
    ## Move comparison score
    
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    totalScore = 0
    #empty_board_places = len(game.get_blank_spaces())
    
    y, x = game.get_player_location(player)
    for h,w in game.get_blank_spaces():
        score = ((h - y)**2 + (w - x)**2)
        totalScore = totalScore + score
    
    
    return float(totalScore)


def custom_score_3(game, player):
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
    
    # My moves 
    my_moves = len(game.get_legal_moves(player))
    
    # Enemy Moves
    # Punish if enemy has more moves - this tries to minimize 
    enemy_moves = len(game.get_legal_moves(game.get_opponent(player)))
    return float(my_moves*my_moves - 1.7*enemy_moves*enemy_moves)


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

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

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move
    
    def minimax(self, game, depth):
        return self.actual_minimax(game, depth)[1]
    

    def actual_minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        
        # Get Legal Moves First
        legal_moves = game.get_legal_moves()
        
        # Firstly assess that there is no  no legal moves
        if not legal_moves or depth <= 0:
            return self.score(game, self), None
        
        
        # DEtermine if we max or are a min player
        # If we are the active player, we would obviously want to maximize.
        if game.active_player == self:
            maximizing_player = True
        else:
            maximizing_player = False
        
        # Set the best score
        if maximizing_player:
            best_val = float("-inf")
        else:
            best_val = float("inf")
        
        # Now begin Finding Best_move
        best_move = None
        
        #Go through each move
        if maximizing_player:
            for move in legal_moves:
                forecast_the_move = game.forecast_move(move)
                val, _ = self.actual_minimax(forecast_the_move, depth-1)
                if val > best_val:
                    best_val, best_move = val, move
        else:
            for move in legal_moves:
                forecast_the_move = game.forecast_move(move)
                val, _ = self.actual_minimax(forecast_the_move, depth-1)
                if val < best_val:
                    best_val, best_move = val, move
        
        return best_val, best_move
        


class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

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

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)
        
        # Deep Learing iterative search
        # In this case, we need to terminate if no legal moves
        if len(game.get_legal_moves(self)) == 0:
            return (-1,-1)
        
        

        #try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
        # Basically brute force thorugh as many as possible
        for depth in range(1,1000):
            try:
                best_move = self.alphabeta(game, depth)
            # it should autobreak given a Searchtimeout
            except:
                break
            
        return best_move
        
        

        #except SearchTimeout:
        #    pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        #return best_move
        
    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        
        return self.actual_alphabeta(game, depth)[1]

    def actual_alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf"),maximizing_player = True):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

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

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if depth == 0:
            return self.score(game, self), game.get_player_location(self)

        best_score = float('-inf') if maximizing_player else float('inf')
        best_move = (-1, -1)
        # Much cleaner to allocate to opponenet turns
        possible_moves = game.get_legal_moves(self) if maximizing_player else game.get_legal_moves(
            game.get_opponent(self))

        if len(possible_moves) == 0:
            return self.score(game, self), (-1, -1)
        
        #This time seperate the player by max or not max
        
        for move in possible_moves:
            forecast_move = game.forecast_move(move)
            score, _move = self.actual_alphabeta(forecast_move, depth - 1, alpha, beta, not maximizing_player)

            if maximizing_player:
                # We want to compare the best scores and is associated with ALPHA
                if score >= best_score:
                    best_score = score
                    best_move = move
                if best_score >= beta:
                    return best_score, best_move
                alpha = max(best_score, alpha)

            else:
                 # We want to compare the best scores and is associated with BETA
                if score <= best_score:
                    best_score = score
                    best_move = move
                if best_score <= alpha:
                    return best_score, best_move
                beta = min(best_score, beta)

        return best_score, best_move
    
    


  