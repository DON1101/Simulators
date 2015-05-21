import random
from broker import BrokerSingleton


class PlayerBase(object):
    """
    A base model for stock player in the market.
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

    perseverance = 1
    """
    Perseverance of a player, which is used in adjusting target price.
    A higher perseverance indicates less likely the player would change his
    target price.
    """

    period_tick = 0
    """
    A clock ticking in every market period.
    """

    target_sell_price_last = 0.0
    """
    Target price for sell in last market period.
    """

    target_buy_price_last = 0.0
    """
    Target price for buy in last market period.
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
        self.perseverance = random.randint(1, 10)
        self.period_tick = 0

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
    # Object property #
    ###################

    @property
    def target_sell_price(self):
        """
        Return the target price for sell.
        Returning a None value means no price adjustment in next period.
        """
        (avg_price,
         max_price,
         min_price) = self.market.get_stock_price_last_period()

        target_price = max(avg_price + random.randint(-10, 10), 1.0)

        return target_price

    @property
    def target_buy_price(self):
        """
        Return the target price for buy.
        Returning a None value means no price adjustment in next period.
        """
        (avg_price,
         max_price,
         min_price) = self.market.get_stock_price_last_period()

        target_price = min(avg_price + random.randint(-10, 10),
                           self.money_balance * 0.5)

        return target_price

    ###################
    # Object function #
    ###################

    def try_sell(self):
        """
        Inform the broker that I want to sell some stock.
        """
        if self.stock_list:
            target_price = self.target_sell_price
            if target_price is not None:
                self.target_sell_price_last = target_price
                self._set_price(target_price)

            self._try_sell_stock(self.stock_list[0])

    def try_buy(self):
        """
        Inform the broker that I want to buy some stock.
        """
        target_price = self.target_buy_price
        if target_price is not None:
            self.target_buy_price_last = target_price
        else:
            target_price = self.target_buy_price_last

        self._try_buy_stock(target_price)

    def period_ticking(self):
        self.period_tick += 1

    ####################
    # STANDARD METHODS #
    ####################

    def __repr__(self):
        return str(self.identifier)

    def __str__(self):
        return str(self.identifier)
