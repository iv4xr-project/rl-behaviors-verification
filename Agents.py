from WorldObjects import *
from random import random, choice, randrange


class Agent(WorldObject):
	def __init__(self, name, x, y):
		WorldObject.__init__(self, name)
		self.InitialPosX = x
		self.InitialPosY = y

	def Reset(self):
		self.SetPos(self.InitialPosX, self.InitialPosY)


class SingleAgent(WorldObject):
	def __init__(self, name, actions, stepSize, discount, epsilonMax, epsilonMin, planningStep):
		WorldObject.__init__(self, name)
		self.StepSize = stepSize
		self.Discount = discount
		self.EpsilonMax = epsilonMax
		self.Epsilon = epsilonMax
		self.EpsilonMin = epsilonMin
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


	def UpdateEpsilon(self, currentEpisode, maxEpisodes):
		self.Epsilon = max(self.EpsilonMax - ((self.EpsilonMax - self.EpsilonMin) * currentEpisode / (0.4 * maxEpisodes)), self.EpsilonMin)


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
			_, done = env.StepSingleAgent(self.Name, action)
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


	def Learn(self, prevState, action, nextState, reward):
		self.UpdateQTable(prevState, action, nextState, reward)
		self.UpdateModel(prevState, action, nextState, reward)

		for j in range(self.PlanningStep):
			randomState = choice(list(self.Model.keys()))
			randomAction = choice(list(self.Model[randomState].keys()))
			predictedState, predictedReward = self.Model[randomState][randomAction]
			self.UpdateQTable(randomState, randomAction, predictedState, predictedReward)
			

	#using dynaQ
	def LearnDynaQ(self, env, episodes, maxSteps):
		for i in range(episodes):
			step = 0
			done = False
			env.RandomReset()

			while step < maxSteps and not done:
				step += 1
				prevState = env.GetStatePartialObservability(self)
				action = self.ChooseActionEgreedy(prevState)
				self.UpdateEpsilon(i, episodes)
				reward, done = env.StepSingleAgent(self.Name, action)
				nextState = env.GetStatePartialObservability(self)
				self.Learn(prevState, action, nextState, reward)
			print("Episode: " + str(i) + " Steps: " + str(step) + " Epsilon: " + str(self.Epsilon))







class DoubleAgent(SingleAgent):
	def __init__(self, name0, name1, actions, stepSize, discount, epsilonMax, epsilonMin, planningStep):
		super().__init__("centralized", actions, stepSize, discount, epsilonMax, epsilonMin, planningStep)
		super().SetInitialPosition(-1, -1)
		self.Name0 = name0
		self.Name1 = name1


	def Reset(self):
		self.PosX0 = self.InitialPosX0
		self.PosY0 = self.InitialPosY0
		self.PosX1 = self.InitialPosX1
		self.PosY1 = self.InitialPosY1


	def SetInitialPosition(self, x, y):
		print("ERROR: This method should not be called for an instance of DoubleAgent")


	def SetInitialPosition0(self, x0, y0):
		self.InitialPosX0 = x0
		self.InitialPosY0 = y0


	def SetInitialPosition1(self, x1, y1):
		self.InitialPosX1 = x1
		self.InitialPosY1 = y1