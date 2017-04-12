import numpy
import random as ran


def reward(fileN):
    listR = numpy.zeros((81, 1), dtype=int)
    row = 0
    with open(fileN) as f:
        contend = f.readlines()
    for c in contend:
        listR[row][0] = int(c)
        row += 1
    return listR


def action(fileN):
    listA = numpy.zeros((81, 81), dtype=float)

    with open(fileN) as f:
        contend = f.readlines()

    for c in contend:
        singleL = c.split()
        listA[int(singleL[0]) - 1, int(singleL[1]) - 1] = float(singleL[2])

    return listA


def policy_evaluation(v_list, policy_list, rewardH, actionDir):
    for state in range(81):
        oldV = 0.0
        for nextS in range(81):
            oldV += actionDir[policy_list[state]][state][nextS] * v_list[nextS]

        v_list[state] = rewardH[state][0] + 0.99 * oldV
    return v_list


def p_iteration(actionDir, rewardH):

    action_list = [0, 1, 2, 3]
    policy_list = []

    for i in range(81):
        policy_list.append(ran.choice(action_list))

    v = [0.0] * 81

    #unchanged = False
    #while unchanged is not True:
    for k in range(500):
        v = policy_evaluation(v, policy_list, rewardH, actionDir)
        #unchanged = True

        for state in range(81):
            oldV = 0.0
            for nextS in range(81):
                oldV += actionDir[policy_list[state]][state][nextS] * v[nextS]

            maxV = float("-inf")
            maxA = float("-inf")
            for a in range(4):
                tmp = 0.0
                for nextS in range(81):
                    tmp += actionDir[a][state][nextS] * v[nextS]

                if tmp > maxV:
                    maxV = tmp
                    maxA = a

            if maxV > oldV:
                policy_list[state] = maxA
                #unchanged = False

    return policy_list, v


rewards = reward("rewards.txt")
action_west = action("prob_west.txt")
action_north = action("prob_north.txt")
action_east = action("prob_east.txt")
action_south = action("prob_south.txt")
action = [action_west, action_north, action_east, action_south]

policy, value = p_iteration(action, rewards)

toReturn = []
for i in range(0, 81):
    if policy[i] is 0:
        toReturn.append((i + 1, "WEST"))
    elif policy[i] is 1:
        toReturn.append((i + 1, "NORTH"))
    elif policy[i] is 2:
        toReturn.append((i + 1, "EAST"))
    elif policy[i] is 3:
        toReturn.append((i + 1, "SOUTH"))

print toReturn


