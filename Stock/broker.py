class Broker(object):
    """
    A model for stock broker.
    """

    #################
    # Object fileds #
    #################

    sell_list = []
    """
    Each element in the sell list is a tuple of (player, stock).
    """

    buy_list = []
    """
    Each element in the buy list is tuple of (player, target_price).
    """

    ##################
    # Private method #
    ##################

    def _clean_list(self, target_seller, target_buyer, target_stock):
        """
        Clean up the sell and buy list after a transaction to remove
        expired or dirty data.

        Only keep the top 10000 recently records.
        """
        self.sell_list = filter(
            lambda tuple:
                tuple[0] != target_seller or
                tuple[1] != target_stock,
            self.sell_list[-10000:])
        self.buy_list = filter(
            lambda tuple:
                tuple[0] != target_buyer or
                tuple[1] != target_stock.sales_price,
            self.buy_list[-10000:])

    def _match_player(self):
        """
        Find and return 2 different players whose target prices are matched.
        """
        self.sell_list.sort(key=lambda tuple: tuple[1].sales_price)
        for (seller, stock) in self.sell_list:
            for (buyer, target_price) in self.buy_list:
                if seller != buyer and \
                        stock.sales_price <= target_price:
                    self.sell_list.remove((seller, stock))
                    self.buy_list.remove((buyer, target_price))
                    return (seller, buyer, stock)

        return (None, None, None)

    def _trade(self, seller, buyer, stock):
        """
        Do an actual transaction for seller and buyer.
        """
        traded = False
        if buyer.money_balance >= stock.sales_price:
            #################
            # Update seller #
            #################

            seller.stock_list.remove(stock)
            seller.money_balance += stock.sales_price

            ################
            # Update buyer #
            ################

            buyer.stock_list.append(stock)
            buyer.money_balance -= stock.sales_price

            stock.last_transaction_price = stock.sales_price
            stock.transaction_counting()

            traded = True

        self._clean_list(seller, buyer, stock)
        return traded

    ###################
    # Object function #
    ###################

    def update_sell_list(self, player, stock):
        """
        Append the sell list.
        """
        if player and stock:
            self.sell_list.append((player, stock))

    def update_buy_list(self, player, target_price):
        """
        Append the buy list.
        """
        if player and target_price:
            self.buy_list.append((player, target_price))

    def work(self):
        """
        Single complete work round for broker.
        """
        (seller, buyer, stock) = self._match_player()
        if seller and buyer and stock:
            traded = self._trade(seller, buyer, stock)
        else:
            traded = False

        return (seller, buyer, stock, traded)


class BrokerSingleton(object):
    """
    A singleton class for broker.
    """

    instance = None

    def __new__(cls, *args, **kwds):
        if not cls.instance:
            cls.instance = Broker()

        return cls.instance
