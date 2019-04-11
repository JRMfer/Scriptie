import numpy as np

class Agent(object):
    """
    This is a representation of
    a financial agent (buyer/seller).
    """

    def __init__(self, id, type, value, quantity, max):
        """
        Every agent is intiialized as buyer/seller
        with id, redemption/cost price and
        corresponding quantity and also a variable
        to keep track of individual transasction price.
        """

        self.id = id
        self.type = type
        self.value = value
        self.quantity = quantity
        self.price = max

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

        price = np.random.randint(1, 200)
        if self.check_bid(price):
            self.price = price
            return price
        return 0

    def check_bid(self, price):
        """
        Check if bid is better than it's own bid
        """
        
        if self.type == "buyer":
            return price > self.price
        elif self.type == "seller":
            return price < self.price

class Agent_ZI_U(Agent):
    pass
