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

class GoalButton(WorldObject):
	def __init__(self, name):
		WorldObject.__init__(self, name)
		self.WasPressed = False

class DoorButton(GoalButton):
	def __init__(self, name, door):
		WorldObject.__init__(self, name)
		self.Door = door

class Agent(WorldObject):
	def __init__(self, name, x, y):
		WorldObject.__init__(self, name)
		self.InitialPosX = x
		self.InitialPosY = y

class GridWorld:
	def __init__(self, grid):
		self.grid = grid


def CreateGridWorld(filename):
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
					row.append("wa")
				elif cell.startswith("f"):
					row.append("fr")
				else:
					print "Unknown cell: " + str(rowNum) + " " + str(colNum)

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
				print "Unknow init line: " + line



if __name__ == "__main__":
    CreateGridWorld("scenarios/scenario1.txt")