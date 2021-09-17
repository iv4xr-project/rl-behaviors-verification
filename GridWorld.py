from WorldObjects import *
from Agents import *
import os


class GridWorld:
	def __init__(self, grid, agents, doors, doorButtons, goalButtons):
		self.Grid = grid #array of arrays
		self.Agents = agents #dictionary
		self.Doors = doors #dictionary
		self.DoorButtons = doorButtons #dictionary
		self.GoalButtons = goalButtons #dictionary


	#return True only if there is door in position (x,y) and the door is not open
	def IsLockedDoor(self, x, y):
		for d in self.Doors.values():
			if d.PosX == x and d.PosY == y and d.IsOpen == False:
				return True
		return False


	def GetUnpressedDoorButton(self, x, y):
		for b in self.DoorButtons.values():
			if b.PosX == x and b.PosY == y and b.WasPressed == False:
				return b
		return None
	

	def GetUnpressedGoalButton(self, x, y):
		for b in self.GoalButtons.values():
			if b.PosX == x and b.PosY == y and b.WasPressed == False:
				return b
		return None


	def Reset(self):
		for agent in self.Agents.values():
			agent.Reset()
		for door in self.Doors.values():
			door.Reset()
		for doorButton in self.DoorButtons.values():
			doorButton.Reset()
		for goalButton in self.GoalButtons.values():
			goalButton.Reset()


	def CheckGoal(self):
		for b in self.GoalButtons.values():
			if not b.WasPressed:
				return False
		return True


	def StepSingleAgent(self, agentName, action):
		a = self.Agents[agentName]
		newX = a.PosX
		newY = a.PosY
		reward = -1
		done = self.CheckGoal()

		if action == 5: #NOTHING
			reward = -0.5
		if action == 4: #PRESS
			b = self.GetUnpressedDoorButton(newX, newY)
			if b != None:
				b.Press()
			else:
				b = self.GetUnpressedGoalButton(newX, newY)
				if b != None:
					b.Press()
		else: #moving actions
			if action == 0: #UP
				newX -= 1
			elif action == 1: #DOWN
				newX += 1
			elif action == 2:	#LEFT
				newY -= 1
			elif action == 3: #RIGHT
				newY += 1

			if self.Grid[newX][newY] != "w" and not self.IsLockedDoor(newX, newY):
				a.PosX = newX
				a.PosY = newY
		
		if done:
			reward = 100
		return reward, done


	def StepDecentralized(self, action0, action1):
		reward0 = -1
		reward1 = -1
		done = self.CheckGoal()

		for i in range(2):
			action = action0
			a = self.Agents["agent0"]
			if i == 1:
				action = action1
				a = self.Agents["agent1"]
			newX = a.PosX
			newY = a.PosY

			if action == 5: #NOTHING
				if i == 0:
					reward0 = 0
				elif i == 1:
					reward1 = 0
			if action == 4: #PRESS
				b = self.GetUnpressedDoorButton(newX, newY)
				if b != None:
					b.Press()
					#reward = 100
				else:
					b = self.GetUnpressedGoalButton(newX, newY)
					if b != None:
						#reward = 100
						b.Press()
			else: #moving actions
				if action == 0: #UP
					newX -= 1
				elif action == 1: #DOWN
					newX += 1
				elif action == 2:	#LEFT
					newY -= 1
				elif action == 3: #RIGHT
					newY += 1

				if self.Grid[newX][newY] != "w" and not self.IsLockedDoor(newX, newY):
					a.PosX = newX
					a.PosY = newY
		
		if done:
			reward0 = 100
			reward1 = 100
		return reward0, reward1, done


	def StepCentralized(self, actions):
		reward = -1
		done = self.CheckGoal()

		agents = self.Agents["centralized"]
		action0 = agents.Actions[actions].split("-")[0]
		action1 = agents.Actions[actions].split("-")[1]
		action = action0
		newX = agents.PosX0
		newY = agents.PosY0
		for i in range(2):
			if i == 1:
				action = action1
				newX = agents.PosX1
				newY = agents.PosY1

			if action == "NOTHING":
				reward = 0
			if action == "PRESS":
				b = self.GetUnpressedDoorButton(newX, newY)
				if b != None:
					b.Press()
				else:
					b = self.GetUnpressedGoalButton(newX, newY)
					if b != None:
						b.Press()
			else: #moving actions
				if action == "UP":
					newX -= 1
				elif action == "DOWN":
					newX += 1
				elif action == "LEFT":
					newY -= 1
				elif action == "RIGHT":
					newY += 1

				if self.Grid[newX][newY] != "w" and not self.IsLockedDoor(newX, newY):
					if i == 0:
						agents.PosX0 = newX
						agents.PosY0 = newY
					elif i == 1:
						agents.PosX1 = newX
						agents.PosY1 = newY
		
		if done:
			reward = 100
		return reward, done


	def Render(self):
		grid = []
		for i in self.Grid:
			grid.append(i.copy())

		for b in self.DoorButtons.values():
			x = b.PosX
			y = b.PosY
			if b.WasPressed:
				grid[x][y] = "B" + b.Name[-1]
			else:
				grid[x][y] = "b" + b.Name[-1]
		for b in self.GoalButtons.values():
			x = b.PosX
			y = b.PosY
			if b.WasPressed:
				grid[x][y] = "B" + b.Name[-1]
			else:
				grid[x][y] = "b" + b.Name[-1]
		for d in self.Doors.values():
			x = d.PosX
			y = d.PosY
			if d.IsOpen:
				grid[x][y] = "D" + d.Name[-1]
			else:
				grid[x][y] = "d" + d.Name[-1]
		for a in self.Agents.values():
			if isinstance(a, DoubleAgent):
				x = a.PosX0
				y = a.PosY0
				grid[x][y] = "a" + a.Name0[-1]
				x = a.PosX1
				y = a.PosY1
				grid[x][y] = "a" + a.Name1[-1]
			else:
				x = a.PosX
				y = a.PosY
				grid[x][y] = "a" + a.Name[-1]

		for row in grid:
			printableRow = ""
			for i in range(len(row)):
				if row[i] == "f":
					printableRow += "  "
				elif row[i] == "w":
					printableRow += ".."
				else:
					printableRow += row[i]
			print(printableRow)


	def GetStatePartialObservability(self, agent):
		state = ""
		if agent.PosX < 10:
			state += "0"
		state += str(agent.PosX)
		if agent.PosY < 10:
			state += "0"
		state += str(agent.PosY)
		for b in self.DoorButtons.values():
			if b.WasPressed:
				state += "1"
			else:
				state += "0"
		for b in self.GoalButtons.values():
			if b.WasPressed:
				state += "1"
			else:
				state += "0"
		return state


	def GetStateFullObservability(self):
		agents = self.Agents["centralized"]

		state = ""
		if agents.PosX0 < 10:
			state += "0"
		state += str(agents.PosX0)
		if agents.PosY0 < 10:
			state += "0"
		state += str(agents.PosY0)
		if agents.PosX1 < 10:
			state += "0"
		state += str(agents.PosX1)
		if agents.PosY1 < 10:
			state += "0"
		state += str(agents.PosY1)
		for b in self.DoorButtons.values():
			if b.WasPressed:
				state += "1"
			else:
				state += "0"
		for b in self.GoalButtons.values():
			if b.WasPressed:
				state += "1"
			else:
				state += "0"
		return state


	def EvalAgentsDecentralized(self):
		agent0 = self.Agents["agent0"]
		agent1 = self.Agents["agent1"]

		self.Reset()
		step = 0
		done = False
		while step < 60 and not done:
			step += 1
			state0 = self.GetStatePartialObservability(agent0)
			state1 = self.GetStatePartialObservability(agent1)
			action0 = agent0.Act(state0)
			action1 = agent1.Act(state1)
			_, _,done = self.StepDecentralized(action0, action1)
			self.Render()
			input("This was the " + str(step) + " th step: (a0," + agent0.Actions[action0] + ") (a1," + agent1.Actions[action1] + "). Press any key to continue.")
		print("Total Steps: " + str(step))


	def EvalAgentsCentralized(self):
		agents = self.Agents["centralized"]

		self.Reset()
		step = 0
		done = False
		while step < 60 and not done:
			step += 1
			state = self.GetStateFullObservability()
			actions = agents.Act(state)
			_, done = self.StepCentralized(actions)
			self.Render()
			input("This was the " + str(step) + " th step: action0-action1 were " + agents.Actions[actions] + ". Press any key to continue.")
		print("Total Steps: " + str(step))



	#two agents learn individually their actions
	def LearnDecentralized(self, episodes, maxSteps):
		agent0 = self.Agents["agent0"]
		agent1 = self.Agents["agent1"]

		for i in range(episodes):
			step = 0
			done = False
			self.Reset()

			while step < maxSteps and not done:
				step += 1
				prevState0 = self.GetStatePartialObservability(agent0)
				prevState1 = self.GetStatePartialObservability(agent1)
				action0 = agent0.ChooseActionEgreedy(prevState0)
				action1 = agent1.ChooseActionEgreedy(prevState1)
				agent0.UpdateEpsilon(i, episodes)
				agent1.UpdateEpsilon(i, episodes)
				reward0, reward1, done = self.StepDecentralized(action0, action1)
				nextState0 = self.GetStatePartialObservability(agent0)
				nextState1 = self.GetStatePartialObservability(agent1)
				agent0.Learn(prevState0, action0, nextState0, reward0)
				agent1.Learn(prevState1, action1, nextState1, reward1)
			print("Episode: " + str(i) + " Steps: " + str(step) + " Epsilon: " + str(agent0.Epsilon))



	#one agent learns the actions of two agents together
	def LearnCentralized(self, episodes, maxSteps):
		agents = self.Agents["centralized"]

		for i in range(episodes):
			step = 0
			done = False
			self.Reset()

			while step < maxSteps and not done:
				step += 1
				prevState = self.GetStateFullObservability()
				actions = agents.ChooseActionEgreedy(prevState)
				agents.UpdateEpsilon(i, episodes)
				reward, done = self.StepCentralized(actions)
				nextState = self.GetStateFullObservability()
				agents.Learn(prevState, actions, nextState, reward)
				#self.Render()
			print("Episode: " + str(i) + " Steps: " + str(step) + " Epsilon: " + str(agents.Epsilon))


	def WriteAgentsQtableToFile(self, mode, scenario):
		directory = "policies"
		if not os.path.exists(directory):
			os.makedirs(directory)
		
		if mode == "centralized":
			filename = directory + "/qvalues-centralized-s" + scenario + ".txt"
			file = open(filename, "w")
			for agent in self.Agents.values():
				states = []
				file.write(agent.Name + "\n")
				file.write("actions")
				for action in agent.Actions.values():
					file.write(" " + action)
				for state in agent.QTable.keys():
					file.write("\n" + state)
					for qvalue in agent.QTable[state]:
						file.write(" " + str(qvalue))
				file.write("\n---\n")
			file.close()
		elif mode == "decentralized":
			filename = directory + "/qvalues-decentralized-s" + scenario + ".txt"
			file = open(filename, "w")
			for agent in self.Agents.values():
				states = []
				file.write(agent.Name + "\n")
				file.write("actions")
				for action in agent.Actions.values():
					file.write(" " + action)
				for state in agent.QTable.keys():
					file.write("\n" + state)
					for qvalue in agent.QTable[state]:
						file.write(" " + str(qvalue))
				file.write("\n---\n")
			file.close()
		elif mode == "singleagents":
			filename = directory + "/qvalues-singleagents-s" + scenario + ".txt"
			file = open(filename, "w")
			for agent in self.Agents.values():
				states = []
				file.write(agent.Name + "\n")
				file.write("actions")
				for action in agent.Actions.values():
					file.write(" " + action)
				for state in agent.QTable.keys():
					file.write("\n" + state)
					for qvalue in agent.QTable[state]:
						file.write(" " + str(qvalue))
				file.write("\n---\n")
			file.close()


	def LoadAgentsQtableFromFile(self, mode, scenario):
		if mode == "centralized":
			filename = "policies/qvalues-centralized-s" + scenario + ".txt"
		elif mode == "decentralized":
			filename = "policies/qvalues-decentralized-s" + scenario + ".txt"
		elif mode == "singleagents":
			filename = "policies/qvalues-singleagents-s" + scenario + ".txt"
		
		try:
			file = open(filename, "r")
			agentName = ""
			readingQvalues = False
			for line in file:
				if agentName == "":
					agentName = line[:-1]
				elif line.startswith("actions"):
					readingQvalues = True
				elif line.startswith("---"):
					readingQvalues = False
					agentName = ""
				elif readingQvalues:
					splittedLine = line[:-1].split(" ")
					state = ""
					qValues = []
					for val in splittedLine:
						if state == "":
							state = val
						else:
							qValues.append(float(val))
					if not agentName in self.Agents:
						print("Agent name not found: " + agentName)
					self.Agents[agentName].QTable[state] = qValues.copy()
			file.close()
		except OSError as err:
			print("File not found: policies/qvalues-decentralized-s" + scenario + ".txt " + err)



