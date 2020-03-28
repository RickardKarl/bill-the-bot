
class Agent:
    """  Class that defines agent and its possible actions """


    def __init__(self, symbol, state):
        self.symbol = symbol
        self.current_state = state

        self.actions = self.current_state.getAvailablePos()
        self.action_history = []

        self.trainer = None

    def getPossibleActions(self):
        return self.actions
    
    def performAction(self, action, state = None):
        """ Make move from agent, updates the state and possible actions  """

        if state == None:
            state = self.current_state

        # Read action
        x = action[0]
        y = action[1]
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

    def getActionHash(action):
        return hash(str(action))

    def getNextStateHash(self, action, state = None):

        if state == None:
            state = self.current_state

        self.performAction(action, state=state)
        next_state_hash = state.getStateHash()
        next_actions_hash = []
        for a in self.actions:
            next_actions_hash.append(Agent.getActionHash(a))

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
        
    def updatePossibleActions(self):
        self.actions = self.current_state.getAvailablePos()

    def assignState(self, state):
        self.current_state = state
        self.updatePossibleActions()

    def assignTrainer(self, trainer):
        self.trainer = trainer

    def getBestMove(self):
        if self.trainer != None:
            
            # Get best action
            best_action = self.trainer.getBestMove(self.current_state, self.actions)

            return best_action

        else:
            raise ValueError("No trainer assigned yet")





    
