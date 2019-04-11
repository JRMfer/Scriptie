# This is a script to simulate zero-intellegence
# robots in a double auction

import numpy as np
from agent import Agent

TYPES = ["buyer", "seller"]
AMOUNT = 12
VALUATION = np.array([[125, 1], [115, 1], [95, 1], [80, 1], [65, 1], [55, 1]])
COSTS = np.array([[50, 1], [55, 1], [60, 1], [65, 1], [70, 1], [75, 1]])

def main():
    create_agents(TYPES, AMOUNT, VALUATION, COSTS)


def create_agents(types, amount, valuations, costs):
    agents = []

    for value, quantity in valuations:
        agents.append(Agent("buyer", value, quantity))

    for cost, quantity in costs:
        agents.append(Agent("seller", cost, quantity))

    for agent in agents:
        print(agent)


if __name__ == "__main__":
    main()
