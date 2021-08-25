from CreateWorldFromFile import *
from Agents import *
import sys


if __name__ == "__main__":
	if len(sys.argv) < 2:
		print("Unknown command! >main.py [-centralized|-decentralized]")
	else:
		if len(sys.argv) == 4 and sys.argv[1] == "-learn" and (sys.argv[2] == "-centralized" or sys.argv[2] == "-decentralized") and (sys.argv[3] == "-s1" or sys.argv[3] == "-s2" or sys.argv[3] == "-s3"):

		elif len(sys.argv) == 4 and sys.argv[1] == "-centralized" and sys.argv[2] == "-f" :
			policyfile = sys.argv[3]

		elif len(sys.argv) == 5 and sys.argv[1] == "-decentralized" and sys.argv[2] == "-f" :
			policyfile1 = sys.argv[3]
			policyfile2 = sys.argv[4]

		else:
			print("Unknown command! >main.py [-centralized|-decentralized]")
	agent0 = RLAgent("agent0", ["UP", "DOWN", "LEFT", "RIGHT", "PRESS", "NOTHING"], 0.1, 0.99, 0.1, 10)
	agent1 = RLAgent("agent1", ["UP", "DOWN", "LEFT", "RIGHT", "PRESS", "NOTHING"], 0.1, 0.99, 0.1, 10)
	#env = CreateGridWorld("scenarios/scenario1.txt", agent0, agent1) #ep 600 stepsMax 500
	env = CreateGridWorld("scenarios/scenario2.txt", agent0, agent1) #ep 600 stepsMax 500
	#env = CreateGridWorld("scenarios/scenario3.txt", agent0, agent1) #ep 300 stepsMax 1000
	#agent0.Learn(env) #ep 300 stepsMax 1000
	#agent0.Eval(env)
	#agent1.Learn(env)
	#agent1.Eval(env)

	#env.LearnDecentralized()
	#env.EvalAgents()


