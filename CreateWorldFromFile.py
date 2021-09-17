from GridWorld import *
from Agents import *


def CreateGridWorld(filename, a0, a1):
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
					if isinstance(a0, DoubleAgent):
						if agentName == a0.Name0:
							agents["centralized"] = a0
							a0.SetInitialPosition0(rowNum, colNum)
						elif agentName == a0.Name1:
							agents["centralized"] = a0
							a0.SetInitialPosition1(rowNum, colNum)
						else:
							agent = Agent(agentName, rowNum, colNum)
							agents[agentName] = agent
					else:
						if agentName == a0.Name:
							agents[agentName] = a0
							a0.SetInitialPosition(rowNum, colNum)
						elif agentName == a1.Name:
							agents[agentName] = a1
							a1.SetInitialPosition(rowNum, colNum)
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