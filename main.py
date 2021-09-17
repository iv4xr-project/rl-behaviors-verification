from CreateWorldFromFile import *
from Agents import *
import sys


if __name__ == "__main__":
	if len(sys.argv) == 4 and sys.argv[1] == "-learn" and (sys.argv[2] == "-centralized" or sys.argv[2] == "-decentralized" or sys.argv[2] == "-singleagents") and (sys.argv[3] == "-s1" or sys.argv[3] == "-s2" or sys.argv[3] == "-s3"):
		mode = sys.argv[2][1:]
		scenario = sys.argv[3][-1]
		
		singleActions = ["UP", "DOWN", "LEFT", "RIGHT", "PRESS", "NOTHING"]

		if mode == "centralized":
			doubleActions = []
			for a0 in singleActions:
				for a1 in singleActions.copy():
					doubleActions.append(a0 + "-" + a1)
			agents = DoubleAgent("agent0", "agent1", doubleActions, 0.1, 0.999, 1.0, 0.05, 10)
			env = CreateGridWorld("scenarios/scenario" + scenario + ".txt", agents, None)

			if scenario == "1":
				env.LearnCentralized(500, 500)
			elif scenario == "2":
				env.LearnCentralized(500, 800)
			elif scenario == "3":
				env.LearnCentralized(2000, 1500)
			else:
				print("Unknown scenario.")
			env.EvalAgentsCentralized()
		elif mode == "singleagents":
			agent0 = SingleAgent("agent0", singleActions, 0.1, 0.999, 1.0, 0.05, 10)
			agent1 = SingleAgent("agent1", singleActions, 0.1, 0.999, 1.0, 0.05, 10)
			env = CreateGridWorld("scenarios/scenario" + scenario + ".txt", agent0, agent1)

			if scenario == "1":
				agent0.LearnDynaQ(env, 500, 500)
				agent1.LearnDynaQ(env, 500, 500)
			elif scenario == "2":
				env.LearnDecentralized(500, 800)
			elif scenario == "3":
				env.LearnDecentralized(2000, 1500)
			else:
				print("Unknown scenario.")

			env.EvalAgentsDecentralized()
		else:
			agent0 = SingleAgent("agent0", singleActions, 0.1, 0.999, 1.0, 0.05, 10)
			agent1 = SingleAgent("agent1", singleActions, 0.1, 0.999, 1.0, 0.05, 10)
			env = CreateGridWorld("scenarios/scenario" + scenario + ".txt", agent0, agent1)

			if scenario == "1":
				env.LearnDecentralized(500, 500)
			elif scenario == "2":
				env.LearnDecentralized(500, 800)
			elif scenario == "3":
				env.LearnDecentralized(2000, 1500)
			else:
				print("Unknown scenario.")

			env.EvalAgentsDecentralized()
		env.WriteAgentsQtableToFile(mode, scenario)

	elif len(sys.argv) == 4 and sys.argv[1] == "-run" and (sys.argv[2] == "-centralized" or sys.argv[2] == "-decentralized") and (sys.argv[3] == "-s1" or sys.argv[3] == "-s2" or sys.argv[3] == "-s3"):
		scenario = sys.argv[3][-1]

		singleActions = ["UP", "DOWN", "LEFT", "RIGHT", "PRESS", "NOTHING"]

		if mode == "centralized":
			doubleActions = []
			for a0 in singleActions:
				for a1 in singleActions.copy():
					doubleActions.append(a0 + "-" + a1)
			agents = DoubleAgent("agent0", "agent1", doubleActions, 0.1, 0.999, 1.0, 0.05, 10)
			env = CreateGridWorld("scenarios/scenario" + scenario + ".txt", agents, None)

			env.LoadAgentsQtableFromFile(mode, scenario)
			env.EvalAgentsCentralized()
		elif mode == "singleagents":
			print("NOT IMPLEMENTED!")
		else:
			agent0 = SingleAgent("agent0", ["UP", "DOWN", "LEFT", "RIGHT", "PRESS", "NOTHING"], 0.1, 0.999, 0.0, 0.0, 10)
			agent1 = SingleAgent("agent1", ["UP", "DOWN", "LEFT", "RIGHT", "PRESS", "NOTHING"], 0.1, 0.999, 0.0, 0.0, 10)
			env = CreateGridWorld("scenarios/scenario" + scenario + ".txt", agent0, agent1)

			env.LoadAgentsQtableFromFile(mode, scenario)
			env.EvalAgentsDecentralized()

	else:
		print("Unknown command. Possible commands are:")
		print("> main.py -learn [-centralized|-decentralized] [-s1|-s2|-s3]")
		print("> main.py -run [-centralized|-decentralized] [-s1|-s2|-s3]")
	

