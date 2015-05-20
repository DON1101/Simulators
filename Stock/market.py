from broker import BrokerSingleton
from player import Player
from stock import Stock


class Market(object):
    """
    A model for stock market.
    """

    #################
    # Object fileds #
    #################

    player_list = None
    """
    All the players in this stock market.
    """

    stocks_last_period = None
    """
    All the stocks traded during last period
    """

    last_avg_price = 0.0
    """
    The last recorded average market price.
    """

    broker = BrokerSingleton()
    """
    The singleton broker.
    All the transactions need to be done only through this broker.
    """

    ##################
    # Initial method #
    ##################

    def __init__(self, players_num=100, stocks_num=10000):
        """
        Initialize the market.
        """
        self.player_list = []
        for i in range(players_num):
            self.player_list.append(Player(i, 10000.0, self))

        stock_list = []
        for i in range(stocks_num):
            stock_list.append(Stock(i, 1.0))

        seed_stockholder = self.player_list[0]
        seed_stockholder.stock_list = stock_list

    ##################
    # Private method #
    ##################

    def __ready_for_next_period(self):
        self.stocks_last_period = []

    ###################
    # Object function #
    ###################

    def get_stock_price_last_period(self):
        """
        Get an average price for all stocks traded during last period.
        """
        if not self.stocks_last_period:
            return self.last_avg_price

        total_price = sum([stock.last_transaction_price
                           for stock in self.stocks_last_period])
        avg_price = total_price / (len(self.stocks_last_period) + 0.01)
        self.last_avg_price = avg_price
        return avg_price

    def run_period(self):
        """
        Run the market for one period time.
        """
        self.__ready_for_next_period()

        print "Sell list {0}, Buy list {1}".format(
            len(self.broker.sell_list),
            len(self.broker.buy_list)
        )

        for player in self.player_list:
            player.adjust_price()
            player.try_sell()
            player.try_buy()

        for i in range(100):
            (seller, buyer, stock) = self.broker.work()
            if stock:
                self.stocks_last_period.append(stock)

        print ("During last period, {0} stocks are traded, "
               "avg price {1}".format(
                   len(self.stocks_last_period),
                   self.get_stock_price_last_period())
               )
