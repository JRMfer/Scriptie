# Test versie voor scriptie
#

import time
import numpy as np
from agent import Agent, Agent_ZI_U

TYPES = ["buyer", "seller"]

TIME = 30

class Round(object):

    def __init__(self, types, amount, valuations, costs):

        self.agents = self.create_agents_u(types, amount, valuations, costs)
        self.max_bid = np.array([0, 0])
        self.min_ask = np.array([0, 200])
        self.transactions = []
        self.surplus = 0

    def create_agents(self, types, amount, valuations, costs):
        agents = []
        counter = 1

        for value, quantity in valuations:
            agents.append(Agent(counter, "buyer", value, quantity, 0))
            counter += 1

        for cost, quantity in costs:
            agents.append(Agent(counter, "seller", cost, quantity, 200))
            counter += 1

        return agents

    def create_agents_u(self, types, amount, valuations, costs):
        agents = []
        counter = 1

        for value, quantity in valuations:
            agents.append(Agent_ZI_U(counter, "buyer", value, quantity, 0))
            counter += 1

        for cost, quantity in costs:
            agents.append(Agent_ZI_U(counter, "seller", cost, quantity, 200))
            counter += 1

        return agents

    def check_transaction(self):
        return self.max_bid[1] >= self.min_ask[1]

    def make_transaction(self):

        possible_sellers = []
        possible_buyers = []

        # check for all possible sellers
        for agent in self.agents:
            if agent.type == "seller" and agent.price <= self.max_bid[1]:
                possible_sellers.append(agent)
            elif agent.type == "buyer" and agent.price >= self.min_ask[1]:
                possible_buyers.append(agent)

        # pick random seller/buyer
        if len(possible_sellers) == 1:
            seller = possible_sellers[0]
        else:
            index_seller = np.random.randint(0, len(possible_sellers) - 1)
            seller = possible_sellers[index_seller]

        # pick random buyer
        if len(possible_buyers) == 1:
            buyer = possible_buyers[0]
        else:
            index_buyer = np.random.randint(0, len(possible_buyers) - 1)
            buyer = possible_buyers[index_buyer]


        # adjust quantity buyer/seller and total surplus,
        # also keep track of transaction price
        buyer.quantity -= 1
        seller.quantity -= 1
        self.surplus += ((buyer.value - self.max_bid[1]) + (self.max_bid[1] - seller.value))
        self.transactions.append(self.max_bid[1])

        # reset offers
        self.reset_offers()

        # remove buyer/seller from round, if quantity is met
        if buyer.quantity == 0:
            self.agents.remove(buyer)

        elif seller.quantity == 0:
            self.agents.remove(seller)


    def reset_offers(self):
        self.max_bid = np.array([0, 0])
        self.min_ask = np.array([0, 200])

        for agent in self.agents:
            if agent.type == "buyer":
                agent.price = 0
            elif agent.type == "seller":
                agent.price = 200


    def remove_agent(self, trader):

        for agent in self.agents:
            if agent.id == trader.id:
                self.agents.remove(agent)
