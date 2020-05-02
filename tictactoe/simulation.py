
from tictactoe.agent import Agent
from tictactoe.board import Board
from tictactoe.learning import Trainer

from tqdm import tqdm
import random

player1_symbol = Board.playerX
player2_symbol = Board.playerO

def simulate(iterations = 10000, agent1 = None, agent2 = None, exploration = False, save_agent1 = None, load_agent1 = None, eval=False):

    # Construct game board
    game = Board()
    exploration_probability = 1
    
    # Construct agents
    if load_agent1 is None:
        if agent1 is None:
            agent1 = Agent(player1_symbol, game)
        else:
            agent1.assignState(game)
            agent1.symbol = player1_symbol
    else:
        agent1 = Agent(player1_symbol, game, load_trainer=load_agent1)
    
    if agent2 is None:
        agent2 = Agent(player2_symbol, game)
    else:
        agent2.assignState(game)
        agent2.symbol = player2_symbol

    # Counters for wins of each agent and total number of games
    nbr_wins_agent1 = 0
    nbr_wins_agent2 = 0
    nbr_games = 0

    # Pick current player
    current_player = player1_symbol

    # Start iterations
    for i in tqdm(range(iterations)):

        # Check if games has ended, reset if True
        if game.checkGameEnded():
            nbr_games += 1

            game.resetGame()
            agent1.updatePossibleActions()
            agent2.updatePossibleActions()

        # Check who is the current player 
        if current_player == agent1.symbol:
            a = agent1
        else:
            a = agent2
        # If exploration mode is true, then perofrm random actions 
        # for agent to explore state-pair space
        # Updates Q-value during these actions
        if exploration is True and random.random() < exploration_probability:
            a.performRandomAction(updateQ=True)
        else:
            best_action = a.getBestAction()
            a.performAction(best_action, updateQ=(eval==False))

        # Reduce probability to explore during training
        if exploration_probability > 0.2:
            exploration_probability -= 1/iterations

        # Check if there is a winner
        winner = game.checkWinner() # Returns 0 if there is no winner
        if winner != 0:

            # Reset game and retrieve 
            nbr_games += 1
            game.resetGame()

            # Add to count for corresponding winner
            if winner == agent1.symbol:
                nbr_wins_agent1 += 1
            else:
                nbr_wins_agent2 += 1
        
        # Swap player
        if current_player == player1_symbol:
            current_player = player2_symbol
        else:
            current_player = player1_symbol

        
        
    print(nbr_wins_agent1, nbr_wins_agent2, nbr_games)    
    print("Win percentage: Agent 1 {:.2%}, Agent 2 {:.2%}.".format(nbr_wins_agent1/nbr_games, nbr_wins_agent2/nbr_games))

    if save_agent1 is not None:
        print("Saved trainer of agent 1 to {}".format(save_agent1))
        agent1.saveTrainer(save_agent1)

    # Return agents
    return agent1, agent2


