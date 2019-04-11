import numpy as np
import matplotlib.pylab as plt
import time
from round import Round

TYPES = ["buyer", "seller"]
AMOUNT = 12
TIME = 30
VALUATION = np.array([[125, 6], [115, 6], [95, 6], [80, 6], [65, 6], [55, 6]])
COSTS = np.array([[75, 6], [70, 6], [65, 6], [60, 6], [55, 6], [50, 6]])

def main():

    # calculate max total surplus
    surplus = total_surplus()
    print(f"max surplus: {surplus}")

    # create trading round
    round = Round(TYPES, AMOUNT, VALUATION, COSTS)

    t_end = time.time() + TIME
    while time.time() < t_end:

        if len(round.agents) > 1:
            # select random agent
            number = np.random.randint(0, len(round.agents) - 1)
            agent = round.agents[number]

            # make offer
            price = agent.offer_price()

            if price:

                # checks if agent is buyer/seller and
                # if offer is better than outstanding offer
                if agent.type == "buyer" and price > round.max_bid[1]:
                    round.max_bid[0] = agent.id
                    round.max_bid[1] = price

                elif agent.type == "seller" and price < round.min_ask[1]:
                    round.min_ask[0] = agent.id
                    round.min_ask[1] = price

                if round.check_transaction():
                    round.make_transaction()

        else:
            break

    # plots demand/supply curve
    # plt.step(np.arange(0,6), VALUATION[:,0])
    # plt.step(np.arange(0,6), COSTS[:,0])
    # plt.show()

    # prints allocative efficiency
    print(f"surplus: {round.surplus}")
    print(f"allocative efficiency: {round.surplus / surplus * 100}")

    # plot transaction price against time
    plt.plot(list(range(len(round.transactions))), round.transactions)
    plt.show()

def total_surplus():

    surplus = 0;
    for i in range(len(VALUATION)):
        surplus += (VALUATION[i][0] - COSTS[i][0]) * COSTS[i][1]

    return surplus


if __name__ =="__main__":
    main()
