from CreateWorldFromFile import *
from Agents import *
import sys


if __name__ == "__main__":
	if len(sys.argv) == 4 and sys.argv[1] == "-learn" and (sys.argv[2] == "-centralized" or sys.argv[2] == "-decentralized") and (sys.argv[3] == "-s1" or sys.argv[3] == "-s2" or sys.argv[3] == "-s3"):
		isCentralized = (sys.argv[2] == "-centralized")
		scenario = sys.argv[3][-1]

		agent0 = RLAgent("agent0", ["UP", "DOWN", "LEFT", "RIGHT", "PRESS", "NOTHING"], 0.1, 0.99, 0.1, 10)
		agent1 = RLAgent("agent1", ["UP", "DOWN", "LEFT", "RIGHT", "PRESS", "NOTHING"], 0.1, 0.99, 0.1, 10)
		env = CreateGridWorld("scenarios/scenario" + scenario + ".txt", agent0, agent1)

		if isCentralized:
			env.LearnCentralized()
		else:
			env.LearnDecentralized()
		
		env.WriteAgentsQtableToFile(isCentralized, scenario)

	elif len(sys.argv) == 4 and sys.argv[1] == "-run" and (sys.argv[2] == "-centralized" or sys.argv[2] == "-decentralized") and (sys.argv[3] == "-s1" or sys.argv[3] == "-s2" or sys.argv[3] == "-s3"):
		isCentralized = (sys.argv[2] == "-centralized")
		scenario = sys.argv[3][-1]

		agent0 = RLAgent("agent0", ["UP", "DOWN", "LEFT", "RIGHT", "PRESS", "NOTHING"], 0.1, 0.99, 0.1, 10)
		agent1 = RLAgent("agent1", ["UP", "DOWN", "LEFT", "RIGHT", "PRESS", "NOTHING"], 0.1, 0.99, 0.1, 10)
		env = CreateGridWorld("scenarios/scenario" + scenario + ".txt", agent0, agent1)

		env.LoadAgentsQtableFromFile(isCentralized, scenario)
		env.EvalAgents()

	else:
		print("Unknown command. Possible commands are:")
		print("> main.py -learn [-centralized|-decentralized] [-s1|-s2|-s3]")
		print("> main.py -run [-centralized|-decentralized] [-s1|-s2|-s3]")
	

