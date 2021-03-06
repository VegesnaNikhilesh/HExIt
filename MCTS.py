import util
import numpy as np
from MCTS_Tree import MCTS_Tree, MCTS_Node
from State import State


class MCTS:
	#uct_new(s,a) = uct(s,a) + w_a * (apprentice_policy(s,a) / n(s,a) + 1)
	# given a list of batch_size state objects
	# return an array with batch_size elements.  Each element is a 26-list.  The state, followed by number of times we took action i
	#uct(s,a) = r(s,a)/n(s,a) + c_b * sqrt ( log(n(s)) / n(s,a) )
	
	#rollout begind at state s' we've never seen before. finish sim, add s' to tree. propagate signal up 
	def __init__(self, game_size=5, batch_size=256, simulations_per_state=1000, max_depth=6, apprentice=None):
		print ("initialized MCTS")
		self.game_size = game_size
		self.num_actions = game_size ** 2
		self.batch_size = batch_size
		self.simulations_per_state = simulations_per_state
		self.max_depth = max_depth
		self.apprentice = apprentice

	# This method generates a dataset of size SELF.BATCH_SIZE.
	# It is passed STARTING_STATES, which is a list of BATCH_SIZE states (as State instances).
	# For each starting state, runs SELF.SIMULATIONS_PER_STATE, each starting at that start state.
	# Calculates the number of times each action was taken from the root node (start state).
	# Returns three arrays, S, A1 and A2, each with BATCH_SIZE + 1 elements.
	# S is just a copy of STARTING_STATES.
	# The i-th element of A gives the distribution of actions from the i-th start state for Player 1.
	# The i-th element of A gives the distribution of actions from the i-th start state for Player 2.
	# If it is Player X's turn, then Player Y's distribution will be all 0's except for the last position is a 1.
	# This data is to be passed to the apprentice, that will be trained to mimic this distribution.
	def generateDataBatch(self, starting_states):

		action_distribution1 = np.zeros(shape=(self.batch_size, self.num_actions + 1))
		action_distribution2 = np.zeros(shape=(self.batch_size, self.num_actions + 1))

		for i, state in enumerate(starting_states):
			
			if state.playerOneTurn():
				action_distribution1 = self.runSimulations(state)
				action_distribution2[i][-1] = 1
			else:
				action_distribution2 = self.runSimulations(state)
				action_distribution1[i][-1] = 1

		return (starting_states, action_distribution1, action_distribution2)


	# Runs SIMULATIONS_PER_STATE simulations, each starting from the given START_STATE.
	# Returns a list with as many elements as there are actions, plus 1. (ex. 26 for a 5x5 hex game).
	# Each element is a probability (between 0 and 1).
	# The i-th element is the number of times we took the i-th action from the root state (as a probability).
	# The last element is the number of times we took no action (if it wasn't this player's turn.)
	def runSimulations(self, start_state):
		# breakpoints = list(np.random.randint(0, self.simulations_per_state, self.num_actions - 1))
		# breakpoints = [0] + breakpoints + [self.simulations_per_state]
		# breakpoints = sorted(breakpoints)
		# action_counts = [breakpoints[i + 1] - breakpoints[i] for i in range(self.num_actions)]
		# return action_counts

		# Initialize new tree
		self.tree = MCTS_Tree(start_state, self.num_actions, max_depth=self.max_depth, apprentice=self.apprentice)
		for t in range(self.simulations_per_state):
			self.tree.runSingleSimulation()

		return self.tree.getActionCounts() / self.simulations_per_state
				





def main():
	m = MCTS(batch_size=16, simulations_per_state=100)
	states = [State(x) for x in np.random.randint(0, 1000, 16)]
	data = m.generateDataBatch(states)


if __name__ == '__main__':
	main()