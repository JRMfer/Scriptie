# AGENT
# Julien Fer
# University of Amsterdam
#
# This script contains the functionality to computationally visualize either a
# ZI-U or ZI-C agent.

import numpy as np

class Agent(object):
    """
    This is a representation of
    a financial agent (buyer/seller).
    """
    name = "ZI-U"

    def __init__(self, id, type, valuation, quantity, max):
        """
        Every agent is intiialized as buyer/seller
        with id, redemption/cost price and
        corresponding quantity and also a variable
        to keep track of individual transasction price.
        """

        self.id = id
        self.type = type
        self.valuation = valuation
        self.quantity = quantity
        self.bid = max
        self.transactions = []

    def __str__(self):
        """
        Prints type, id, value and quantity of agent
        """
        return f"This agent is of the type {self.type} with id: {self.id} and " \
                f"has preferences price: {self.value} and quantity: {self.quantity}"

    def offer_price(self):
        """
        Random offer strategy of ZI-U trader
        """

        price = round(np.random.uniform(1, 200), 2)
        # print(f"Price: {price}")
        if self.check_bid(price):
            self.bid = price
            return price
        return 0

    def check_bid(self, price):
        """
        Check if bid is better than it's own bid
        """

        if self.type == "buyer":
            return price > self.bid
        elif self.type == "seller":
            return price < self.bid

class Agent_C(Agent):
    """
    Representation of a ZI-C agent
    """

    name = "ZI-C"

    def offer_price(self):
        """
        Random offer strategy for a ZI-C agent
        """

        if self.type == "buyer":
            price = round(np.random.uniform(1, self.valuation), 2)
        elif self.type == "seller":
            price = round(np.random.uniform(self.valuation, 200), 2)

        if self.check_bid(price):
            self.bid = price
            return price
        return 0
