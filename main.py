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
		return self.ChooseCurrentBestAction(state)


	def Eval(self, env):
		env.Reset()
		step = 0
		done = False
		while step < 60 and not done:
			step += 1
			state = self.GetState(env)
			action = self.Act(state)
			_, done = env.Step(self.Name, action)
			env.Render()
		print("Total Steps: " + str(step))



	def UpdateModel(self, prevState, action, nextState, reward):
		if not prevState in self.Model:
			self.Model[prevState] = {}
		self.Model[prevState][action] = (nextState, reward) #will I do this regadless of having done already?


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
		return choice(ties)


	def ChooseActionEgreedy(self, state):
		if random() < self.Epsilon:
			return randrange(len(self.Actions.keys()))
		else:
			return self.ChooseCurrentBestAction(state)


	#using dynaQ
	def Learn(self, env):
		for i in range(300):
			step = 0
			done = False
			env.Reset()

			while step < 1000 and not done:
				step += 1
				prevState = self.GetState(env)
				action = self.ChooseActionEgreedy(prevState)
				#if self.PosX == 5 and self.PosY == 4:
				#	print("ACTION: " + self.Actions[action])
				reward, done = env.Step(self.Name, action)
				nextState = self.GetState(env)
				self.UpdateQTable(prevState, action, nextState, reward)
				self.UpdateModel(prevState, action, nextState, reward)

				for j in range(self.PlanningStep):
					randomState = choice(list(self.Model.keys()))
					randomAction = choice(list(self.Model[randomState].keys()))
					predictedState, predictedReward = self.Model[randomState][randomAction]
					self.UpdateQTable(randomState, randomAction, predictedState, predictedReward)
			print("Episode: " + str(i) + " Steps: " + str(step))




if __name__ == "__main__":
	agent = RLAgent("agent0", ["UP", "DOWN", "LEFT", "RIGHT", "PRESS", "NOTHING"], 0.1, 0.95, 0.1, 10)
	env = CreateGridWorld("scenarios/scenario1.txt", agent)
	agent.Learn(env)
	agent.Eval(env)










