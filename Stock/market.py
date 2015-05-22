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
            self.player_list.append(Player(i, 1000.0, self))

        stock_list = []
        for i in range(stocks_num):
            stock_list.append(Stock(i, 1.0))

        seed_stockholder = self.player_list[0]
        seed_stockholder.stock_list = stock_list

    ##################
    # Private method #
    ##################

    def _ready_for_next_period(self):
        self.stocks_last_period = []

    ###################
    # Object function #
    ###################

    def get_stock_price_last_period(self):
        """
        Get an average price for all stocks traded during last period.
        """
        if not self.stocks_last_period:
            return (self.last_avg_price,
                    self.last_avg_price,
                    self.last_avg_price)

        price_list = [stock.last_transaction_price
                      for stock in self.stocks_last_period]
        total_price = sum(price_list)
        avg_price = total_price / (len(self.stocks_last_period) + 0.01)
        self.last_avg_price = avg_price
        return (avg_price, max(price_list), min(price_list))

    def run_period(self):
        """
        Run the market for one period time.
        """
        self._ready_for_next_period()

        ########################
        # Players do their job #
        ########################

        for player in self.player_list:
            player.try_sell()
            player.try_buy()
            player.period_ticking()

        print "Sell list {0}, Buy list {1}".format(
            len(self.broker.sell_list),
            len(self.broker.buy_list)
        )

        #####################
        # Broker do his job #
        #####################

        while True:
            (seller, buyer, stock, traded) = self.broker.work()
            if traded:
                self.stocks_last_period.append(stock)
            else:
                break

        (avg_price,
         max_price,
         min_price) = self.get_stock_price_last_period()
        print ("During last period, {0} stocks are traded, "
               "avg price {1}, max price {2}, min price {3}".format(
                   len(self.stocks_last_period),
                   avg_price,
                   max_price,
                   min_price)
               )

    def rank_player_wealth(self):
        player_list = sorted(self.player_list,
                             key=lambda p: p.money_balance,
                             reverse=True)
        for player in player_list:
            print "Player {0} with money {1}. Perseverance {2}".format(
                player.identifier,
                player.money_balance,
                player.perseverance)
