class WorldObject():
	def __init__(self, name):
		self.Name = name

	def SetPos(self, x, y):
		self.PosX = x
		self.PosY = y


class Door(WorldObject):
	def __init__(self, name):
		WorldObject.__init__(self, name)
		self.IsOpen = False

	def Reset(self):
		self.IsOpen = False


class GoalButton(WorldObject):
	def __init__(self, name):
		WorldObject.__init__(self, name)
		self.WasPressed = False

	def Reset(self):
		self.WasPressed = False

	def Press(self):
		self.WasPressed = True


class DoorButton(GoalButton):
	def __init__(self, name, door):
		WorldObject.__init__(self, name)
		self.Door = door

	def Reset(self):
		super().Reset()
		self.Door.IsOpen = False

	def Press(self):
		super().Press()
		self.Door.IsOpen = True


class Agent(WorldObject):
	def __init__(self, name, x, y):
		WorldObject.__init__(self, name)
		self.InitialPosX = x
		self.InitialPosY = y

	def Reset(self):
		self.SetPos(self.InitialPosX, self.InitialPosY)


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


	def Step(self, agentName, action):
		a = self.Agents[agentName]
		newX = a.PosX
		newY = a.PosY
		reward = -1
		done = self.CheckGoal()

		#if action == 5: #NOTHING
			#reward = 0
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


def CreateGridWorld(filename, a0):
	file = open(filename)
	lines = file.readlines()
	startReadingGrid = False
	doorButtons = {}
	goalButtons = {}
	doors = {}
	agents = {}
	grid =[]

	rowNum = 0
	colNum = 0
	for line in lines:
		if line[-1] == "\n":
			line = line[:-1] #remote \n
		cells = line.split(",")

		if not startReadingGrid and line[0] == "|":
			startReadingGrid = True
			cells[0] = cells[0][1:] #remote |
		
		if startReadingGrid:
			row = []
			for cell in cells:
				if cell.startswith("w"):
					row.append("w")
				elif cell.startswith("f"):
					row.append("f")
				else:
					print("Unknown cell: " + str(rowNum) + " " + str(colNum))

				if "cb" in cell:
					buttonName = cell[cell.index("button"):]
					goalButtons[buttonName].SetPos(rowNum, colNum)
				elif "b" in cell:
					buttonName = cell[cell.index("button"):]
					doorButtons[buttonName].SetPos(rowNum, colNum)
				elif "d" in cell:
					doorName = cell[cell.index("door"):]
					doors[doorName].SetPos(rowNum, colNum)
				elif "a" in cell:
					agentName = cell[cell.index("agent"):]
					if agentName == a0.Name:
						agents[agentName] = a0
						a0.SetInitialPosition(rowNum, colNum)
					else:
						agent = Agent(agentName, rowNum, colNum)
						agents[agentName] = agent

				colNum += 1
			colNum = 0
			rowNum += 1
			grid.append(row)
		else:
			if cells[0] != "" and cells[1] != "":
				buttonName = cells[0]
				doorName = cells[1]
				door = Door(doorName)
				button = DoorButton(buttonName, door)
				doors[doorName] = door
				doorButtons[buttonName] = button
			elif cells[0] != "":
				buttonName = cells[0]
				button = GoalButton(buttonName)
				goalButtons[buttonName] = button
			else:
				print("Unknow init line: " + line)
	
	return GridWorld(grid, agents, doors, doorButtons, goalButtons)