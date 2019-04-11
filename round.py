# Round
# Julien Fer (10649441)
# University of Amsterdam
#
# This script contains the functionailty
# to represent a bidding round for a
# double auction

import time
import random
import numpy as np
from agent import Agent, Agent_ZI_U

TYPES = ["buyer", "seller"]
TIME = 30

class Round(object):
    """
    Reprensentation of the structure of bidding round
    considering a double auction
    """

    def __init__(self, types, amount, valuations, costs):
        """
        Every Round is intiialized with a random distribution of
        buyers/sellers and variables to keep track of max bid, min ask,
        price transactions, agents who've met, last round and surplus.
        """

        self.agents = self.create_agents(types, amount, valuations, costs)
        self.max_bid = np.array([0, 0])
        self.min_ask = np.array([0, 200])
        self.transactions = []
        self.succes = []
        self.last_round = False
        self.surplus = 0

    def create_agents(self, types, amount, valuations, costs):
        """
        Divide the traders into buyers/sellers (BASIC),
        all with specific id, and redemption/cost price
        """
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
        """
        Divide the traders into buyers/sellers (ZI-U),
        all with specific id, and redemption/cost price
        """
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
        """
        Checks if at least one transaction is possible
        """

        return self.max_bid[1] >= self.min_ask[1]

    def pick_agents_transactions(self):
        """
        Randomly selects buyer and seller
        from the set of possible agents
        for transaction
        """

        possible_sellers = []
        possible_buyers = []

        # check for all possible sellers
        for agent in self.agents:
            if agent.type == "seller" and agent.price <= self.max_bid[1]:
                possible_sellers.append(agent)
            elif agent.type == "buyer" and agent.price >= self.min_ask[1]:
                possible_buyers.append(agent)

        # random seller/buyer
        seller = random.choice(possible_sellers)
        buyer = random.choice(possible_buyers)

        return buyer, seller

    def preprocces_transaction(self, buyer, seller):
        """
        Adjust quantity seller/buyer, surplus
        and keep track of transaction price
        """

        # adjust quantity, surplus and keep track of transaction price
        buyer.quantity -= 1
        seller.quantity -= 1
        self.surplus += ((buyer.value - buyer.price) + (buyer.price - seller.value))
        self.transactions.append(buyer.price)

        # keep track of individual transaction prices (only for seller)
        seller.price = buyer.price

        # "remove" agent temporary from auction
        self.agents = [agent for agent in self.agents if agent not in (buyer, seller)]

    def reset_offers(self):
        """
        Reset all outstanding offers
        after a transaction
        """

        self.max_bid = np.array([0, 0])
        self.min_ask = np.array([0, 200])

        for agent in self.agents:
            if agent.type == "buyer":
                agent.price = 0
            elif agent.type == "seller":
                agent.price = 200

    def check_agents(self, buyer, seller):
        """
        Check if agents still need to
        participate in round
        """

        # check if quantity is met, if not "save" agents "outside" participants
        if buyer.quantity == 0 or seller.quantity == 0:
            self.last_round = True
        else:
            self.succes.append(buyer)
            self.succes.append(seller)

    def check_round(self):
        """
        Checks if round need to be reset
        """

        # checks if every agent has traded, if so make them participants again
        if len(self.succes) == 12:
            self.agents = self.succes
            self.succes = []

    def make_transaction(self):
        """
        Randomsly selects agents,
        preprocces transaction, reset offers and
        check if agents are still participants and
        if every succesfull participant can participate
        """

        buyer, seller = self.pick_agents_transactions()
        self.preprocces_transaction(buyer, seller)

        # reset offers
        self.reset_offers()

        self.check_agents(buyer, seller)
        self.check_round()
