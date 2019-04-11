# This is a script to simulate zero-intellegence
# robots in a double auction

import numpy as np
from agent import Agent

class Market(object):

    def __init__(self, types, amount, valuations, costs):
        self.agents = self.create_agents(types, amount, valuations, costs)

    def create_agents(self,types, amount, valuations, costs):
        agents = []

        for value, quantity in valuations:
            agents.append(Agent("buyer", value, quantity))

        for cost, quantity in costs:
            agents.append(Agent("seller", cost, quantity))

        return agents
