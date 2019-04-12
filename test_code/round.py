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
from agent import Agent, Agent_C

TYPES = ["buyer", "seller"]
TIME = 30

class Round(object):
    """
    Reprensentation of the structure of bidding round
    considering a double auction
    """

    name = ""

    def __init__(self, types, amount, valuations, costs):
        """
        Every Round is intiialized with a random distribution of
        buyers/sellers and variables to keep track of max bid, min ask,
        price transactions, agents who've met, last round and surplus.
        """

        self.agents = self.create_agents(types, amount, valuations, costs)
        Round.name = self.agents[0].name
        self.max_bid = np.array([0, 0])
        self.min_ask = np.array([0, 200])
        self.transactions = []
        self.succes = []
        self.last_round = False
        self.surplus = 0

    def create_agents(self, types, amount, valuations, costs):
        """
        Divide the traders into buyers/sellers (ZI-U),
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

    def create_agents_C(self, types, amount, valuations, costs):
        """
        Divide the traders into buyers/sellers (ZI-C),
        all with specific id, and redemption/cost price
        """
        agents = []
        counter = 1

        for value, quantity in valuations:
            agents.append(Agent_C(counter, "buyer", value, quantity, 0))
            counter += 1

        for cost, quantity in costs:
            agents.append(Agent_C(counter, "seller", cost, quantity, 200))
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

        for agent in self.agents:
            if agent.type == "seller" and agent.price <= self.max_bid[1]:
                possible_sellers.append(agent)
            elif agent.type == "buyer" and agent.price >= self.min_ask[1]:
                possible_buyers.append(agent)

        seller = random.choice(possible_sellers)
        buyer = random.choice(possible_buyers)

        return buyer, seller

    def preprocces_transaction(self, buyer, seller):
        """
        Adjust quantity seller/buyer, surplus
        and keep track of transaction price and
        individual transaction prices and "removes"
        buyer and seller from the participants
        """

        buyer.quantity -= 1
        seller.quantity -= 1
        self.surplus += (buyer.value - seller.value)
        self.transactions.append(buyer.price)
        seller.transactions.append(buyer.price)
        buyer.price = 0
        seller.price = 200
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
        participate in future bidings
        """
        #
        if buyer.quantity == 0 or seller.quantity == 0:
            self.last_round = True
        else:
            self.succes.append(buyer)
            self.succes.append(seller)
        # if buyer.quantity != 0:
        #     self.succes.append(buyer)
        # if seller.quantity != 0:
        #     self.succes.append(seller)

    def check_round(self):
        """
        Checks if round need to be reset
        """

        # # ONLY NECESSARY FOR ZI-C AGENTS!!!!
        # if not self.check_possible_transactions():
        #     self.agents += self.succes
        #     self.succes = []
            # self.last_round == False

        if len(self.succes) == 12:
            self.agents = self.succes
            self.succes = []
            # self.last_round == False


    def check_possible_transactions(self):
        """
        Checks if transactions can be made by participants
        (only important for ZI-C agents)
        """

        buyers = []
        sellers = []
        # participants = self.agents + self.succes

        for agent in self.agents:
        # for agent in self.agents
            if agent.type == "buyer":
                buyers.append(agent.value)
            elif agent.type == "seller":
                sellers.append(agent.value)

        deal = 0
        for buy, sell in zip(buyers, sellers):
            if buy >= sell:
                deal += 1

        if deal:
            return True

        return False


    def check_last_transactions(self):
        """
        Checks if transactions can be made
        (only important for ZI-C agents)
        """

        buyers = []
        sellers = []
        participants = self.agents + self.succes

        for agent in participants:
        # for agent in self.agents
            if agent.type == "buyer":
                buyers.append(agent.value)
            elif agent.type == "seller":
                sellers.append(agent.value)

        deal = 0
        for buy, sell in zip(buyers, sellers):
            if buy >= sell:
                deal += 1

        if deal:
            return True

        return False

    def check_last_round(self):
        """
        For ZI-C!!!!
        """
        trans_pos = self.check_last_transactions()
        self.last_round == True
        # if len
        # pass

    def make_transaction(self):
        """
        Randomsly selects agents,
        preprocces transaction, reset offers and
        check if agents are still participants and
        if every succesfull participant can participate
        """

        buyer, seller = self.pick_agents_transactions()
        self.preprocces_transaction(buyer, seller)
        self.check_agents(buyer, seller)
        self.reset_offers()
        self.check_round()
        # self.check_last_round()
