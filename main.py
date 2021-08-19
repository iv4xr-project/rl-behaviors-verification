from GridWorld import *
from random import random, choice, randrange

class RLAgent(WorldObject):
	def __init__(self, name, actions, stepSize, discount, epsilon, planningStep):
		WorldObject.__init__(self, name)
		self.StepSize = stepSize
		self.Discount = discount
		self.Epsilon = epsilon
		self.PlanningStep = planningStep
		self.Model = {}
		self.QTable = {}
		self.Actions = {}
		for i in range(len(actions)):
			self.Actions[i] = actions[i]


	def Reset(self):
		self.PosX = self.InitialPosX
		self.PosY = self.InitialPosY


	def SetInitialPosition(self, x, y):
		self.InitialPosX = x
		self.InitialPosY = y


	#it assumes each coordinate of the position is below 99
	def GetState(self, env):
		state = ""
		if self.PosX < 10:
			state += "0"
		state += str(self.PosX)
		if self.PosY < 10:
			state += "0"
		state += str(self.PosY)
		for b in env.DoorButtons.values():
			if b.WasPressed:
				state += "1"
			else:
				state += "0"
		for b in env.GoalButtons.values():
			if b.WasPressed:
				state += "1"
			else:
				state += "0"
		return state


	def Act(self, state):
		rewards = self.Model[state]
		top = float("-inf")
		bestActions = []

		for a in rewards.keys():
			if rewards[a] > top:
				top = rewards[a]
				bestActions = []
			elif rewards[a] == top:
				bestActions.append(i)

		return choice(bestActions)


	def UpdateModel(self, prevState, action, reward):
		if not prevState in self.Model:
			self.Model[prevState] = {}
		self.Model[prevState][action] = reward #will I do this regadless of having done already?


	def UpdateQTable(self, prevState, action, nextState, reward):
		if not prevState in self.QTable:
			self.QTable[prevState] = []
			for a in self.Actions:
				self.QTable[prevState].append(0)


		nextBestAction = self.ChooseCurrentBestAction(nextState)
		nextBestQvalue = self.QTable[nextState][nextBestAction]
		self.QTable[prevState][action] += self.StepSize * (reward + self.Discount * nextBestQvalue - self.QTable[prevState][action])


	def ChooseCurrentBestAction(self, state):
		if not state in self.QTable:
			self.QTable[state] = []
			for a in self.Actions.keys():
				self.QTable[state].append(0)
		qValues = self.QTable[state]
		top = float("-inf")
		ties = []

		for i in range(len(qValues)):
			if qValues[i] > top:
				top = qValues[i]
				ties = [i]
			elif qValues[i] == top:
				ties.append(i)

		if ties == []:
			print(state)
			print(qValues)
		return choice(ties)


	def ChooseActionEgreedy(self, state):
		if random() < self.Epsilon:
			return randrange(len(self.Actions.keys()))
		else:
			return self.ChooseCurrentBestAction(state)


	#using dynaQ
	def Learn(self, env):
		env.Reset()
		#env.Render()
		done = False
		i = 0
		while i < 1000 and not done:
			i += 1
			prevState = self.GetState(env)
			action = self.ChooseActionEgreedy(prevState)
			#print("ACTION: " + self.Actions[action])
			reward, done = env.Step(self.Name, action)
			nextState = self.GetState(env)
			self.UpdateQTable(prevState, action, nextState, reward)
			self.UpdateModel(prevState, action, reward)
			#TODO add planning part of dynaQ
			#env.Render()




if __name__ == "__main__":
	agent = RLAgent("agent0", ["UP", "DOWN", "LEFT", "RIGHT", "PRESS", "NOTHING"], 0.1, 0.95, 0.1, 10)
	env = CreateGridWorld("scenarios/scenario1.txt", agent)
	#agent.SetInitialPosition(gridWorld.Agents["agent0"].InitialPosX, gridWorld.Agents["agent0"].InitialPosY)

	agent.Learn(env)










