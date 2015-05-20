class Stock(object):
    """
    A model for stock.
    """

    ##################
    # Initial method #
    ##################

    def __init__(self, identifier, init_price):
        self.identifier = identifier
        self.sales_price = init_price

        print "Stock {0} is created at price {1}".format(
            identifier,
            init_price
        )

    #################
    # Object fileds #
    #################

    identifier = None
    """
    A universal identifier for this stock.
    """

    sales_price = 0.0
    """
    The current price of this stock, which is set by stock holder.
    """

    last_transaction_price = 0.0
    """
    The price in last transaction.
    This is used for statistic calculation in the whole market.
    """

    ####################
    # STANDARD METHODS #
    ####################

    def __repr__(self):
        return str(self.identifier)

    def __str__(self):
        return str(self.identifier)
