import numpy as np

class Agent(object):
    """
    This is a representation of a financial agent.
    """

    def __init__(self, id, type, value, quantity, max):

        self.id = id
        self.type = type
        self.value = value
        self.quantity = quantity
        self.price = max

    def __str__(self):
        return f"This agent is of the type {self.type} with id: {self.id} and " \
                f"has preferences price: {self.value} and quantity: {self.quantity}"

    def offer_price(self):
        price = np.random.randint(1, 200)
        if self.check_bid(price):
            self.price = price
            return price
        return 0

    def check_bid(self, price):
        if self.type == "buyer":
            return price > self.price
        elif self.type == "seller":
            return price < self.price

class Agent_ZI_U(Agent):
    pass
