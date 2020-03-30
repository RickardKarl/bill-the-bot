from tictactoe.learning import Trainer

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

    def getActionHashFromState(self, action, state = None):
        """ Get hash key of actions in a given state, also returns the hash key of that state """
        if state == None:
            state = self.current_state

        self.performAction(action, state=state)
        next_state_hash = state.getStateHash()
        next_actions_hash = []
        for a in self.actions:
            next_actions_hash.append(self.getActionHash(a))

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

    def getBestMove(self):
        """ Get best move from the Trainer that has the largest expected reward """

        # Get hash key for state and actions
        state_hash, actions_hash = self.getActionHashFromState(selr.current_state, self.actions)

        # Return best move (if all are equally good, then it picks one at random)
        return self.trainer.getBestAction(state_hash, actions_hash, self.actions)

    
