import numpy as np
import matplotlib.pylab as plt
import time
import random
from round import Round

TYPES = ["buyer", "seller"]
AMOUNT = 12
TIME = 120
ROUNDS = 6
VALUATION = np.array([[105, 6], [97, 6], [90, 6], [82, 6], [75, 6], [70, 6]])
COSTS = np.array([[40, 6], [47, 6], [55, 6], [62, 6], [65, 6], [80, 6]])

# # plots demand/supply curve
# fig = plt.figure()
# plt.step(np.arange(0,6), VALUATION[:,0])
# plt.step(np.arange(0,6), COSTS[:,0])
# fig.savefig('curves_market1.png')
# plt.close()

def main():

    # calculate max total surplus
    surplus = total_surplus()
    print(f"max surplus: {surplus}")

    # repeat simulation for ROUNDS times
    for counter in range(ROUNDS):

        # create trading round and set time for round
        round = Round(TYPES, AMOUNT, VALUATION, COSTS)
        t_end = time.time() + TIME

        # while time of round hasn't end
        while time.time() < t_end:

            # check if round can continue
            if not_last_round(round.agents, round.last_round):

                # select random agent and make offer
                agent = random.choice(round.agents)
                price = agent.offer_price()

                # check if offer was valid
                if price:
                    procces_offer(price, round, agent)
            else:
                print("true")
                break

        # prints allocative efficiency
        print(f"surplus: {round.surplus}")
        print(f"allocative efficiency: {round.surplus / surplus * 100}")

        save_plots_transactions(round, counter)
        print(round.transactions)

def total_surplus():
    """
    Calculates max total surplus
    """

    surplus = 0;
    for i in range(len(VALUATION)):
        surplus += (VALUATION[i][0] - COSTS[i][0]) * COSTS[i][1]

    return surplus

def not_last_round(agents, last_round):
    """
    Checks for last round
    """
    return len(agents) > 1 and not last_round

def procces_offer(price, round, agent):
    """
    Adjust outstanding offer, if bid is better, and
    checks if transaction is possible
    """

    if agent.type == "buyer" and price > round.max_bid[1]:
        round.max_bid[0] = agent.id
        round.max_bid[1] = price

    elif agent.type == "seller" and price < round.min_ask[1]:
        round.min_ask[0] = agent.id
        round.min_ask[1] = price

    if round.check_transaction():
        round.make_transaction()

def save_plots_transactions(round, counter):
    """
    Save plot figures transaction prices per round
    """

    fig_trans = plt.figure()
    plt.plot(list(range(len(round.transactions))), round.transactions)
    fig_trans.savefig(f"{round.name}/market_prices/ZI-U_market1_round{counter + 1}")
    plt.close()


if __name__ =="__main__":
    main()
