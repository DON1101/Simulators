import csv
from market import Market


if __name__ == "__main__":
    #########################
    # Initialize the market #
    #########################

    market = Market(players_num=100, stocks_num=10000)

    ###############################
    # Start market behaviour loop #
    ###############################

    file_out = open("/tmp/market_price.csv", "w")
    csv_writer = csv.writer(file_out)

    for i in range(100):
        print i
        market.run_period()
        csv_writer.writerow([market.get_stock_price_last_period()[0]])

    file_out.flush()
    file_out.close()
