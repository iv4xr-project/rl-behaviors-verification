from CreateWorldFromFile import *
from Agents import *


if __name__ == "__main__":
	agent0 = RLAgent("agent0", ["UP", "DOWN", "LEFT", "RIGHT", "PRESS", "NOTHING"], 0.1, 0.99, 0.1, 10)
	agent1 = RLAgent("agent1", ["UP", "DOWN", "LEFT", "RIGHT", "PRESS", "NOTHING"], 0.1, 0.99, 0.1, 10)
	env = CreateGridWorld("scenarios/scenario1.txt", agent0, agent1) #ep 300 stepsMax 1000
	#env = CreateGridWorld("scenarios/scenario2.txt", agent0, agent1) #ep 300 stepsMax 1000
	#env = CreateGridWorld("scenarios/scenario3.txt", agent0, agent1) #ep 300 stepsMax 1000
	agent0.Learn(env)
	agent0.Eval(env)
	#agent1.Learn(env)
	#agent1.Eval(env)



