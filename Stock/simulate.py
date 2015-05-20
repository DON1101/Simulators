from market import Market


if __name__ == "__main__":
    #########################
    # Initialize the market #
    #########################

    market = Market(players_num=100, stocks_num=10000)

    ###############################
    # Start market behaviour loop #
    ###############################

    for i in range(10000):
        print i
        market.run_period()
