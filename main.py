from CreateWorldFromFile import *
from Agents import *
from CompareBehaviors import *
import sys

LEARN = "-learn"
RUN = "-run"
COMPARE = "-compare"
CENTRALIZED = "centralized"
CENTRALIZED_F = "-" + CENTRALIZED
DECENTRALIZED = "decentralized"
DECENTRALIZED_F = "-" + DECENTRALIZED
SINGLE = "singleagents"
SINGLE_F = "-" + SINGLE
S1 = "-s1"
S2 = "-s2"
S3 = "-s3"


if __name__ == "__main__":
	if len(sys.argv) == 4 and sys.argv[1] == LEARN and (sys.argv[2] == CENTRALIZED_F or sys.argv[2] == DECENTRALIZED_F or sys.argv[2] == SINGLE_F) and (sys.argv[3] == S1 or sys.argv[3] == S2 or sys.argv[3] == S3):
		mode = sys.argv[2][1:]
		scenario = sys.argv[3][-1]
		scenarioPath = "scenarios/scenario" + scenario + ".txt"
		
		singleActions = ["UP", "DOWN", "LEFT", "RIGHT", "PRESS", "NOTHING"]

		if mode == CENTRALIZED:
			doubleActions = []
			for a0 in singleActions:
				for a1 in singleActions.copy():
					doubleActions.append(a0 + "-" + a1)
			agents = DoubleAgent("agent0", "agent1", doubleActions, 0.1, 0.999, 1.0, 0.05, 10)
			env = CreateGridWorld(scenarioPath, agents, None)

			if scenario == "1":
				env.LearnCentralized(1000, 500)
			elif scenario == "2":
				env.LearnCentralized(1000, 800)
			elif scenario == "3":
				env.LearnCentralized(2000, 1500)
			else:
				print("Unknown scenario.")
		elif mode == SINGLE:
			agent0 = SingleAgent("agent0", singleActions, 0.1, 0.999, 1.0, 0.05, 10)
			agent1 = SingleAgent("agent1", singleActions, 0.1, 0.999, 1.0, 0.05, 10)
			env = CreateGridWorld(scenarioPath, agent0, agent1)

			if scenario == "1":
				agent0.LearnDynaQ(env, 1000, 500)
				agent1.LearnDynaQ(env, 1000, 500)
			elif scenario == "2":
				agent0.LearnDynaQ(env, 1000, 800)
				agent1.LearnDynaQ(env, 1000, 800)
			elif scenario == "3":
				agent0.LearnDynaQ(env, 2000, 1500)
				agent1.LearnDynaQ(env, 2000, 1500)
			else:
				print("Unknown scenario.")

		else:
			agent0 = SingleAgent("agent0", singleActions, 0.1, 0.999, 1.0, 0.05, 10)
			agent1 = SingleAgent("agent1", singleActions, 0.1, 0.999, 1.0, 0.05, 10)
			env = CreateGridWorld(scenarioPath, agent0, agent1)

			if scenario == "1":
				env.LearnDecentralized(1000, 500)
			elif scenario == "2":
				env.LearnDecentralized(1000, 800)
			elif scenario == "3":
				env.LearnDecentralized(2000, 1500)
			else:
				print("Unknown scenario.")

		#env.EvalAgents(True)
		env.WriteAgentsQtableToFile(mode, scenario)

	elif len(sys.argv) == 4 and sys.argv[1] == RUN and (sys.argv[2] == CENTRALIZED_F or sys.argv[2] == DECENTRALIZED_F or sys.argv[2] == SINGLE_F) and (sys.argv[3] == S1 or sys.argv[3] == S2 or sys.argv[3] == S3):
		mode = sys.argv[2][1:]
		scenario = sys.argv[3][-1]
		scenarioPath = "scenarios/scenario" + scenario + ".txt"

		singleActions = ["UP", "DOWN", "LEFT", "RIGHT", "PRESS", "NOTHING"]

		if mode == CENTRALIZED:
			doubleActions = []
			for a0 in singleActions:
				for a1 in singleActions.copy():
					doubleActions.append(a0 + "-" + a1)
			agents = DoubleAgent("agent0", "agent1", doubleActions, 0.1, 0.999, 1.0, 0.05, 10)
			env = CreateGridWorld(scenarioPath, agents, None)

			env.LoadAgentsQtableFromFile(mode, scenario)
			env.EvalAgents(True)
		else:
			agent0 = SingleAgent("agent0", singleActions, 0.1, 0.999, 0.0, 0.0, 10)
			agent1 = SingleAgent("agent1", singleActions, 0.1, 0.999, 0.0, 0.0, 10)
			env = CreateGridWorld(scenarioPath, agent0, agent1)

			env.LoadAgentsQtableFromFile(mode, scenario)
			env.EvalAgents(True)

	elif len(sys.argv) == 5 and sys.argv[1] == COMPARE and (sys.argv[2] == CENTRALIZED_F or sys.argv[2] == DECENTRALIZED_F or sys.argv[2] == SINGLE_F) and (sys.argv[3] == CENTRALIZED_F or sys.argv[3] == DECENTRALIZED_F or sys.argv[3] == SINGLE_F) and (sys.argv[4] == S1 or sys.argv[4] == S2 or sys.argv[4] == S3):
		behavior1 = sys.argv[2][1:]
		behavior2 = sys.argv[3][1:]
		scenario = sys.argv[4][-1]
		scenarioPath = "scenarios/scenario" + scenario + ".txt"

		singleActions = ["UP", "DOWN", "LEFT", "RIGHT", "PRESS", "NOTHING"]
		doubleActions = []
		if behavior1 == CENTRALIZED or behavior2 == CENTRALIZED:
			for a0 in singleActions:
				for a1 in singleActions.copy():
					doubleActions.append(a0 + "-" + a1)

		env1 = None
		env2 = None
		policy1 = None
		policy2 = None
		if behavior1 == CENTRALIZED:
			agents = DoubleAgent("agent0", "agent1", doubleActions, 0.1, 0.999, 1.0, 0.05, 10)
			env1 = CreateGridWorld(scenarioPath, agents, None)
			env1.LoadAgentsQtableFromFile(behavior1, scenario)
			policy1 = GetPolicy(agents)
		else:
			agent0 = SingleAgent("agent0", singleActions, 0.1, 0.999, 0.0, 0.0, 10)
			agent1 = SingleAgent("agent1", singleActions, 0.1, 0.999, 0.0, 0.0, 10)
			env1 = CreateGridWorld(scenarioPath, agent0, agent1)
			env1.LoadAgentsQtableFromFile(behavior1, scenario)
			policy1 = CreateJointPolicy(agent0, agent1)
		if behavior2 == CENTRALIZED:
			agents = DoubleAgent("agent0", "agent1", doubleActions, 0.1, 0.999, 1.0, 0.05, 10)
			env2 = CreateGridWorld(scenarioPath, agents, None)
			env2.LoadAgentsQtableFromFile(behavior2, scenario)
			policy2 = GetPolicy(agents)
		else:
			agent0 = SingleAgent("agent0", singleActions, 0.1, 0.999, 0.0, 0.0, 10)
			agent1 = SingleAgent("agent1", singleActions, 0.1, 0.999, 0.0, 0.0, 10)
			env2 = CreateGridWorld(scenarioPath, agent0, agent1)
			env2.LoadAgentsQtableFromFile(behavior2, scenario)
			policy2 = CreateJointPolicy(agent0, agent1)

		gridSize = env1.GetGridSize()
		trace1, reward1 = env1.EvalAgents(False)
		trace2, reward2 = env2.EvalAgents(False)
		rewardDiff = abs(reward1 - reward2)
		print("REWARD DIFF: " + str(rewardDiff))
		hitmapsPerAgentDiff = CompareHitmapsPerAgent(gridSize, trace1.copy(), trace2.copy())
		print("HITMAP PER AGENT DIFF: " + str(hitmapsPerAgentDiff))
		hitmapsDiff = CompareHitmaps(gridSize, trace1.copy(), trace2.copy())
		print("HITMAP DIFF: " + str(hitmapsDiff))
		policiesDiff = CompareAgentsPolicies(policy1, policy2)
		print("POLICIES DIFF: " + str(policiesDiff))

	else:
		print("Unknown command. Possible commands are:")
		print("> main.py -learn [-centralized|-decentralized|-singleagents] [-s1|-s2|-s3]")
		print("> main.py -run [-centralized|-decentralized|-singleagents] [-s1|-s2|-s3]")
		print("> main.py -compare [-centralized|-decentralized|-singleagents] [-centralized|-decentralized|-singleagents] [-s1|-s2|-s3]")
	

