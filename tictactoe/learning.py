from tictactoe.agent import Agent

class Trainer:

    def __init__(self, agent, learning_parameter = 0.9, discount_factor = 0.95):
        self.agent = agent
        self.learning_parameter = learning_parameter
        self.discount_factor = discount_factor

        self.Q = {}


    def getStatePairKey(state_hash, action_hash):
        return hash(str(state_hash)+str(action_hash))
    

    def getValueQ(self, state_hash, action_hash):

        state_action_key = Trainer.getStatePairKey(state_hash, action_hash)

        if state_action_key in self.Q:
            return self.Q.get(state_action_key)
        else:
            self.Q[state_action_key] = 0
            return 0
    

    def setValueQ(self, state_hash, action_hash, value):

        state_action_key = Trainer.getStatePairKey(state_hash, action_hash)

        self.Q[state_action_key] = value

    def getMaxQ(self, state_hash, list_of_action_hashes):
        maxQ = 0
        for a in list_of_action_hashes:
            tmpQ = self.getValueQ(state_hash, a) 
            if maxQ < tmpQ:
                maxQ = tmpQ
        return maxQ

    def getBestMove(self, state, list_of_actions):

        # Get hash of possible actions
        actions_hash = []
        for a in list_of_actions:
            actions_hash.append(Agent.getActionHash(a))

        # Get current state hash
        state_hash = state.getStateHash()
            
        best_action = list_of_actions[0]
        maxQ = 0
        for a_hash, action in zip(actions_hash, list_of_actions):
            tmpQ = self.getValueQ(state_hash, a_hash) 
            if maxQ < tmpQ:
                maxQ = tmpQ
                best_action = action

        return best_action


    def updateQ(self, state, action):
        """ Implements Q-learning iterative algorithm """

        state_hash = state.getStateHash()
        action_hash = Agent.getActionHash(action)

        # Get current Q Value
        currentQ = self.getValueQ(state_hash, action_hash)

        # Find max Q value given the possible set of actions in the next state
        next_state, next_actions = self.agent.getNextStateHash(action, state=state)
        max_nextQ = self.getMaxQ(next_state, next_actions) 
        
        # Update new Q
        newQ =  (1-self.learning_parameter)*currentQ
        newQ += self.learning_parameter*(self.agent.rewardFunction(state, action) + self.discount_factor*max_nextQ)

        self.setValueQ(state_hash, action_hash, newQ)