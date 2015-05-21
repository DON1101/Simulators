import random
from player_base import PlayerBase


class Player(PlayerBase):
    """
    A model for stock player in the market.
    """

    #############################
    # Overrided Object property #
    #############################

    @property
    def target_sell_price(self):
        """
        Return the target price for sell.
        Returning a None value means no price adjustment in next period.
        """
        return super(Player, self).target_sell_price

    @property
    def target_buy_price(self):
        """
        Return the target price for buy.
        Returning a None value means no price adjustment in next period.
        """
        if self.period_tick == 0:
            return random.randint(1, 10)
        elif self.period_tick % self.perseverance == 0:
            # Player runs out of patience and decides to change target price.
            (avg_price,
             max_price,
             min_price) = self.market.get_stock_price_last_period()

            power = self.period_tick / self.perseverance
            target_price = min(min_price + power, self.money_balance * 0.5)
            return target_price
        else:
            return None
