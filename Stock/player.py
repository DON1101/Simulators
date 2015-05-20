import random
from broker import BrokerSingleton


class Player(object):
    """
    A model for stock player in the market.
    """

    #################
    # Object fileds #
    #################

    identifier = ""
    """
    The universal identifier for this player.
    """

    money_balance = 0.0
    """
    The amount of money in this player's pocket currently.
    """

    stock_list = None
    """
    The stocks this player is holding currently.
    """

    broker = BrokerSingleton()
    """
    The singleton broker.
    All the transactions need to be done only through this broker.
    """

    market = None
    """
    The stock market object.
    """

    ##################
    # Initial method #
    ##################

    def __init__(self, identifier, money, market):
        self.identifier = identifier
        self.money_balance = money
        self.market = market
        self.stock_list = []

        print "Player {0} is born with money {1}".format(identifier, money)

    ##################
    # Private method #
    ##################

    def _set_price(self, target_price):
        """
        Set price for all the stocks in hand.
        """
        for stock in self.stock_list:
            stock.sales_price = target_price

    def _try_sell_stock(self, stock):
        """
        Inform the broker that I want to sell this stock.
        """
        if stock in self.stock_list:
            self.broker.update_sell_list(self, stock)

    def _try_buy_stock(self, target_price):
        """
        Inform the broker that I want to buy stock in target_price.
        """
        if self.money_balance >= target_price:
            self.broker.update_buy_list(self, target_price)

    ###################
    # Object function #
    ###################

    def adjust_price(self):
        """
        Player will observe the market and adjust his own stock price.
        """
        market_price = self.market.get_stock_price_last_period()
        self._set_price(market_price + random.randint(0, 100) / 100.0)

    def try_sell(self):
        """
        Inform the broker that I want to sell some stock.
        """
        if self.stock_list:
            self._try_sell_stock(self.stock_list[0])

    def try_buy(self):
        """
        Inform the broker that I want to buy some stock.
        """
        market_price = self.market.get_stock_price_last_period()
        self._try_buy_stock(market_price + random.randint(0, 100) / 100.0)

    ####################
    # STANDARD METHODS #
    ####################

    def __repr__(self):
        return str(self.identifier)

    def __str__(self):
        return str(self.identifier)
