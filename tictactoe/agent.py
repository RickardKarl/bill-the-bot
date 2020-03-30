from tictactoe.learning import Trainer

import numpy as np

class Agent:
    """  Class that defines agent and its possible actions """


    def __init__(self, symbol, state):
        self.symbol = symbol
        self.current_state = state

        self.actions = self.current_state.getAvailablePos()
        self.action_history = []

        self.trainer = Trainer(self)

    def getPossibleActions(self):
        """ Get possible actions """
        self.updatePossibleActions()
        return self.actions

    def updatePossibleActions(self):
        """ Update possible actions """
        self.actions = self.current_state.getAvailablePos()
    
    def performAction(self, action, state = None, updateQ = False):
        """ Make move from agent, updates the state and possible actions.
            Also updates Q at the same time.                        """

        assert action.shape == (2,), "Wrong shape " + str(action)

        if state == None:
            state = self.current_state

        # Read action
        x = action[0]
        y = action[1]

        # Update Q as part of Q-learning in the Trainer class
        if updateQ is True:
            self.trainer.updateQ(state, action)

        # Make move
        state.setPosition(x, y, self.symbol)
        self.action_history.append(action)

        # Update possible actions
        self.updatePossibleActions()
    
    def performRandomAction(self, updateQ=True):
        """ Perform random actions, important for exploration of state-pairs """
        
        self.updatePossibleActions()
        random_idx = np.random.choice(self.actions.shape[0])
        action = self.actions[random_idx]

        self.performAction(action, updateQ=updateQ)

    def revertLastAction(self, state = None):
        """ Make move from agent, updates the state and possible actions  """

        if state == None:
            state = self.current_state

        # Get last action
        last_action = self.action_history.pop()
        x = last_action[0]
        y = last_action[1]
        
        # Set to zero
        state.setPosition(x, y, 0) 

        # Update possible actions
        self.updatePossibleActions()

    def getActionHash(self, action):
        """ Get hash key of action """
        return hash(str(action))

    def getActionHashFromState(self, action = None, state = None):
        """ Get hash key of actions in a given state, also returns the hash key of that state """

        if state is None:
            state = self.current_state

        if not action is None:
            self.performAction(action, state=state)

        next_state_hash = state.getStateHash()
        next_actions_hash = []
        for a in self.actions:
            next_actions_hash.append(self.getActionHash(a))

        if not action is None:
            self.revertLastAction(state=state)

        return next_state_hash, next_actions_hash

    def rewardFunction(self, state, action):
        """ Returns positive value actions turns into win, else zero """

        # Perform action
        self.performAction(action, state=state)

        # Check winner
        if state.checkWinner() == self.symbol:
            reward = 100
        else:
            reward = -1

        # Revert action
        self.revertLastAction(state=state)

        return reward

    def assignState(self, state):
        """ Assign a state (Board) to the agent"""
        self.current_state = state
        self.updatePossibleActions()

    def getBestAction(self):
        """ Get best move from the Trainer that has the largest expected reward """

        self.updatePossibleActions()

        # Get hash key for state and actions
        state_hash, actions_hash = self.getActionHashFromState()

        # Return best move (if all are equally good, then it picks one at random)
        return self.trainer.getBestAction(state_hash, actions_hash, self.actions)
    
