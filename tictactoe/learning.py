import numpy as np

class Trainer:

    def __init__(self, agent, learning_parameter = 0.95, discount_factor = 0.9, Q = {}):
        """
            agent (Agent)
            learning_parameter (float)
            discount_factor (float)
            Q (dict)
        """

        self.agent = agent
        self.learning_parameter = learning_parameter
        self.discount_factor = discount_factor
        self.Q = Q

    def getStatePairKey(state_hash, action_hash):
        """ Returns state-pair hash key, requires separate state and action hash keys first """
        return state_hash*action_hash

    def getValueQ(self, state_hash, action_hash):
        """ Get expected reward given an action in a given state,
            returns 0 if the state-action pair has not been seen before.
            Input is state and action hash key                          """

        state_action_key = Trainer.getStatePairKey(state_hash, action_hash)
        if state_action_key in self.Q:
            return self.Q.get(state_action_key)
        else:
            self.Q[state_action_key] = 0
            return 0

    def setValueQ(self, state_hash, action_hash, value):
        """ Set value in Q """
        state_action_key = Trainer.getStatePairKey(state_hash, action_hash)

        self.Q[state_action_key] = value

    def getMaxQ(self, state_hash, list_action_hash):
        """ Returns the maximum Q value given a state and list of actions (input is hash keys) """
        maxQ = 0
        for a_hash in list_action_hash:
            tmpQ = self.getValueQ(state_hash, a_hash) 
            if maxQ < tmpQ:
                maxQ = tmpQ
        return maxQ

    def getBestAction(self, state_hash, list_action_hash, list_actions):
        """ Get best action given a set of possible actions in a given state """

        # Pick a random action at first
        random_idx = np.random.choice(list_actions.shape[0])
        best_action = list_actions[random_idx]
        
        # Find action that given largest Q in given state
        maxQ = 0
        for a_hash, action in zip(list_action_hash, list_actions):
            tmpQ = self.getValueQ(state_hash, a_hash)
            if maxQ < tmpQ:
                maxQ = tmpQ
                best_action = action

        return best_action
        

    def updateQ(self, state, action):
        """ Implements Q-learning iterative algorithm """


        state_hash = state.getStateHash()
        action_hash = self.agent.getActionHash(action)

        # Get current Q Value
        currentQ = self.getValueQ(state_hash, action_hash)

        # Find max Q value given the possible set of actions in the next state
        next_state, next_actions = self.agent.getActionHashFromState(action=action, state=state)
        max_nextQ = self.getMaxQ(next_state, next_actions) 
        
        # Update new Q
        newQ =  (1-self.learning_parameter)*currentQ
        newQ += self.learning_parameter*(self.agent.rewardFunction(state, action) + self.discount_factor*max_nextQ)

        self.setValueQ(state_hash, action_hash, newQ)