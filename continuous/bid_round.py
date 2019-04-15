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
    considering a double auction for ZI-U traders
    """

    name = "ZI-U"

    def __init__(self, amount, valuations, costs):
        """
        Every Round is intiialized with a random distribution of
        buyers/sellers and variables to keep track of max bid, min ask,
        price transactions, agents who've met, last round and surplus.
        """

        self.agents = self.create_agents(amount, valuations, costs)
        # self.max_bid = np.array([0, 0])
        # self.min_ask = np.array([0, 201])
        self.max_bid = {"id": 0, "price": 1}
        self.min_ask = {"id": 0, "price": 200}
        self.transactions = []
        self.succes = []
        self.last_round = False
        self.surplus = 0

    def create_agents(self, amount, valuations, costs):
        """
        Divide the traders into buyers/sellers (ZI-U),
        all with specific id, and redemption/cost price
        """
        agents = []
        counter = 1

        for value, quantity in valuations:
            agents.append(Agent(counter, "buyer", value, quantity, 1))
            counter += 1

        for cost, quantity in costs:
            agents.append(Agent(counter, "seller", cost, quantity, 200))
            counter += 1

        return agents

    def check_transaction(self):
        """
        Checks if at least one transaction is possible
        """

        return self.max_bid["price"] >= self.min_ask["price"]

    def make_transaction(self):
        """
        Procces transaction: adjust quantity buyer/seller, total surplus,
        """
        buyer, seller = self.pick_agents_transactions()
        self.preprocces_transaction(buyer, seller)
        self.check_agents(buyer, seller)
        self.reset_offers()

    def pick_agents_transactions(self):
        """
        Randomly selects buyer and seller
        from the set of possible agents
        for transaction
        """

        possible_sellers = []
        possible_buyers = []

        for agent in self.agents:
            if agent.type == "seller" and agent.bid <= self.max_bid["price"]:
                possible_sellers.append(agent)
            elif agent.type == "buyer" and agent.bid >= self.min_ask["price"]:
                possible_buyers.append(agent)

        # print(f"Length Buyers: {len(possible_buyers)}")
        # print(f"Length Sellers: {len(possible_sellers)}")
        # print(f"Length All Agents: {len(self.agents)}")
        # for agent in self.agents:
        #     print(f"Agent with type: {agent.type} and outstanding bid: {agent.bid}")

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
        self.surplus += buyer.valuation - seller.valuation
        self.transactions.append(buyer.bid)
        buyer.profits.append(buyer.valuation - buyer.bid)
        seller.profits.append(buyer.bid - seller.valuation)
        buyer.bid = 1
        seller.bid = 200
        self.agents = [agent for agent in self.agents if agent not in (buyer, seller)]

    def reset_offers(self):
        """
        Reset all outstanding offers
        after a transaction
        """

        self.max_bid = {"id": 0, "price": 1}
        self.min_ask = {"id": 0, "price": 200}
        participants = self.agents + self.succes

        for agent in participants:
            if agent.type == "buyer":
                agent.bid = 1
            elif agent.type == "seller":
                agent.bid = 200

    def check_agents(self, buyer, seller):
        """
        Checks if agents still can participate
        in next bidding round
        """

        # if buyer/seller still has quantity to sell, keep them in game
        if buyer.quantity:
            self.succes.append(buyer)
        if seller.quantity:
            self.succes.append(seller)


    def check_particpants(self):
        """
        Checks if bids are possible
        among those still participating in the round (ZI-U)
        """

        buyers = 0
        sellers = 0
        if not self.agents:
            return False

        for agent in self.agents:
            if agent.type == "buyer":
                buyers += 1
            elif agent.type == "seller":
                sellers += 1

        return buyers and sellers

    def check_all_participants(self):
        """
        Checks if bids arr possible among all participants
        (also those who've already closed a deal) only for ZI-U
        """

        if not self.agents and not self.succes:
            return False

        buyers = 0
        sellers = 0
        all_participants = self.agents + self.succes
        for agent in all_participants:
            if agent.type == "buyer":
                buyers += 1
            elif agent.type == "seller":
                sellers += 1

        return buyers and sellers


    def reset_round(self):
        """
        Checks if rounds need to reset
        (mix participants with those who already closed a deal succesfully)
        """

        return (not self.check_particpants() and self.check_all_participants())


    def check_last_round(self):
        """
        Checks if next round can take place
        """

        return ((not self.agents and not self.succes) or
            (not self.check_particpants() and not self.check_all_participants()))



class Round_C(Round):
    """
    Reprensentation of the structure of bidding round
    considering a double auction for ZI-C traders
    """

    name = "ZI-C"

    def __init__(self, amount, valuations, costs):
        """
        Every Round is intiialized with a random distribution of
        buyers/sellers and variables to keep track of max bid, min ask,
        price transactions, agents who've met, last round and surplus.
        """
        Round.__init__(self, amount, valuations, costs)
        self.agents = self.create_agents(amount, valuations, costs)
        self.max_bid = {"id": 0, "price": 1}
        self.min_ask = {"id": 0, "price": 200}
        self.transactions = []
        self.succes = []
        self.last_round = False
        self.surplus = 0


    def create_agents(self, amount, valuations, costs):
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

    def check_particpants(self):
        """
        Checks if bids are possible
        among those still participating in the round (ZI-C)
        """

        if not self.agents:
            return False

        buyers = []
        sellers = []

        for agent in self.agents:
            if agent.type == "buyer":
                buyers.append(agent.valuation)
            elif agent.type == "seller":
                sellers.append(agent.valuation)

        if not buyers or not sellers:
            return False

        deal = 0
        for buy in buyers:
            if any(sell <= buy for sell in sellers):
                deal += 1

        return deal

    def check_all_participants(self):
        """
        Checks if bids arr possible among all participants
        (also those who've already closed a deal) only for ZI-U
        """

        if not self.agents and not self.succes:
            return False

        buyers = []
        sellers = []

        all_participants = self.agents + self.succes
        for agent in all_participants:
            if agent.type == "buyer":
                buyers.append(agent.valuation)
            elif agent.type == "seller":
                sellers.append(agent.valuation)

        if not buyers or not sellers:
            return False

        deal = 0
        for buy in buyers:
            if any(sell <= buy for sell in sellers):
                deal += 1

        return deal
