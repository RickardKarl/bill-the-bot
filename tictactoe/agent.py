
class Agent:
    """  Class that defines agent and its possible actions """


    def __init__(self, symbol, state, horizon = 10):
        self.symbol = symbol
        self.current_state = state
        self.horizon = horizon

        self.actions = self.current_state.getAvailablePos()


    def makeMove(self, action):
        """ Make move from agent, updates the state and possible actions  """
        x = action[0]
        y = action[1]
        self.current_state.setPosition(x, y, self.symbol)
        self.actions = self.current_state.getAvailablePos()

        
    def rewardFunction(self, state, action):
        



         




    
