
from tictactoe.agent import Agent
from tictactoe.board import Board
from tictactoe.learning import Trainer

import numpy as np
from tqdm import tqdm

player1_symbol = 1
player2_symbol = -1 

def simulate(iterations = 1000, agent1 = None, agent2 = None, use_trainer1 = False):

    game = Board()

    if agent1 == None:
        agent1 = Agent(player1_symbol, game)
        trainer1 = Trainer(agent1)
    else:
        agent1.assignState(game)
        trainer1 = agent1.trainer
    
    if agent2 == None:
        agent2 = Agent(player2_symbol, game)
        trainer2 = Trainer(agent2)
    else:
        agent2.assignState(game)
        trainer2 = Trainer(agent2)

    nbr_wins_agent1 = 0
    nbr_wins_agent2 = 0
    nbr_games = 0

    current_player = player1_symbol

    for i in tqdm(range(iterations)):

        if game.checkGameEnded():
            nbr_games += 1
            game.resetGame()
            agent1.updatePossibleActions()
            agent2.updatePossibleActions()

        if current_player == agent1.symbol:
            a = agent1
            t = trainer1
        else:
            a = agent2
            t = trainer2

        

        if current_player == player1_symbol and use_trainer1:
            action = agent1.getBestMove()

        else:
            possible_actions = a.getPossibleActions()
            random_idx = np.random.choice(possible_actions.shape[0])
            action = possible_actions[random_idx]

        t.updateQ(game, action)
        a.performAction(action)

        winner = game.checkWinner()
        if winner != 0:
            nbr_games += 1
            game.resetGame()
            agent1.updatePossibleActions()
            agent2.updatePossibleActions()

            if winner == agent1.symbol:
                nbr_wins_agent1 += 1
            else:
                nbr_wins_agent2 += 1
        
        if current_player == player1_symbol:
            current_player = player2_symbol
        else:
            current_player = player1_symbol


    
    print("Win percentage: Agent 1 {:.2%}, Agent 2 {:.2%}.".format(nbr_wins_agent1/nbr_games, nbr_wins_agent2/nbr_games))
    
    agent1.assignTrainer(trainer1)
    agent2.assignTrainer(trainer2)

    return agent1, agent2


