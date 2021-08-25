from WorldObjects import *


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
		reward = -1
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
				reward = -0.1
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


	def GetState(self):
		agent0 = self.Agents["agent0"]
		agent1 = self.Agents["agent1"]

		state = ""
		if agent0.PosX < 10:
			state += "0"
		state += str(agent0.PosX)
		if agent0.PosY < 10:
			state += "0"
		state += str(agent1.PosY)
		if agent1.PosX < 10:
			state += "0"
		state += str(agent1.PosX)
		if agent1.PosY < 10:
			state += "0"
		state += str(agent0.PosY)
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


	def EvalAgents(self):
		agent0 = self.Agents["agent0"]
		agent1 = self.Agents["agent1"]

		self.Reset()
		step = 0
		done = False
		while step < 60 and not done:
			step += 1
			state = self.GetState()
			action0 = agent0.Act(state)
			action1 = agent1.Act(state)
			_, done = self.StepDecentralized(action0, action1)
			self.Render()
			input("This was the " + str(step) + " th step: (a0," + agent0.Actions[action0] + ") (a1," + agent1.Actions[action1] + "). Press any key to continue.")
		print("Total Steps: " + str(step))


	#two agents learn individually their actions
	def LearnDecentralized(self):
		agent0 = self.Agents["agent0"]
		agent1 = self.Agents["agent1"]

		for i in range(400):
			step = 0
			done = False
			self.Reset()

			while step < 750 and not done:
				step += 1
				prevState = self.GetState()
				action0 = agent0.ChooseActionEgreedy(prevState)
				action1 = agent1.ChooseActionEgreedy(prevState)
				reward, done = self.StepDecentralized(action0, action1)
				nextState = self.GetState()
				agent0.Learn(prevState, action0, nextState, reward)
				agent1.Learn(prevState, action1, nextState, reward)
			print("Episode: " + str(i) + " Steps: " + str(step))



	#one agent learns the actions of two agents together
	#def LearnCentralized(self):




