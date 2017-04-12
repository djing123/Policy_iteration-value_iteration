import numpy


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


def v_iteration(rewardH, actionDir):

    policy = [0] * 81
    v = [0.0] * 81
    loopC = True
    while loopC:

        v_prev = list(v)
        delta = 0

        for state in range(81):
            maxV = float("-inf")
            maxA = float("-inf")
            prev = v_prev[state]

            for a in range(4):
                tmp = 0.0
                for nextS in range(81):
                    tmp += actionDir[a][state][nextS] * v_prev[nextS]
                if tmp > maxV:
                    maxV = tmp
                    maxA = a

            v[state] = rewardH[state][0] + 0.99 * maxV

            policy[state] = maxA

            if abs(v[state] - prev) > delta:
                delta = abs(v[state] - prev)

        if delta < 0.0001:
            loopC = False
            break

    return v, policy


rewards = reward("rewards.txt")
action_west = action("prob_west.txt")
action_north = action("prob_north.txt")
action_east = action("prob_east.txt")
action_south = action("prob_south.txt")
action = [action_west, action_north, action_east, action_south]


value, policy_pi = v_iteration(rewards, action)
toReturn = []
for i in range(0, 81):
    if value[i] > 0:
        if policy_pi[i] is 0:
            toReturn.append((i + 1, value[i], "WEST"))
        elif policy_pi[i] is 1:
            toReturn.append((i + 1, value[i], "NORTH"))
        elif policy_pi[i] is 2:
            toReturn.append((i + 1, value[i], "EAST"))
        elif policy_pi[i] is 3:
            toReturn.append((i + 1, value[i], "SOUTH"))

print toReturn






