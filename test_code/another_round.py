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
from agent_test import Agent, Agent_C

TYPES = ["buyer", "seller"]
TIME = 30

class Round(object):
    """
    Reprensentation of the structure of bidding round
    considering a double auction
    """

    name = "ZI-U"

    def __init__(self, types, amount, valuations, costs):
        """
        Every Round is intiialized with a random distribution of
        buyers/sellers and variables to keep track of max bid, min ask,
        price transactions, agents who've met, last round and surplus.
        """

        self.agents = self.create_agents(types, amount, valuations, costs)
        self.max_bid = np.array([0, 0])
        self.min_ask = np.array([0, 201])
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
            agents.append(Agent(counter, "seller", cost, quantity, 201))
            counter += 1

        return agents

    def check_transaction(self):
        """
        Checks if at least one transaction is possible
        """

        return self.max_bid[1] >= self.min_ask[1]

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
        print(f"length agents: {len(self.agents)}")
        for agent in self.agents:
            print(f"TYPE: {agent.type} and BID: {agent.bid}")

        for agent in self.agents:
            if agent.type == "seller" and agent.bid <= self.max_bid[1]:
                possible_sellers.append(agent)
            elif agent.type == "buyer" and agent.bid >= self.min_ask[1]:
                possible_buyers.append(agent)

        print(f"length sellers: {len(possible_sellers)}")
        print(f"length buyers: {len(possible_buyers)}")

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
        self.surplus += (buyer.valuation - seller.valuation)
        self.transactions.append(buyer.bid)
        buyer.transactions.append(buyer.bid)
        seller.transactions.append(buyer.bid)
        buyer.bid = 0
        seller.bid = 201
        self.agents = [agent for agent in self.agents if agent not in (buyer, seller)]
        # print("DEAL")
        # print(f"Surplus: {self.surplus}")

    def reset_offers(self):
        """
        Reset all outstanding offers
        after a transaction
        """

        self.max_bid = np.array([0, 0])
        self.min_ask = np.array([0, 200])
        participants = self.agents + self.succes

        for agent in participants:
            if agent.type == "buyer":
                agent.bid = 0
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

        if buyers > 0 and sellers > 0:
            return True

        return False

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

        if buyers > 0 and sellers > 0:
            return True

        return False


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

    name = "ZI-C"
    def __init__(self, types, amount, valuations, costs):
        Agent.__init__(self, types, amount, valuations, costs)
        self.agents = self.create_agents(types, amount, valuations, costs)
        self.max_bid = np.array([0, 0])
        self.min_ask = np.array([0, 200])
        self.transactions = []
        self.succes = []
        self.last_round = False
        self.surplus = 0


    def create_agents(self, types, amount, valuations, costs):
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
