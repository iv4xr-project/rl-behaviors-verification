from GridWorld import *
from random import random, choice, randrange

class RLAgent():
	def __init__(self, numStates, actions, gamma, stepSize, epsilon, planningStep):
		self.Gamma = gamma
		self.StepSize = stepSize
		self.Epsilon = epsilon
		self.PlanningStep = planningStep
		self.PastAction = -1
		self.PastState = -1
		self.Model = {}

		self.Actions = {}
		for i in range(len(actions)):
			self.Actions[i] = actions[i]

		self.QTable = []
		for st in range(numStates):
			line = []
			for a in range(len(actions)):
				line.append(0)
			self.QTable.append(line)


	def UpdateModel(self, prevState, action, newState, reward):
		if not prevState in self.Model:
			self.Model[prevState] = {}
		if not action in self.Model[prevState]:
			self.Model[prevState][action] = {}
		self.Model[prevState][action] = (newState, reward)


	def ChooseActionEgreedy(self, state):
		if random() < self.Epsilon:
			return randrange(len(self.Actions.keys()))
		else:
			qValues = self.QTable[state]
			top = float("-inf")
			ties = []

			for i in range(len(qValues)):
				if qValues[i] > top:
					top = qValues[i]
					ties = []
				elif qValues[i] == top:
					ties.append(i)

    		return choice(ties)

#def runDynaQ(self, gridWorld, agent):



if __name__ == "__main__":
	gridWorld = CreateGridWorld("scenarios/scenario1.txt")
	gridWorld.Reset()

	agent = RLAgent(4, ["UP", "DOWN", "LEFT", "RIGHT", "PRESS", "NOTHING"], 0.95, 0.1, 0.1, 10)
	action = agent.ChooseActionEgreedy(0)
	print agent.Actions[action]


