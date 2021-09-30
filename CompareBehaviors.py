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


def GetPolicy(agent):
	policies = {}
	size = len(agent.Actions)
	for state in agent.QTable.keys():
		action = agent.ChooseCurrentBestAction(state)
		policy = []
		for i in range(size):
			if i == action:
				policy.append(1)
			else:
				policy.append(0)
		policies[state] = policy
	return policies


def CreateJointPolicy(agent0, agent1):
	policies = {}
	for state0 in agent0.QTable.keys():
		pos0 = state0[0:4]
		env0 = state0[4:]
		action0 = agent0.ChooseCurrentBestAction(state0)
		for state1 in agent1.QTable.keys():
			pos1 = state1[0:4]
			env1 = state1[4:]
			if env0 == env1:
				action1 = agent1.ChooseCurrentBestAction(state1)
				jointState = pos0 + pos1 + env0
				jointAction = (6 * action0) + action1
				policy = []
				for i in range(36):
					if i == jointAction:
						policy.append(1)
					else:
						policy.append(0)
				if jointState in policies:
					print("weird")
				policies[jointState] = policy
	return policies



def CompareAgentsPolicies(policy0, policy1):
	#print(len(policy0))
	#print(len(policy1))
	temp0 = policy0.copy()
	temp1 = policy1.copy()
	for state0 in policy0.keys():
		if not state0 in policy1:
			temp0.pop(state0)
	for state1 in policy1.keys():
		if not state1 in policy0:
			temp1.pop(state1)
	mat0 = np.zeros((len(temp0), 36))
	mat1 = np.zeros((len(temp1), 36))
	i = 0
	for state0 in sorted(temp0):
		mat0[i] = temp0[state0]
		i += 1
	i = 0
	counter = 0
	for state1 in sorted(temp1):
		if temp0[state1] != temp1[state1]:
			counter += 1
			#print(temp0[state1])
			#print(temp1[state1])
			#print("-----")
		mat1[i] = temp1[state1]
		i += 1
	return linalg.norm(mat0-mat1)



