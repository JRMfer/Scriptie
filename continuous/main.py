# ABM Model
# Julien Fer (10649441)
# University of Amsterdam
#
# This script generates an ABM model based on either ZI-U or ZI-C agents.
# Several rounds (30 seconds) are generated. In every rounds the agents are
# equally divided in buyers and sellers and in every loop (bid round) an agent
# will be selected at random and it will makes its offer and checks
# all the neceassary to simulate the rules of a double auction.

import numpy as np
import matplotlib.pylab as plt
import time
import random
from bid_round import Round, Round_C

TYPES = ["buyer", "seller"]
AMOUNT = 12
TIME = 30
ROUNDS = 6
VALUATION = np.array([[105, 5], [97, 10], [90, 15], [82, 20], [75, 25], [70, 30]])
COSTS = np.array([[40, 5], [47, 10], [55, 15], [62, 20], [77, 25], [85, 30]])
# VALUATION = [{"price": 105, "quantity": 5}, {"price": 97, "quantity": 10},
#             {"price": 90, "quantity":15}, {"price": 82, "quantity": 20},
#             {"price": 75, "quantity": 25}, {"price": 70, "quantity": 30}]
# COSTS = [{"price": 40, "quantity": 5}, {"price": 47, "quantity": 10},
#             {"price": 55, "quantity":15}, {"price": 62, "quantity": 20},
#             {"price": 77, "quantity": 25}, {"price": 85, "quantity": 30}]
# VALUATION = np.array([[105, 6], [97, 6], [90, 6], [82, 6], [75, 6], [70, 6]])
# COSTS = np.array([[40, 6], [47, 6], [55, 6], [62, 6], [65, 6], [80, 6]])
# VALUATION = np.array([[105, 1], [97, 2], [90, 3], [82, 4], [75, 5], [70, 6]])
# COSTS = np.array([[40, 6], [47, 5], [55, 4], [62, 3], [65, 2], [80, 1]])

def main():

    simulation(ROUNDS, AMOUNT, VALUATION, COSTS)

def simulation(rounds, amount, valuations, costs):
    """
    Starts bidding simulation for
    a certain amount of rounds, agents and
    a given distribution of the redemption
    and cost value of the buyers/sellers
    """

    # calculate max total surplus
    surplus = total_surplus()
    print(f"max surplus: {surplus}")

    plot_demand_supply(valuations, costs, "Market_1")

    # simulate the amount of rounds
    for counter in range(rounds):

        # create round and set time to 30 seconds
        period = Round(amount, valuations, costs)
        t_end = time.time() + TIME

        # while time rounds hasn't ended
        while time.time() < t_end:

            # check if round can continue (not last round)
            if not period.last_round:

                # select random agent and make offer
                agent = random.choice(period.agents)

                if agent.type == "buyer":
                    price = agent.offer_price(period.max_bid["price"])

                elif agent.type == "seller":
                    price = agent.offer_price(period.min_ask["price"])

                # price = agent.offer_price()

                # check if offer was valid (better than own price)
                if price:
                    procces_offer(price, period, agent)

                    if period.reset_round():
                        period.agents += period.succes
                        period.succes = []
                    elif period.check_last_round():
                        period.last_round = True

                # else:
                #     print("False")

            # if round cannot continue, break out of loop (round)
            else:
                break

        # prints allocative efficiency
        print(f"surplus: {period.surplus}")
        print(f"allocative efficiency: {round(period.surplus / surplus * 100, 2)}%")
        save_plots_transactions(period, counter)

def total_surplus():
    """
    Calculates max total surplus
    """

    surplus = 0;
    for i in range(len(VALUATION)):
        if VALUATION[i][0] >= COSTS[i][0]:
            surplus += (VALUATION[i][0] - COSTS[i][0]) * COSTS[i][1]

    return surplus

def plot_demand_supply(valuations, costs, market):
    """
    Plots demand and supply curve of given market
    """

    fig = plt.figure()
    plt.step(valuations[:,1], valuations[:,0], label="Demand")
    plt.step(costs[:,1], costs[:,0], label="Supply")
    plt.title(f"Demand/Supply curves for {market}")
    plt.xlabel("Quantity")
    plt.ylabel("Price")
    plt.legend(loc='upper right')
    fig.savefig(f'curves_{market}.png')
    plt.close()

def not_last_round(agents, last_round):
    """
    Checks for last round
    """
    return len(agents) > 1 and not last_round

def procces_offer(price, round, agent):
    """
    Adjust outstanding offer, if bid is better, and
    checks if transaction is possible, if so make transaction
    """

    if agent.type == "buyer" and price > round.max_bid["price"]:
        round.max_bid["id"] = agent.id
        round.max_bid["price"] = price

    elif agent.type == "seller" and price < round.min_ask["price"]:
        round.min_ask["id"] = agent.id
        round.min_ask["price"] = price

    if round.check_transaction():
        round.make_transaction()

def save_plots_transactions(round, counter):
    """
    Save plot figures transaction prices per round
    """

    fig_trans = plt.figure()
    plt.plot(list(range(len(round.transactions))), round.transactions)
    plt.title(f"The development of transaction prices (Market 1) round: {counter + 1}")
    plt.xlabel("Number of transactions")
    plt.ylabel("Transactions price")
    fig_trans.savefig(f"{round.name}/market_prices/{round.name}_market1_round{counter + 1}")
    plt.close()


if __name__ =="__main__":
    main()
