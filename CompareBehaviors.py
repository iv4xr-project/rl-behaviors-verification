import numpy as np
from numpy import linalg

def CompareHitmapsPerAgent(gridSize, trace1, trace2):
	agent0env1 = np.zeros(gridSize)
	agent1env1 = np.zeros(gridSize)
	agent0env2 = np.zeros(gridSize)
	agent1env2 = np.zeros(gridSize)

	while len(trace1) > 0:
		pos = trace1.pop(0)
		agent0env1[pos[0]][pos[1]] += 1
		pos = trace1.pop(0)
		agent1env1[pos[0]][pos[1]] += 1

	while len(trace2) > 0:
		pos = trace2.pop(0)
		agent0env2[pos[0]][pos[1]] += 1
		pos = trace2.pop(0)
		agent1env2[pos[0]][pos[1]] += 1

	a0Diff = linalg.norm(agent0env1-agent0env2)
	a1Diff = linalg.norm(agent1env1-agent1env2)
	print("a0Diff " + str(a0Diff))
	print("a1Diff " + str(a1Diff))
	return (a0Diff + a1Diff) / 2


def CompareHitmaps(gridSize, trace1, trace2):
	env1 = np.zeros(gridSize)
	env2 = np.zeros(gridSize)

	while len(trace1) > 0:
		pos = trace1.pop(0)
		env1[pos[0]][pos[1]] += 1
		pos = trace1.pop(0)
		env1[pos[0]][pos[1]] += 1

	while len(trace2) > 0:
		pos = trace2.pop(0)
		env2[pos[0]][pos[1]] += 1
		pos = trace2.pop(0)
		env2[pos[0]][pos[1]] += 1

	return linalg.norm(env1-env2)



def CompareAgentsPolicies(gridSize, policy1, policy2):
	return 0
