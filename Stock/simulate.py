import csv
from market import Market


if __name__ == "__main__":
    #########################
    # Initialize the market #
    #########################

    market = Market(players_num=100, stocks_num=1000)

    ###############################
    # Start market behaviour loop #
    ###############################

    file_out_price = open("/tmp/market_prices.csv", "w")
    file_out_player = open("/tmp/market_players.csv", "w")
    file_out_stock = open("/tmp/market_stocks.csv", "w")
    csv_writer_price = csv.writer(file_out_price)
    csv_writer_player = csv.writer(file_out_player)
    csv_writer_stock = csv.writer(file_out_stock)

    for i in range(5000):
        print i
        market.run_period()

        (avg_price,
         max_price,
         min_price) = market.get_stock_price_last_period()
        csv_writer_price.writerow([
            avg_price,
            max_price,
            min_price
        ])
        file_out_price.flush()

    player_list = market.rank_player_wealth()
    stock_list = market.rank_stock()

    for player in player_list:
        csv_writer_player.writerow([
            player.money_balance,
            len(player.stock_list),
            player.perseverance,
        ])

    for stock in stock_list:
        csv_writer_stock.writerow([
            stock.sales_price,
            stock.transaction_count,
        ])

    file_out_price.flush()
    file_out_player.flush()
    file_out_stock.flush()

    file_out_price.close()
    file_out_player.close()
    file_out_stock.close()
